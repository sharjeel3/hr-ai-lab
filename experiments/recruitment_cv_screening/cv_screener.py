"""
CV Screening Benchmark (Experiment A)

This module implements an AI-powered CV screening system that:
1. Parses candidate CVs
2. Extracts key qualifications (skills, experience, education)
3. Matches candidates against job requirements
4. Generates screening scores with detailed explanations
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from scripts.utils import LLMClient, load_json_data, save_results, calculate_metrics, logger


class CVScreener:
    """AI-powered CV screening agent."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize CV screener.
        
        Args:
            config: Configuration dictionary with LLM settings and job requirements
        """
        self.config = config
        self.llm_client = LLMClient(
            provider=config.get('llm_provider', 'openai'),
            model=config.get('llm_model', 'gpt-4')
        )
        self.job_requirements = config.get('job_requirements', {})
        
    def extract_qualifications(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract key qualifications from CV using LLM.
        
        Args:
            cv_data: Parsed CV data
            
        Returns:
            Dictionary with extracted qualifications
        """
        prompt = f"""
You are an expert HR analyst. Extract and structure the key qualifications from this CV:

Candidate: {cv_data.get('name', 'Unknown')}
Summary: {cv_data.get('summary', '')}
Experience: {json.dumps(cv_data.get('experience', []), indent=2)}
Education: {json.dumps(cv_data.get('education', []), indent=2)}
Skills: {json.dumps(cv_data.get('skills', []), indent=2)}
Certifications: {json.dumps(cv_data.get('certifications', []), indent=2)}
Projects: {json.dumps(cv_data.get('projects', []), indent=2)}

Please extract and return a JSON object with:
1. total_years_experience: Total years of professional experience
2. technical_skills: List of technical skills
3. soft_skills: List of soft skills
4. education_level: Highest education level
5. relevant_certifications: List of relevant certifications
6. key_achievements: Top 3-5 achievements
7. leadership_experience: Years of leadership/management experience
8. domain_expertise: Areas of domain expertise

Return only valid JSON.
"""
        
        try:
            response = self.llm_client.generate(
                prompt=prompt,
                temperature=self.config.get('temperature', 0.3),
                max_tokens=self.config.get('max_tokens', 1000)
            )
            
            qualifications = json.loads(response)
            qualifications['candidate_id'] = cv_data.get('candidate_id', 'Unknown')
            qualifications['candidate_name'] = cv_data.get('name', 'Unknown')
            
            return qualifications
            
        except Exception as e:
            logger.error(f"Error extracting qualifications: {e}")
            return self._fallback_extraction(cv_data)
    
    def _fallback_extraction(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback extraction using simple parsing."""
        return {
            'candidate_id': cv_data.get('candidate_id', 'Unknown'),
            'candidate_name': cv_data.get('name', 'Unknown'),
            'total_years_experience': self._calculate_years(cv_data.get('experience', [])),
            'technical_skills': cv_data.get('skills', {}).get('technical', []),
            'soft_skills': cv_data.get('skills', {}).get('soft', []),
            'education_level': self._highest_education(cv_data.get('education', [])),
            'relevant_certifications': [cert['name'] for cert in cv_data.get('certifications', [])],
            'key_achievements': [],
            'leadership_experience': 0,
            'domain_expertise': []
        }
    
    def _calculate_years(self, experience_list: List[Dict]) -> float:
        """Calculate total years of experience."""
        total_months = 0
        for exp in experience_list:
            # Simple calculation - can be enhanced
            if 'start_date' in exp:
                total_months += 12  # Placeholder
        return round(total_months / 12, 1)
    
    def _highest_education(self, education_list: List[Dict]) -> str:
        """Determine highest education level."""
        if not education_list:
            return "Unknown"
        
        education_hierarchy = {
            'PhD': 5, 'Doctorate': 5, 'Ph.D.': 5,
            'Masters': 4, 'Master': 4, 'M.S.': 4, 'MBA': 4,
            'Bachelor': 3, 'B.S.': 3, 'B.A.': 3,
            'Associate': 2,
            'High School': 1
        }
        
        highest = "Unknown"
        highest_level = 0
        
        for edu in education_list:
            degree = edu.get('degree', '')
            for key, level in education_hierarchy.items():
                if key.lower() in degree.lower() and level > highest_level:
                    highest_level = level
                    highest = degree
        
        return highest
    
    def match_requirements(
        self, 
        qualifications: Dict[str, Any], 
        job_requirements: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Match candidate qualifications against job requirements.
        
        Args:
            qualifications: Extracted qualifications
            job_requirements: Job requirements (uses default if None)
            
        Returns:
            Dictionary with matching analysis and score
        """
        if job_requirements is None:
            job_requirements = self.job_requirements
        
        prompt = f"""
You are an expert recruiter. Evaluate this candidate against the job requirements:

CANDIDATE QUALIFICATIONS:
{json.dumps(qualifications, indent=2)}

JOB REQUIREMENTS:
{json.dumps(job_requirements, indent=2)}

Please provide a detailed matching analysis with:
1. overall_score: Overall match score (0-100)
2. category_scores: Scores for different categories (experience, skills, education, etc.)
3. strengths: List of candidate's strong matches
4. gaps: List of requirements not met or weakly met
5. recommendation: "Strong Match", "Good Match", "Possible Match", or "Weak Match"
6. reasoning: Detailed explanation of the matching and recommendation
7. interview_recommendation: Should this candidate be interviewed? (true/false)
8. key_questions: 3-5 questions to ask in interview to assess gaps

Return only valid JSON.
"""
        
        try:
            response = self.llm_client.generate(
                prompt=prompt,
                temperature=self.config.get('temperature', 0.3),
                max_tokens=self.config.get('max_tokens', 1500)
            )
            
            matching_result = json.loads(response)
            matching_result['candidate_id'] = qualifications.get('candidate_id')
            matching_result['candidate_name'] = qualifications.get('candidate_name')
            matching_result['timestamp'] = datetime.utcnow().isoformat()
            
            return matching_result
            
        except Exception as e:
            logger.error(f"Error matching requirements: {e}")
            return {
                'candidate_id': qualifications.get('candidate_id'),
                'candidate_name': qualifications.get('candidate_name'),
                'overall_score': 0,
                'recommendation': 'Error',
                'reasoning': f'Error during matching: {str(e)}',
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def screen_candidate(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete screening pipeline for a candidate.
        
        Args:
            cv_data: Raw CV data
            
        Returns:
            Complete screening result
        """
        logger.info(f"Screening candidate: {cv_data.get('name', 'Unknown')}")
        
        # Step 1: Extract qualifications
        qualifications = self.extract_qualifications(cv_data)
        
        # Step 2: Match against requirements
        matching_result = self.match_requirements(qualifications)
        
        # Combine results
        screening_result = {
            'candidate_id': cv_data.get('candidate_id'),
            'candidate_name': cv_data.get('name'),
            'qualifications': qualifications,
            'matching': matching_result,
            'screened_at': datetime.utcnow().isoformat()
        }
        
        return screening_result
    
    def screen_multiple(self, cv_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Screen multiple candidates and return ranked results.
        
        Args:
            cv_list: List of CV data
            
        Returns:
            List of screening results sorted by score
        """
        results = []
        
        for cv_data in cv_list:
            try:
                result = self.screen_candidate(cv_data)
                results.append(result)
            except Exception as e:
                logger.error(f"Error screening {cv_data.get('name', 'Unknown')}: {e}")
        
        # Sort by overall score
        results.sort(
            key=lambda x: x.get('matching', {}).get('overall_score', 0),
            reverse=True
        )
        
        return results


def load_cvs(dataset_path: str = "datasets/synthetic_cvs") -> List[Dict[str, Any]]:
    """Load all CV files from dataset."""
    cv_files = list(Path(dataset_path).glob("cv_*.json"))
    cvs = []
    
    for cv_file in cv_files:
        try:
            cv_data = load_json_data(str(cv_file))
            cvs.append(cv_data)
        except Exception as e:
            logger.error(f"Error loading {cv_file}: {e}")
    
    logger.info(f"Loaded {len(cvs)} CVs from {dataset_path}")
    return cvs


def run_cv_screening_experiment(
    config_path: str = "config.json",
    job_requirements_path: Optional[str] = None,
    output_dir: str = "results/cv_screening"
) -> Dict[str, Any]:
    """
    Run the CV screening experiment.
    
    Args:
        config_path: Path to configuration file
        job_requirements_path: Path to job requirements JSON
        output_dir: Output directory for results
        
    Returns:
        Dictionary with experiment results and metrics
    """
    logger.info("Starting CV Screening Experiment")
    
    # Load configuration
    config = load_json_data(config_path)
    cv_config = config.get('experiments', {}).get('cv_screening', {})
    
    # Load job requirements
    if job_requirements_path:
        job_requirements = load_json_data(job_requirements_path)
    else:
        # Use sample requirements
        job_requirements = {
            'title': 'Senior Software Engineer',
            'min_years_experience': 5,
            'required_skills': [
                'Python', 'JavaScript', 'React', 'REST APIs',
                'SQL', 'Git', 'Microservices'
            ],
            'preferred_skills': [
                'AWS', 'Docker', 'Kubernetes', 'CI/CD', 'System Design'
            ],
            'education': 'Bachelor\'s degree in Computer Science or related field',
            'leadership': 'Experience leading small teams or projects'
        }
    
    cv_config['job_requirements'] = job_requirements
    
    # Initialize screener
    screener = CVScreener(cv_config)
    
    # Load CVs
    cvs = load_cvs(cv_config.get('dataset', 'datasets/synthetic_cvs'))
    
    # Screen all candidates
    screening_results = screener.screen_multiple(cvs)
    
    # Calculate metrics
    scores = [r.get('matching', {}).get('overall_score', 0) for r in screening_results]
    recommendations = [r.get('matching', {}).get('recommendation', '') for r in screening_results]
    
    metrics = {
        'total_candidates': len(screening_results),
        'average_score': sum(scores) / len(scores) if scores else 0,
        'max_score': max(scores) if scores else 0,
        'min_score': min(scores) if scores else 0,
        'strong_matches': recommendations.count('Strong Match'),
        'good_matches': recommendations.count('Good Match'),
        'possible_matches': recommendations.count('Possible Match'),
        'weak_matches': recommendations.count('Weak Match'),
        'interview_recommended': sum(
            1 for r in screening_results 
            if r.get('matching', {}).get('interview_recommendation', False)
        )
    }
    
    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    
    save_results(
        screening_results,
        str(output_path / f"screening_results_{timestamp}.json")
    )
    
    save_results(
        metrics,
        str(output_path / f"screening_metrics_{timestamp}.json")
    )
    
    logger.info(f"CV Screening Experiment completed. Results saved to {output_dir}")
    logger.info(f"Metrics: {json.dumps(metrics, indent=2)}")
    
    return {
        'screening_results': screening_results,
        'metrics': metrics,
        'config': cv_config
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run CV Screening Experiment')
    parser.add_argument('--config', default='config.json', help='Config file path')
    parser.add_argument('--job-requirements', help='Job requirements JSON file')
    parser.add_argument('--output', default='results/cv_screening', help='Output directory')
    
    args = parser.parse_args()
    
    results = run_cv_screening_experiment(
        config_path=args.config,
        job_requirements_path=args.job_requirements,
        output_dir=args.output
    )
    
    print(f"\n✅ Screening complete!")
    print(f"📊 Screened {results['metrics']['total_candidates']} candidates")
    print(f"⭐ Average score: {results['metrics']['average_score']:.1f}/100")
    print(f"🎯 Recommended for interview: {results['metrics']['interview_recommended']}")
