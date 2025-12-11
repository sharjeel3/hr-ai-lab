"""
Career Pathway Recommendation Engine (Experiment D)

This module implements an AI-powered career pathway recommendation system that:
1. Analyzes employee skill profiles using embeddings
2. Compares against internal job family roles
3. Recommends top 3 next career steps
4. Generates personalized 90-day development plans
5. Provides detailed explanations for each recommendation

Architecture:
- Embeddings: sentence-transformers for skill similarity
- Vector Store: FAISS for efficient similarity search
- LLM: Gemini for explanation generation and development planning
"""

import os
import sys
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from scripts.utils import LLMClient, load_json_data, save_results, logger

try:
    from sentence_transformers import SentenceTransformer
    import faiss
except ImportError:
    logger.error("Required packages not installed. Run: pip install sentence-transformers faiss-cpu")
    SentenceTransformer = None
    faiss = None


class CareerPathwayRecommender:
    """AI-powered career pathway recommendation engine."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize career pathway recommender.
        
        Args:
            config: Configuration dictionary with LLM and embedding settings
        """
        self.config = config
        self.llm_client = LLMClient(
            provider=config.get('llm_provider', 'google'),
            model=config.get('llm_model', 'gemini-2.5-flash-lite')
        )
        
        # Initialize embedding model
        embedding_model = config.get('embedding_model', 'sentence-transformers/all-MiniLM-L6-v2')
        try:
            self.embedding_model = SentenceTransformer(embedding_model)
            logger.info(f"Loaded embedding model: {embedding_model}")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            self.embedding_model = None
        
        # Initialize vector store
        self.index = None
        self.job_roles = []
        self.similarity_threshold = config.get('similarity_threshold', 0.7)
        
    def load_job_families(self, job_family_paths: List[str]) -> None:
        """
        Load job family data and build vector index.
        
        Args:
            job_family_paths: List of paths to job family JSON files
        """
        logger.info(f"Loading {len(job_family_paths)} job families...")
        
        all_roles = []
        
        for path in job_family_paths:
            try:
                job_family = load_json_data(path)
                family_name = job_family.get('family_name', 'Unknown')
                career_levels = job_family.get('career_levels', [])
                
                for level in career_levels:
                    role = {
                        'job_family': family_name,
                        'job_family_id': job_family.get('job_family_id', 'Unknown'),
                        'level': level.get('level'),
                        'title': level.get('title'),
                        'years_experience': level.get('years_experience'),
                        'salary_range': level.get('salary_range'),
                        'responsibilities': level.get('key_responsibilities', []),
                        'required_skills': level.get('required_skills', []),
                        'nice_to_have': level.get('nice_to_have', []),
                        'promotion_criteria': level.get('promotion_criteria', '')
                    }
                    all_roles.append(role)
                    
            except Exception as e:
                logger.error(f"Error loading job family from {path}: {e}")
        
        self.job_roles = all_roles
        logger.info(f"Loaded {len(all_roles)} roles across job families")
        
        # Build vector index
        if self.embedding_model:
            self._build_vector_index()
    
    def _build_vector_index(self) -> None:
        """Build FAISS vector index for job roles."""
        if not self.job_roles:
            logger.warning("No job roles loaded. Cannot build vector index.")
            return
        
        logger.info("Building vector index...")
        
        # Create text representations of roles
        role_texts = []
        for role in self.job_roles:
            text = self._role_to_text(role)
            role_texts.append(text)
        
        # Generate embeddings
        try:
            embeddings = self.embedding_model.encode(role_texts, show_progress_bar=True)
            
            # Build FAISS index
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings)
            self.index.add(embeddings.astype('float32'))
            
            logger.info(f"Built vector index with {len(role_texts)} roles, dimension {dimension}")
            
        except Exception as e:
            logger.error(f"Error building vector index: {e}")
            self.index = None
    
    def _role_to_text(self, role: Dict[str, Any]) -> str:
        """Convert role dictionary to text for embedding."""
        parts = [
            f"Job Title: {role['title']}",
            f"Job Family: {role['job_family']}",
            f"Required Skills: {', '.join(role['required_skills'])}",
            f"Responsibilities: {', '.join(role['responsibilities'][:3])}",  # Top 3
            f"Nice to Have: {', '.join(role['nice_to_have'])}"
        ]
        return " | ".join(parts)
    
    def _employee_to_text(self, employee: Dict[str, Any]) -> str:
        """Convert employee profile to text for embedding."""
        parts = [
            f"Current Role: {employee.get('current_title', '')}",
            f"Skills: {', '.join(employee.get('skills', []))}",
            f"Experience: {employee.get('years_experience', 0)} years",
            f"Education: {employee.get('education_level', '')}",
            f"Certifications: {', '.join(employee.get('certifications', []))}",
            f"Interests: {', '.join(employee.get('career_interests', []))}"
        ]
        return " | ".join(parts)
    
    def _is_valid_next_step(
        self, 
        employee: Dict[str, Any], 
        role: Dict[str, Any],
        apply_strict_rules: bool = True
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Check if a role is a valid next career step with comprehensive business rules.
        
        Args:
            employee: Employee profile
            role: Candidate role
            apply_strict_rules: If True, enforce all organizational policies
            
        Returns:
            Tuple of (is_valid, eligibility_details)
        """
        eligibility = {
            'is_eligible': False,
            'reasons': [],
            'blockers': [],
            'readiness_score': 0.0,  # 0-100%
            'estimated_timeline': None,  # When they'll be eligible
            'requirements_met': {},
            'requirements_needed': {}
        }
        
        # Parse employee data with type conversion
        try:
            current_years = float(employee.get('years_experience', 0))
        except (ValueError, TypeError):
            current_years = 0
            
        try:
            time_in_current_role = float(employee.get('time_in_current_role_years', 0))
        except (ValueError, TypeError):
            time_in_current_role = 0
            
        try:
            performance_rating = float(employee.get('performance_rating', 3.0))
        except (ValueError, TypeError):
            performance_rating = 3.0
            
        education_level = employee.get('education_level', '')
        certifications = set(employee.get('certifications', []))
        
        # Parse role years requirement with proper type conversion
        role_years = role.get('years_experience', '0-100')
        try:
            if isinstance(role_years, (int, float)):
                # If it's already a number, treat it as minimum
                min_years = float(role_years)
                max_years = 100
            elif isinstance(role_years, str):
                if '-' in role_years:
                    parts = role_years.split('-')
                    min_years = float(parts[0].strip())
                    max_years = float(parts[1].strip())
                elif '+' in role_years:
                    min_years = float(role_years.replace('+', '').strip())
                    max_years = 100
                else:
                    min_years = float(role_years.strip())
                    max_years = 100
            else:
                min_years, max_years = 0, 100
        except (ValueError, AttributeError):
            min_years, max_years = 0, 100
        
        points_earned = 0
        max_points = 100
        
        # ==============================================================
        # BUSINESS RULE 1: Experience Requirements (25 points)
        # ==============================================================
        if current_years >= min_years:
            points_earned += 25
            eligibility['requirements_met']['experience'] = True
            eligibility['reasons'].append(f"✓ Meets experience requirement ({current_years} >= {min_years} years)")
        else:
            gap_years = min_years - current_years
            eligibility['requirements_needed']['experience'] = f"Need {gap_years} more years of experience"
            eligibility['blockers'].append(f"✗ Insufficient experience: {current_years} years (need {min_years}+)")
            
            # Estimate when they'll be eligible
            eligibility['estimated_timeline'] = f"{gap_years} years from now"
        
        # Don't recommend roles that are too senior (stretch is ok, but not unrealistic)
        if current_years < min_years - 2:
            eligibility['blockers'].append(f"✗ Role too senior: requires {min_years}+ years (you have {current_years})")
        
        # ==============================================================
        # BUSINESS RULE 2: Time-in-Role Requirement (20 points)
        # ==============================================================
        MIN_TIME_IN_ROLE = 2  # Typically 18-24 months minimum
        
        if time_in_current_role >= MIN_TIME_IN_ROLE:
            points_earned += 20
            eligibility['requirements_met']['time_in_role'] = True
            eligibility['reasons'].append(f"✓ Meets time-in-role requirement ({time_in_current_role} years)")
        else:
            gap_months = int((MIN_TIME_IN_ROLE - time_in_current_role) * 12)
            eligibility['requirements_needed']['time_in_role'] = f"Need {gap_months} more months in current role"
            eligibility['blockers'].append(f"✗ Must spend {MIN_TIME_IN_ROLE} years in current role (currently {time_in_current_role} years)")
            
            if not eligibility['estimated_timeline']:
                eligibility['estimated_timeline'] = f"{gap_months} months from now"
        
        # ==============================================================
        # BUSINESS RULE 3: Performance Rating (25 points)
        # ==============================================================
        MIN_PERFORMANCE_RATING = 3.5  # "Meets Expectations" or higher
        IDEAL_PERFORMANCE_RATING = 4.0  # "Exceeds Expectations"
        
        if performance_rating >= IDEAL_PERFORMANCE_RATING:
            points_earned += 25
            eligibility['requirements_met']['performance'] = 'Exceeds Expectations'
            eligibility['reasons'].append(f"✓ Strong performance rating ({performance_rating}/5.0)")
        elif performance_rating >= MIN_PERFORMANCE_RATING:
            points_earned += 15
            eligibility['requirements_met']['performance'] = 'Meets Expectations'
            eligibility['reasons'].append(f"○ Adequate performance rating ({performance_rating}/5.0)")
        else:
            eligibility['requirements_needed']['performance'] = f"Improve rating to {MIN_PERFORMANCE_RATING}+"
            eligibility['blockers'].append(f"✗ Performance rating below threshold ({performance_rating} < {MIN_PERFORMANCE_RATING})")
        
        # ==============================================================
        # BUSINESS RULE 4: Education Requirements (15 points)
        # ==============================================================
        role_education = role.get('education_requirement', '')
        
        education_levels = {
            'high school': 1,
            'associate': 2,
            'bachelor': 3,
            'master': 4,
            'phd': 5,
            'doctorate': 5
        }
        
        employee_level = 0
        for level, value in education_levels.items():
            if level in education_level.lower():
                employee_level = value
                break
        
        role_level = 0
        for level, value in education_levels.items():
            if level in role_education.lower():
                role_level = value
                break
        
        if employee_level >= role_level:
            points_earned += 15
            eligibility['requirements_met']['education'] = True
            eligibility['reasons'].append(f"✓ Meets education requirement")
        elif role_education:
            eligibility['requirements_needed']['education'] = role_education
            eligibility['blockers'].append(f"✗ Education requirement: {role_education}")
        
        # ==============================================================
        # BUSINESS RULE 5: Required Certifications (15 points)
        # ==============================================================
        required_certs = set(role.get('required_certifications', []))
        
        if required_certs:
            if required_certs.issubset(certifications):
                points_earned += 15
                eligibility['requirements_met']['certifications'] = list(required_certs)
                eligibility['reasons'].append(f"✓ Has all required certifications")
            else:
                missing_certs = required_certs - certifications
                eligibility['requirements_needed']['certifications'] = list(missing_certs)
                eligibility['blockers'].append(f"✗ Missing certifications: {', '.join(missing_certs)}")
        else:
            points_earned += 15  # No certs required
        
        # ==============================================================
        # Calculate Final Readiness Score
        # ==============================================================
        eligibility['readiness_score'] = (points_earned / max_points) * 100
        
        # Determine eligibility
        if apply_strict_rules:
            # STRICT MODE: Must meet ALL critical requirements
            eligibility['is_eligible'] = (
                len(eligibility['blockers']) == 0 and
                eligibility['readiness_score'] >= 70
            )
        else:
            # LENIENT MODE: Can recommend if readiness >= 50% (for career planning)
            eligibility['is_eligible'] = eligibility['readiness_score'] >= 50
        
        return eligibility['is_eligible'], eligibility
    
    def recommend_pathways(
        self, 
        employee_profile: Dict[str, Any],
        top_k: int = 3,
        include_future_roles: bool = True  # NEW: Include roles not yet eligible for
    ) -> Dict[str, Any]:
        """
        Recommend career pathways for an employee.
        
        Args:
            employee_profile: Employee profile with skills, experience, interests
            top_k: Number of recommendations to return (default: 3)
            include_future_roles: If True, include roles employee will be eligible for later
            
        Returns:
            Dictionary with recommendations and explanations
        """
        if not self.index or not self.job_roles:
            logger.error("Vector index not built. Call load_job_families first.")
            return {
                'error': 'Vector index not initialized',
                'recommendations': []
            }
        
        # Generate employee embedding
        employee_text = self._employee_to_text(employee_profile)
        try:
            employee_embedding = self.embedding_model.encode([employee_text])
            faiss.normalize_L2(employee_embedding)
            
            # Search for similar roles
            similarities, indices = self.index.search(
                employee_embedding.astype('float32'), 
                top_k * 3  # Get more candidates for filtering
            )
            
            # Filter and rank candidates
            eligible_now = []
            eligible_soon = []  # Future opportunities
            
            for i, (idx, similarity) in enumerate(zip(indices[0], similarities[0])):
                if idx < len(self.job_roles):
                    role = self.job_roles[idx].copy()
                    role['similarity_score'] = float(similarity)
                    
                    # Check eligibility with business rules
                    if similarity >= self.similarity_threshold:
                        is_eligible, eligibility_details = self._is_valid_next_step(
                            employee_profile, 
                            role,
                            apply_strict_rules=True
                        )
                        
                        role['eligibility'] = eligibility_details
                        
                        if is_eligible:
                            eligible_now.append(role)
                        elif include_future_roles and eligibility_details['readiness_score'] >= 50:
                            eligible_soon.append(role)
            
            # Select top K from each category
            top_eligible_now = eligible_now[:top_k]
            top_eligible_soon = eligible_soon[:top_k]
            
            # Generate explanations and development plans
            recommendations_now = []
            for candidate in top_eligible_now:
                explanation = self._generate_explanation(employee_profile, candidate)
                development_plan = self._generate_development_plan(employee_profile, candidate)
                
                recommendations_now.append({
                    'role': candidate,
                    'similarity_score': candidate['similarity_score'],
                    'eligibility': candidate['eligibility'],
                    'status': 'ELIGIBLE_NOW',
                    'explanation': explanation,
                    'development_plan': development_plan
                })
            
            recommendations_soon = []
            for candidate in top_eligible_soon:
                explanation = self._generate_explanation(employee_profile, candidate)
                development_plan = self._generate_development_plan(employee_profile, candidate)
                
                recommendations_soon.append({
                    'role': candidate,
                    'similarity_score': candidate['similarity_score'],
                    'eligibility': candidate['eligibility'],
                    'status': 'FUTURE_OPPORTUNITY',
                    'explanation': explanation,
                    'development_plan': development_plan
                })
            
            return {
                'employee_id': employee_profile.get('employee_id', 'Unknown'),
                'employee_name': employee_profile.get('name', 'Unknown'),
                'current_title': employee_profile.get('current_title', 'Unknown'),
                'recommendations': {
                    'eligible_now': recommendations_now,
                    'future_opportunities': recommendations_soon
                },
                'summary': {
                    'eligible_now_count': len(recommendations_now),
                    'future_opportunities_count': len(recommendations_soon),
                    'total_candidates_evaluated': len(eligible_now) + len(eligible_soon)
                },
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'similarity_threshold': self.similarity_threshold,
                    'business_rules_applied': True
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return {
                'error': str(e),
                'employee_id': employee_profile.get('employee_id', 'Unknown'),
                'recommendations': {'eligible_now': [], 'future_opportunities': []}
            }
    
    def _generate_explanation(self, employee: Dict, role: Dict) -> str:
        """
        Generate LLM-based explanation for why this role is a good fit.
        
        Args:
            employee: Employee profile
            role: Candidate role
            
        Returns:
            Natural language explanation
        """
        prompt = f"""Analyze why this career move makes sense:

EMPLOYEE PROFILE:
- Name: {employee.get('name', 'Unknown')}
- Current Role: {employee.get('current_title', 'Unknown')}
- Years of Experience: {employee.get('years_experience', 0)}
- Skills: {', '.join(employee.get('skills', []))}
- Career Interests: {', '.join(employee.get('career_interests', []))}

TARGET ROLE:
- Title: {role.get('title', 'Unknown')}
- Job Family: {role.get('job_family', 'Unknown')}
- Required Experience: {role.get('years_experience', 'Unknown')}
- Key Skills: {', '.join(role.get('key_skills', []))}

Provide a 2-3 sentence explanation of:
1. Why this is a logical next step
2. Which skills transfer well
3. What makes the employee a strong candidate

Keep it professional and concise."""

        try:
            response = self.llm_client.generate(prompt, max_tokens=200)
            return response.strip()
        except Exception as e:
            logger.warning(f"LLM explanation failed: {e}")
            return f"This role aligns with your background in {employee.get('current_title', 'your field')} and matches {len(set(employee.get('skills', [])) & set(role.get('key_skills', [])))} of your key skills."
    
    def _generate_development_plan(self, employee: Dict, role: Dict) -> str:
        """
        Generate a 90-day development plan for transitioning to the new role.
        
        Args:
            employee: Employee profile
            role: Candidate role
            
        Returns:
            90-day development plan
        """
        prompt = f"""Create a focused 90-day development plan for this career transition:

CURRENT STATE:
- Current Role: {employee.get('current_title', 'Unknown')}
- Current Skills: {', '.join(employee.get('skills', [])[:10])}

TARGET ROLE:
- Title: {role.get('title', 'Unknown')}
- Required Skills: {', '.join(role.get('key_skills', [])[:10])}
- Experience Level: {role.get('years_experience', 'Unknown')}

Provide a structured 90-day plan with:
- Month 1: Foundation building (30 days)
- Month 2: Skill development (30-60 days)
- Month 3: Application & demonstration (60-90 days)

Focus on actionable steps, specific skills to develop, and measurable outcomes. Keep it under 150 words."""

        try:
            response = self.llm_client.generate(prompt, max_tokens=250)
            return response.strip()
        except Exception as e:
            logger.warning(f"LLM development plan failed: {e}")
            
            # Fallback development plan
            skill_gaps = set(role.get('key_skills', [])) - set(employee.get('skills', []))
            plan = f"""90-Day Development Plan:

Month 1 (Days 1-30):
- Shadow current {role.get('title', 'role')} holders
- Complete orientation to {role.get('job_family', 'the team')}
- Identify skill gaps: {', '.join(list(skill_gaps)[:3])}

Month 2 (Days 31-60):
- Enroll in training for: {', '.join(list(skill_gaps)[:2])}
- Take on stretch assignments
- Build relationships with key stakeholders

Month 3 (Days 61-90):
- Lead a small project demonstrating new skills
- Prepare transition plan with manager
- Document lessons learned and create knowledge transfer materials"""
            
            return plan
    
    def batch_recommend(self, employee_profiles: List[Dict], top_k: int = 5) -> List[Dict]:
        """
        Generate recommendations for multiple employees.
        
        Args:
            employee_profiles: List of employee profile dictionaries
            top_k: Number of recommendations per employee
            
        Returns:
            List of recommendation results for each employee
        """
        results = []
        total = len(employee_profiles)
        
        logger.info(f"Generating recommendations for {total} employees...")
        
        for idx, employee in enumerate(employee_profiles, 1):
            employee_id = employee.get('employee_id', f'employee_{idx}')
            employee_name = employee.get('name', 'Unknown')
            
            logger.info(f"Processing {idx}/{total}: {employee_name} ({employee_id})")
            
            result = self.recommend_pathways(employee, top_k=top_k)
            results.append(result)
            
        logger.info(f"Completed recommendations for {total} employees")
        return results
    
    def evaluate_recommendations(self, recommendations: List[Dict]) -> Dict:
        """
        Evaluate the quality of recommendations across multiple employees.
        
        Args:
            recommendations: List of recommendation results
            
        Returns:
            Dictionary containing evaluation metrics
        """
        metrics = {
            'total_employees': len(recommendations),
            'successful_recommendations': 0,
            'failed_recommendations': 0,
            'total_eligible_now': 0,
            'total_future_opportunities': 0,
            'average_similarity_score': 0.0,
            'employees_with_pathways': 0,
            'employees_without_pathways': 0,
            'coverage_rate': 0.0,
            'success_rate': 0.0,
            'unique_roles_recommended': 0
        }
        
        similarity_scores = []
        unique_roles = set()
        
        for rec in recommendations:
            if 'error' in rec:
                metrics['failed_recommendations'] += 1
                continue
            
            metrics['successful_recommendations'] += 1
            
            # Count recommendations
            eligible_now = rec.get('recommendations', {}).get('eligible_now', [])
            future_opps = rec.get('recommendations', {}).get('future_opportunities', [])
            
            metrics['total_eligible_now'] += len(eligible_now)
            metrics['total_future_opportunities'] += len(future_opps)
            
            # Collect similarity scores and unique roles
            for item in eligible_now + future_opps:
                if 'similarity_score' in item:
                    similarity_scores.append(item['similarity_score'])
                if 'role' in item:
                    role_title = item['role'].get('title', '')
                    if role_title:
                        unique_roles.add(role_title)
            
            # Check if employee has any pathways
            if eligible_now or future_opps:
                metrics['employees_with_pathways'] += 1
            else:
                metrics['employees_without_pathways'] += 1
        
        # Calculate averages
        if similarity_scores:
            metrics['average_similarity_score'] = sum(similarity_scores) / len(similarity_scores)
        
        if metrics['total_employees'] > 0:
            metrics['coverage_rate'] = metrics['employees_with_pathways'] / metrics['total_employees']
            metrics['success_rate'] = metrics['successful_recommendations'] / metrics['total_employees']
        
        metrics['unique_roles_recommended'] = len(unique_roles)
        
        # Add summary statistics
        metrics['average_eligible_now_per_employee'] = (
            metrics['total_eligible_now'] / metrics['successful_recommendations']
            if metrics['successful_recommendations'] > 0 else 0
        )
        
        metrics['average_future_opps_per_employee'] = (
            metrics['total_future_opportunities'] / metrics['successful_recommendations']
            if metrics['successful_recommendations'] > 0 else 0
        )
        
        return metrics

def main():
    """Run career pathway recommender experiment."""
    
    # Load configuration
    config_path = Path(__file__).parent.parent.parent / 'config.json'
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    career_config = config['experiments']['career_pathway']
    career_config['llm_provider'] = config['default_experiment_config']['llm_provider']
    
    # Initialize recommender
    recommender = CareerPathwayRecommender(career_config)
    
    # Load job families
    job_families_dir = Path(__file__).parent.parent.parent / 'datasets' / 'job_families'
    job_family_files = list(job_families_dir.glob('job_family_*.json'))
    
    if not job_family_files:
        logger.error("No job family files found!")
        return
    
    recommender.load_job_families([str(f) for f in job_family_files])
    
    # Create sample employee profile for testing
    sample_employee = {
        'employee_id': 'EMP001',
        'name': 'Alex Johnson',
        'current_title': 'Software Engineer',
        'years_experience': 4,
        'skills': [
            'Python', 'JavaScript', 'React', 'Node.js', 
            'PostgreSQL', 'Docker', 'Git', 'REST APIs',
            'System Design', 'Agile Development'
        ],
        'education_level': 'Bachelor of Science in Computer Science',
        'certifications': ['AWS Certified Developer'],
        'career_interests': [
            'Technical Leadership',
            'System Architecture',
            'Team Mentoring',
            'Cloud Infrastructure'
        ],
        'strengths': [
            'Problem Solving',
            'Technical Communication',
            'Cross-team Collaboration'
        ]
    }
    
    # Generate recommendations
    logger.info("Generating career pathway recommendations...")
    result = recommender.recommend_pathways(sample_employee, top_k=3)
    
    # Save results
    output_dir = Path(__file__).parent.parent.parent / 'results' / 'career_pathway'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f'recommendations_{timestamp}.json'
    
    save_results(result, str(output_file))
    logger.info(f"Results saved to {output_file}")
    
    # Print summary
    print("\n" + "="*80)
    print("CAREER PATHWAY RECOMMENDATIONS")
    print("="*80)
    print(f"\nEmployee: {result['employee_name']} ({result['employee_id']})")
    print(f"Current Role: {result['current_title']}")
    print(f"\nTop {len(result['recommendations'])} Recommended Career Paths:\n")
    
    for i, rec in enumerate(result['recommendations'], 1):
        role = rec['role']
        print(f"{i}. {role['title']} - {role['job_family']}")
        print(f"   Match Score: {rec['similarity_score']:.2%}")
        print(f"   Experience Required: {role['years_experience']} years")
        print(f"   Salary Range: {role['salary_range']}")
        print(f"\n   Explanation:")
        print(f"   {rec['explanation'][:200]}...")
        print()


if __name__ == '__main__':
    main()
