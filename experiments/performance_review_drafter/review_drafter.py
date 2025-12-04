"""
Performance Review Auto-Draft (Experiment C)

This module implements an AI-powered performance review drafting system that:
1. Consolidates performance notes and observations
2. Analyzes employee achievements and growth areas
3. Generates balanced performance reviews
4. Formats reviews according to organizational templates
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from scripts.utils import LLMClient, load_json_data, save_results, logger


class PerformanceReviewDrafter:
    """AI-powered performance review drafting agent."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize performance review drafter.
        
        Args:
            config: Configuration dictionary with LLM settings and review templates
        """
        self.config = config
        self.llm_client = LLMClient(
            provider=config.get('llm_provider', 'openai'),
            model=config.get('llm_model', 'gpt-4')
        )
        self.review_template = config.get('review_template', self._default_template())
    
    def _default_template(self) -> Dict[str, Any]:
        """Default performance review template."""
        return {
            'sections': [
                'Executive Summary',
                'Key Achievements',
                'Technical/Functional Skills',
                'Leadership & Collaboration',
                'Areas for Development',
                'Goal Achievement',
                'Overall Rating',
                'Recommended Actions'
            ],
            'rating_scale': {
                '5': 'Outstanding - Consistently exceeds expectations',
                '4': 'Exceeds Expectations - Regularly delivers beyond requirements',
                '3': 'Meets Expectations - Solid performer meeting all requirements',
                '2': 'Needs Improvement - Performance below expectations',
                '1': 'Unsatisfactory - Significant performance concerns'
            }
        }
    
    def analyze_notes(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze performance notes to extract key themes and patterns.
        
        Args:
            performance_data: Performance note data
            
        Returns:
            Dictionary with analyzed themes and patterns
        """
        notes = performance_data.get('notes', [])
        notes_text = json.dumps(notes, indent=2)
        
        prompt = f"""
You are an expert HR manager analyzing performance notes for an employee review.

EMPLOYEE: {performance_data.get('employee_name', 'Unknown')}
POSITION: {performance_data.get('position', 'Unknown')}
REVIEW PERIOD: {performance_data.get('review_period', 'Unknown')}
MANAGER: {performance_data.get('manager', 'Unknown')}

PERFORMANCE NOTES:
{notes_text}

GOALS PROGRESS:
{json.dumps(performance_data.get('goals_progress', {}), indent=2)}

Please analyze these notes and return a JSON object with:

1. key_achievements: List of 5-7 most significant achievements with:
   - achievement: Description of the achievement
   - impact: Business impact or value created
   - category: Type (Technical, Leadership, Process, Collaboration, etc.)
   - date: When it occurred

2. technical_competencies: Assessment of technical/functional skills:
   - strengths: List of demonstrated strengths
   - skill_level: Overall technical proficiency
   - examples: Specific examples from notes

3. soft_skills: Assessment of behavioral competencies:
   - communication: Rating and examples
   - collaboration: Rating and examples
   - leadership: Rating and examples
   - initiative: Rating and examples
   - problem_solving: Rating and examples

4. development_areas: List of 2-4 areas for growth:
   - area: What needs development
   - importance: Why it matters
   - suggestions: Specific actions to improve
   - examples: Examples from notes if applicable

5. goal_analysis: For each goal:
   - goal_name: The goal
   - achievement_level: Percentage or status
   - quality_assessment: How well it was achieved
   - notes: Key observations

6. patterns_observed: Overall patterns or themes across the review period

7. trajectory: Career trajectory assessment (Upward, Stable, Concerning)

Return only valid JSON.
"""
        
        try:
            response = self.llm_client.generate(
                prompt=prompt,
                temperature=self.config.get('temperature', 0.5),
                max_tokens=self.config.get('max_tokens', 2500)
            )
            
            analysis = json.loads(response)
            analysis['employee_id'] = performance_data.get('employee_id')
            analysis['employee_name'] = performance_data.get('employee_name')
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing notes: {e}")
            return {
                'employee_id': performance_data.get('employee_id'),
                'employee_name': performance_data.get('employee_name'),
                'error': str(e)
            }
    
    def draft_review(
        self, 
        performance_data: Dict[str, Any],
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Draft a comprehensive performance review.
        
        Args:
            performance_data: Original performance data
            analysis: Analyzed notes and themes
            
        Returns:
            Complete performance review draft
        """
        prompt = f"""
You are an experienced HR manager drafting a performance review. Create a comprehensive, 
balanced, and professionally written review.

EMPLOYEE INFORMATION:
{json.dumps({
    'employee_name': performance_data.get('employee_name'),
    'employee_id': performance_data.get('employee_id'),
    'position': performance_data.get('position'),
    'manager': performance_data.get('manager'),
    'review_period': performance_data.get('review_period')
}, indent=2)}

PERFORMANCE ANALYSIS:
{json.dumps(analysis, indent=2)}

REVIEW TEMPLATE:
{json.dumps(self.review_template, indent=2)}

Please draft a complete performance review with these sections:

1. executive_summary: 3-4 sentence overview of performance and key highlights

2. key_achievements: Well-written paragraph highlighting top achievements with specific 
   examples and their business impact. Make it compelling and recognition-worthy.

3. technical_skills_assessment: Detailed paragraph on technical/functional capabilities, 
   expertise areas, and skill development. Include specific examples.

4. leadership_collaboration: Paragraph on soft skills, teamwork, communication, and 
   leadership qualities (if applicable). Use concrete examples.

5. development_areas: Constructive, supportive paragraph on growth opportunities. Frame 
   positively while being honest. Include specific, actionable suggestions.

6. goal_achievement_summary: Paragraph reviewing progress on stated goals, what was 
   achieved, and quality of execution.

7. overall_rating: Numerical rating (1-5) with the rating scale definition

8. overall_rating_justification: Clear explanation of why this rating was given

9. promotion_readiness: Assessment of readiness for promotion or increased responsibility
   (options: "Ready Now", "Ready in 6-12 months", "Developing", "Not at this time")

10. promotion_justification: Reasoning for promotion readiness assessment

11. recommended_next_steps: List of 3-5 specific actions for continued development:
    - action: What should be done
    - timeline: When
    - support_needed: What support/resources needed

12. manager_commitment: What the manager commits to do to support the employee

13. tone_assessment: Overall tone of review (Highly Positive, Positive, Balanced, 
    Constructive, Concerning)

Write in a professional, supportive tone. Be specific with examples. Balance recognition 
with constructive feedback. Make it feel authentic and personal, not generic.

Return only valid JSON.
"""
        
        try:
            response = self.llm_client.generate(
                prompt=prompt,
                temperature=self.config.get('temperature', 0.5),
                max_tokens=self.config.get('max_tokens', 3000)
            )
            
            review = json.loads(response)
            review['employee_id'] = performance_data.get('employee_id')
            review['employee_name'] = performance_data.get('employee_name')
            review['position'] = performance_data.get('position')
            review['manager'] = performance_data.get('manager')
            review['review_period'] = performance_data.get('review_period')
            review['drafted_at'] = datetime.utcnow().isoformat()
            
            return review
            
        except Exception as e:
            logger.error(f"Error drafting review: {e}")
            return {
                'employee_id': performance_data.get('employee_id'),
                'employee_name': performance_data.get('employee_name'),
                'error': str(e)
            }
    
    def format_review_document(self, review: Dict[str, Any]) -> str:
        """
        Format review as readable document.
        
        Args:
            review: Review data
            
        Returns:
            Formatted review text
        """
        doc = f"""
{'='*80}
PERFORMANCE REVIEW
{'='*80}

Employee: {review.get('employee_name', 'Unknown')}
Employee ID: {review.get('employee_id', 'Unknown')}
Position: {review.get('position', 'Unknown')}
Manager: {review.get('manager', 'Unknown')}
Review Period: {review.get('review_period', 'Unknown')}
Date: {datetime.utcnow().strftime('%Y-%m-%d')}

{'='*80}

EXECUTIVE SUMMARY
{'-'*80}
{review.get('executive_summary', '')}

{'='*80}

KEY ACHIEVEMENTS
{'-'*80}
{review.get('key_achievements', '')}

{'='*80}

TECHNICAL/FUNCTIONAL SKILLS
{'-'*80}
{review.get('technical_skills_assessment', '')}

{'='*80}

LEADERSHIP & COLLABORATION
{'-'*80}
{review.get('leadership_collaboration', '')}

{'='*80}

AREAS FOR DEVELOPMENT
{'-'*80}
{review.get('development_areas', '')}

{'='*80}

GOAL ACHIEVEMENT
{'-'*80}
{review.get('goal_achievement_summary', '')}

{'='*80}

OVERALL RATING: {review.get('overall_rating', 'N/A')}/5
{'-'*80}
{review.get('overall_rating_justification', '')}

{'='*80}

PROMOTION READINESS: {review.get('promotion_readiness', 'N/A')}
{'-'*80}
{review.get('promotion_justification', '')}

{'='*80}

RECOMMENDED NEXT STEPS
{'-'*80}
"""
        
        for i, step in enumerate(review.get('recommended_next_steps', []), 1):
            doc += f"\n{i}. {step.get('action', '')}"
            doc += f"\n   Timeline: {step.get('timeline', '')}"
            doc += f"\n   Support Needed: {step.get('support_needed', '')}\n"
        
        doc += f"""
{'='*80}

MANAGER COMMITMENT
{'-'*80}
{review.get('manager_commitment', '')}

{'='*80}
"""
        
        return doc
    
    def draft_performance_review(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete review drafting pipeline.
        
        Args:
            performance_data: Raw performance note data
            
        Returns:
            Complete performance review
        """
        logger.info(f"Drafting review for: {performance_data.get('employee_name', 'Unknown')}")
        
        # Step 1: Analyze notes
        analysis = self.analyze_notes(performance_data)
        
        # Step 2: Draft review
        review = self.draft_review(performance_data, analysis)
        
        # Step 3: Format document
        formatted_review = self.format_review_document(review)
        
        # Combine all data
        complete_review = {
            'performance_note_id': performance_data.get('performance_note_id'),
            'employee_id': performance_data.get('employee_id'),
            'employee_name': performance_data.get('employee_name'),
            'analysis': analysis,
            'review': review,
            'formatted_document': formatted_review,
            'processed_at': datetime.utcnow().isoformat()
        }
        
        return complete_review
    
    def draft_multiple_reviews(
        self, 
        performance_data_list: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Draft multiple performance reviews.
        
        Args:
            performance_data_list: List of performance data
            
        Returns:
            List of drafted reviews
        """
        reviews = []
        
        for performance_data in performance_data_list:
            try:
                review = self.draft_performance_review(performance_data)
                reviews.append(review)
            except Exception as e:
                logger.error(
                    f"Error drafting review for "
                    f"{performance_data.get('employee_name', 'Unknown')}: {e}"
                )
        
        return reviews


def load_performance_notes(
    dataset_path: str = "datasets/performance_notes"
) -> List[Dict[str, Any]]:
    """Load all performance note files from dataset."""
    note_files = list(Path(dataset_path).glob("perf_note_*.json"))
    notes = []
    
    for note_file in note_files:
        try:
            note_data = load_json_data(str(note_file))
            notes.append(note_data)
        except Exception as e:
            logger.error(f"Error loading {note_file}: {e}")
    
    logger.info(f"Loaded {len(notes)} performance notes from {dataset_path}")
    return notes


def run_performance_review_experiment(
    config_path: str = "config.json",
    output_dir: str = "results/performance_reviews"
) -> Dict[str, Any]:
    """
    Run the performance review drafting experiment.
    
    Args:
        config_path: Path to configuration file
        output_dir: Output directory for results
        
    Returns:
        Dictionary with experiment results and metrics
    """
    logger.info("Starting Performance Review Drafting Experiment")
    
    # Load configuration
    config = load_json_data(config_path)
    review_config = config.get('experiments', {}).get('performance_review', {})
    
    # Initialize drafter
    drafter = PerformanceReviewDrafter(review_config)
    
    # Load performance notes
    performance_notes = load_performance_notes(
        review_config.get('dataset', 'datasets/performance_notes')
    )
    
    # Draft all reviews
    drafted_reviews = drafter.draft_multiple_reviews(performance_notes)
    
    # Calculate metrics
    ratings = [
        r.get('review', {}).get('overall_rating', 0) 
        for r in drafted_reviews
    ]
    
    promotion_readiness = [
        r.get('review', {}).get('promotion_readiness', '') 
        for r in drafted_reviews
    ]
    
    metrics = {
        'total_reviews': len(drafted_reviews),
        'average_rating': sum(ratings) / len(ratings) if ratings else 0,
        'max_rating': max(ratings) if ratings else 0,
        'min_rating': min(ratings) if ratings else 0,
        'rating_distribution': {
            '5_outstanding': ratings.count(5),
            '4_exceeds': ratings.count(4),
            '3_meets': ratings.count(3),
            '2_needs_improvement': ratings.count(2),
            '1_unsatisfactory': ratings.count(1)
        },
        'promotion_readiness': {
            'ready_now': promotion_readiness.count('Ready Now'),
            'ready_6_12_months': promotion_readiness.count('Ready in 6-12 months'),
            'developing': promotion_readiness.count('Developing'),
            'not_at_this_time': promotion_readiness.count('Not at this time')
        }
    }
    
    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    
    save_results(
        drafted_reviews,
        str(output_path / f"drafted_reviews_{timestamp}.json")
    )
    
    save_results(
        metrics,
        str(output_path / f"review_metrics_{timestamp}.json")
    )
    
    # Save formatted documents
    for review in drafted_reviews:
        employee_id = review.get('employee_id', 'unknown')
        doc_path = output_path / f"review_{employee_id}_{timestamp}.txt"
        with open(doc_path, 'w') as f:
            f.write(review.get('formatted_document', ''))
    
    logger.info(f"Performance Review Experiment completed. Results saved to {output_dir}")
    logger.info(f"Metrics: {json.dumps(metrics, indent=2)}")
    
    return {
        'drafted_reviews': drafted_reviews,
        'metrics': metrics,
        'config': review_config
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run Performance Review Drafting Experiment')
    parser.add_argument('--config', default='config.json', help='Config file path')
    parser.add_argument('--output', default='results/performance_reviews', help='Output directory')
    
    args = parser.parse_args()
    
    results = run_performance_review_experiment(
        config_path=args.config,
        output_dir=args.output
    )
    
    print(f"\n✅ Review drafting complete!")
    print(f"📊 Drafted {results['metrics']['total_reviews']} reviews")
    print(f"⭐ Average rating: {results['metrics']['average_rating']:.1f}/5")
    print(f"\n📈 Rating Distribution:")
    for rating, count in results['metrics']['rating_distribution'].items():
        print(f"   {rating}: {count}")
    print(f"\n🎯 Promotion Readiness:")
    for status, count in results['metrics']['promotion_readiness'].items():
        print(f"   {status}: {count}")
