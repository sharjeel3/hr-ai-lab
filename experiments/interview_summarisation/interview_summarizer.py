"""
Interview Summarization Agent (Experiment B)

This module implements an AI-powered interview summarization system that:
1. Processes interview transcripts
2. Identifies key competencies and skills demonstrated
3. Extracts technical and behavioral insights
4. Generates structured interview summaries and recommendations
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


class InterviewSummarizer:
    """AI-powered interview summarization agent."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize interview summarizer.
        
        Args:
            config: Configuration dictionary with LLM settings and competency rubrics
        """
        self.config = config
        self.llm_client = LLMClient(
            provider=config.get('llm_provider', 'google'),
            model=config.get('llm_model', 'gemini-2.5-flash-lite')
        )
        self.competency_rubric = config.get('competency_rubric', self._default_rubric())
    
    def _default_rubric(self) -> Dict[str, List[str]]:
        """Default competency rubric for evaluation."""
        return {
            'technical_skills': [
                'Problem solving ability',
                'System design knowledge',
                'Code quality awareness',
                'Technical depth',
                'Best practices understanding'
            ],
            'behavioral_skills': [
                'Communication skills',
                'Leadership and mentoring',
                'Collaboration',
                'Adaptability',
                'Initiative and ownership'
            ],
            'cultural_fit': [
                'Values alignment',
                'Team orientation',
                'Growth mindset',
                'Work style preferences'
            ]
        }
    
    def parse_transcript(self, interview_data: Dict[str, Any]) -> str:
        """
        Convert transcript array to readable text format.
        
        Args:
            interview_data: Interview data with transcript
            
        Returns:
            Formatted transcript text
        """
        transcript = interview_data.get('transcript', [])
        
        formatted_lines = []
        for entry in transcript:
            speaker = entry.get('speaker', 'Unknown')
            text = entry.get('text', '')
            timestamp = entry.get('timestamp', '')
            formatted_lines.append(f"[{timestamp}] {speaker}: {text}")
        
        return "\n\n".join(formatted_lines)
    
    def extract_competencies(self, interview_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract and evaluate competencies demonstrated in the interview.
        
        Args:
            interview_data: Interview data with transcript
            
        Returns:
            Dictionary with competency analysis
        """
        transcript_text = self.parse_transcript(interview_data)
        
        prompt = f"""
You are an expert technical interviewer and HR analyst conducting a RIGOROUS and DIFFERENTIATED evaluation. Your goal is to provide accurate, discriminating assessments that distinguish between candidates.

IMPORTANT: Be critical and look for concrete evidence. Most candidates should score in the 60-75 range. Only exceptional candidates with clear evidence of excellence should score 85+.

INTERVIEW METADATA:
Candidate: {interview_data.get('candidate_name', 'Unknown')}
Position: {interview_data.get('position', 'Unknown')}
Interview Type: {interview_data.get('interview_type', 'Unknown')}
Duration: {interview_data.get('duration_minutes', 0)} minutes

TRANSCRIPT:
{transcript_text}

COMPETENCY RUBRIC:
{json.dumps(self.competency_rubric, indent=2)}

SCORING CALIBRATION GUIDE:
Rating 1 (Poor): Significant gaps, unclear responses, lacks basic knowledge, red flags present
Rating 2 (Below Average): Some gaps, vague answers, limited examples, hesitant communication
Rating 3 (Average): Meets basic requirements, adequate examples, clear but not exceptional
Rating 4 (Good): Strong performance, detailed examples, clear expertise, minor gaps only
Rating 5 (Excellent): Outstanding, exceptional depth, multiple strong examples, expert-level

RED FLAGS TO WATCH FOR:
- Frequent filler words ("um", "uh", "like", "you know")
- Vague or generic answers lacking specifics
- Inability to provide concrete examples
- Contradictory statements
- Lack of ownership (always blaming others)
- Poor communication structure
- Defensive or negative attitude

Please analyze and return a JSON object with:

1. technical_competencies: For each technical skill in the rubric, provide:
   - skill_name: Name of the skill
   - evidence: Specific quotes or examples from the interview (or "None observed" if lacking)
   - rating: Score from 1-5 based on calibration guide above
   - notes: Critical evaluation including any weaknesses observed

2. behavioral_competencies: Same structure, noting communication quality and professionalism

3. cultural_fit: Same structure, noting alignment with values and work style

4. key_strengths: List 2-4 demonstrated strengths with specific evidence

5. areas_of_concern: List ALL red flags, weaknesses, or areas needing improvement

6. technical_depth: Overall technical assessment (1-5, be critical)

7. communication_quality: Assessment considering clarity, structure, filler words (1-5)

8. interview_performance: Overall performance accounting for ALL factors (1-5)

9. response_quality_score: Average quality of responses (1-5, consider specificity and depth)

10. confidence_indicators: Note signs of confidence vs hesitation

Return only valid JSON.
"""
        
        try:
            response = self.llm_client.generate(
                prompt=prompt,
                temperature=self.config.get('temperature', 0.5),
                max_tokens=self.config.get('max_tokens', 2000)
            )
            
            if not response or not response.strip():
                logger.error("Empty response from LLM for competency extraction")
                return {
                    'interview_id': interview_data.get('interview_id'),
                    'candidate_name': interview_data.get('candidate_name'),
                    'error': 'Empty response from LLM'
                }
            
            # Clean markdown code blocks if present
            import re
            cleaned_response = response.strip()
            if cleaned_response.startswith('```'):
                pattern = r'```(?:json)?\s*\n?(.*?)\n?```'
                match = re.search(pattern, cleaned_response, re.DOTALL)
                if match:
                    cleaned_response = match.group(1).strip()
            
            # Log first 200 chars of cleaned response for debugging
            logger.debug(f"Competency extraction response preview: {cleaned_response[:200]}...")
            
            competencies = json.loads(cleaned_response)
            competencies['interview_id'] = interview_data.get('interview_id')
            competencies['candidate_name'] = interview_data.get('candidate_name')
            
            return competencies
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in competency extraction: {e}")
            logger.error(f"Response was: {response[:500] if response else 'None'}")
            return {
                'interview_id': interview_data.get('interview_id'),
                'candidate_name': interview_data.get('candidate_name'),
                'error': f'Invalid JSON response: {str(e)}'
            }
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "429" in error_msg:
                logger.error("⚠️  API quota exceeded. Cannot continue processing.")
            logger.error(f"Error extracting competencies: {e}")
            return {
                'interview_id': interview_data.get('interview_id'),
                'candidate_name': interview_data.get('candidate_name'),
                'error': str(e)
            }
    
    def generate_summary(
        self, 
        interview_data: Dict[str, Any],
        competencies: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a structured interview summary.
        
        Args:
            interview_data: Original interview data
            competencies: Extracted competencies
            
        Returns:
            Structured interview summary
        """
        transcript_text = self.parse_transcript(interview_data)
        
        prompt = f"""
You are an expert recruiter creating a RIGOROUS and DIFFERENTIATED assessment. Scores should reflect true performance differences between candidates.

SCORING PHILOSOPHY:
- Be honest and critical in your assessment
- Look for concrete evidence and specific examples
- Distinguish between strong, average, and weak candidates
- Most candidates fall in 60-80 range; 85+ reserved for truly exceptional performance
- Scores below 60 indicate significant concerns

OVERALL SCORE CALIBRATION:
90-100: Exceptional - No hesitation, immediate hire, exceeds all expectations
80-89: Strong - Clear hire with minor reservations, exceeds most expectations  
70-79: Good - Solid candidate, meets expectations with some strengths
60-69: Adequate - Meets minimum bar but has notable gaps
50-59: Below Bar - Significant concerns, likely not a fit
<50: Poor - Clear rejection, fundamental issues

INTERVIEW DETAILS:
{json.dumps({
    'candidate_name': interview_data.get('candidate_name'),
    'position': interview_data.get('position'),
    'interviewer': interview_data.get('interviewer'),
    'date': interview_data.get('date'),
    'duration_minutes': interview_data.get('duration_minutes'),
    'interview_type': interview_data.get('interview_type')
}, indent=2)}

COMPETENCY ANALYSIS:
{json.dumps(competencies, indent=2)}

Please generate a comprehensive summary with:

1. executive_summary: 2-3 sentence overview of the interview and candidate

2. key_highlights: Bullet points of the most impressive aspects of the interview

3. technical_assessment: Detailed paragraph on technical capabilities

4. behavioral_assessment: Detailed paragraph on soft skills and behavioral traits

5. specific_examples: List of 3-5 notable examples or responses from the interview

6. recommendation: One of ["Strong Hire", "Hire", "Maybe", "No Hire"]

7. recommendation_reasoning: Detailed reasoning for the recommendation

8. next_steps: Suggested next steps (e.g., "Move to final round", "Technical deep-dive needed", etc.)

9. questions_for_next_round: If moving forward, 3-5 questions to explore in next interview

10. overall_score: Composite score out of 100 using this WEIGHTED FORMULA:
    - Technical Competencies (from competency analysis): 35%
    - Behavioral Competencies (from competency analysis): 25%
    - Communication Quality: 20%
    - Response Specificity & Depth: 15%
    - Cultural Fit: 5%
    
    SCORING GUIDELINES:
    - Account for red flags (filler words, vague answers, lack of examples) - deduct 5-15 points
    - Reward specific, detailed examples with metrics - add 5-10 points
    - Consider position level (junior vs senior) but maintain high standards
    - Be discriminating: avoid clustering scores around 85-95

11. confidence_level: Confidence in assessment ["High", "Medium", "Low"]
    - High: Strong evidence, consistent performance, clear signals
    - Medium: Some ambiguity, mixed signals, or limited evidence
    - Low: Significant uncertainty, contradictory signals, or very brief interview

12. score_breakdown: Show component scores used in overall_score calculation:
    - technical_score (out of 100)
    - behavioral_score (out of 100)
    - communication_score (out of 100)
    - response_quality_score (out of 100)
    - cultural_fit_score (out of 100)

Return only valid JSON.
"""
        
        try:
            response = self.llm_client.generate(
                prompt=prompt,
                temperature=self.config.get('temperature', 0.3),  # Lower temperature for more consistent scoring
                max_tokens=self.config.get('max_tokens', 3000)  # Increased for detailed breakdown
            )
            
            # Clean markdown code blocks if present
            import re
            cleaned_response = response.strip()
            if cleaned_response.startswith('```'):
                pattern = r'```(?:json)?\s*\n?(.*?)\n?```'
                match = re.search(pattern, cleaned_response, re.DOTALL)
                if match:
                    cleaned_response = match.group(1).strip()
            
            summary = json.loads(cleaned_response)
            summary['interview_id'] = interview_data.get('interview_id')
            summary['candidate_id'] = interview_data.get('candidate_id')
            summary['candidate_name'] = interview_data.get('candidate_name')
            summary['position'] = interview_data.get('position')
            summary['interview_date'] = interview_data.get('date')
            summary['summarized_at'] = datetime.now().isoformat()
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return {
                'interview_id': interview_data.get('interview_id'),
                'candidate_name': interview_data.get('candidate_name'),
                'error': str(e)
            }
    
    def validate_and_adjust_score(self, summary: Dict[str, Any], competencies: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate scoring and adjust if needed based on evidence and red flags.
        
        Args:
            summary: Generated summary with scores
            competencies: Competency analysis
            
        Returns:
            Summary with validated/adjusted scores
        """
        score = summary.get('overall_score', 0)
        recommendation = summary.get('recommendation', '')
        
        # Check for score-recommendation misalignment
        if score >= 85 and recommendation not in ['Strong Hire', 'Hire']:
            logger.warning(f"Score-recommendation mismatch: score={score}, rec={recommendation}")
            summary['overall_score'] = 75  # Adjust down
            
        if score < 65 and recommendation in ['Strong Hire', 'Hire']:
            logger.warning(f"Score-recommendation mismatch: score={score}, rec={recommendation}")
            summary['recommendation'] = 'Maybe'
            
        # Check for areas_of_concern vs high scores
        concerns = competencies.get('areas_of_concern', [])
        if len(concerns) >= 3 and score >= 85:
            logger.warning(f"High score ({score}) but {len(concerns)} areas of concern")
            summary['overall_score'] = min(score, 78)
            
        # Validate score breakdown if present
        breakdown = summary.get('score_breakdown', {})
        if breakdown:
            # Recalculate weighted score
            weights = {
                'technical_score': 0.35,
                'behavioral_score': 0.25,
                'communication_score': 0.20,
                'response_quality_score': 0.15,
                'cultural_fit_score': 0.05
            }
            
            calculated_score = sum(
                breakdown.get(key, 70) * weight 
                for key, weight in weights.items()
            )
            
            # If stated score differs significantly from calculation, log warning
            if abs(calculated_score - score) > 10:
                logger.warning(f"Score mismatch: stated={score}, calculated={calculated_score:.1f}")
                summary['overall_score'] = round(calculated_score)
                summary['score_adjusted'] = True
        
        return summary
    
    def summarize_interview(self, interview_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete summarization pipeline for an interview.
        
        Args:
            interview_data: Raw interview transcript data
            
        Returns:
            Complete interview summary with competencies
        """
        logger.info(f"Summarizing interview: {interview_data.get('interview_id', 'Unknown')}")
        
        # Step 1: Extract competencies
        competencies = self.extract_competencies(interview_data)
        
        # Step 2: Generate structured summary
        summary = self.generate_summary(interview_data, competencies)
        
        # Step 3: Validate and adjust scoring
        summary = self.validate_and_adjust_score(summary, competencies)
        
        # Combine results
        full_summary = {
            'interview_metadata': {
                'interview_id': interview_data.get('interview_id'),
                'candidate_id': interview_data.get('candidate_id'),
                'candidate_name': interview_data.get('candidate_name'),
                'position': interview_data.get('position'),
                'interviewer': interview_data.get('interviewer'),
                'date': interview_data.get('date'),
                'duration_minutes': interview_data.get('duration_minutes'),
                'interview_type': interview_data.get('interview_type')
            },
            'competency_analysis': competencies,
            'summary': summary,
            'processed_at': datetime.now().isoformat()
        }
        
        return full_summary
    
    def summarize_multiple(
        self, 
        interview_list: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Summarize multiple interviews.
        
        Args:
            interview_list: List of interview data
            
        Returns:
            List of interview summaries
        """
        summaries = []
        
        for interview_data in interview_list:
            try:
                summary = self.summarize_interview(interview_data)
                summaries.append(summary)
            except Exception as e:
                logger.error(
                    f"Error summarizing interview "
                    f"{interview_data.get('interview_id', 'Unknown')}: {e}"
                )
        
        return summaries
    
    def rank_candidates(
        self, 
        summaries: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Rank candidates based on interview summaries.
        
        Args:
            summaries: List of interview summaries
            
        Returns:
            Ranked list with scores
        """
        ranked = []
        
        for summary in summaries:
            overall_score = summary.get('summary', {}).get('overall_score', 0)
            recommendation = summary.get('summary', {}).get('recommendation', 'Unknown')
            
            ranked.append({
                'candidate_id': summary.get('interview_metadata', {}).get('candidate_id'),
                'candidate_name': summary.get('interview_metadata', {}).get('candidate_name'),
                'position': summary.get('interview_metadata', {}).get('position'),
                'overall_score': overall_score,
                'recommendation': recommendation,
                'interview_id': summary.get('interview_metadata', {}).get('interview_id')
            })
        
        # Sort by score descending
        ranked.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return ranked


def load_interviews(dataset_path: str = "datasets/interview_transcripts") -> List[Dict[str, Any]]:
    """Load all interview transcript files from dataset."""
    interview_files = list(Path(dataset_path).glob("interview_*.json"))
    interviews = []
    
    for interview_file in interview_files:
        try:
            interview_data = load_json_data(str(interview_file))
            interviews.append(interview_data)
        except Exception as e:
            logger.error(f"Error loading {interview_file}: {e}")
    
    logger.info(f"Loaded {len(interviews)} interviews from {dataset_path}")
    return interviews


def run_interview_summarization_experiment(
    config_path: str = "config.json",
    output_dir: str = "results/interview_summarization"
) -> Dict[str, Any]:
    """
    Run the interview summarization experiment.
    
    Args:
        config_path: Path to configuration file
        output_dir: Output directory for results
        
    Returns:
        Dictionary with experiment results and metrics
    """
    logger.info("Starting Interview Summarization Experiment")
    
    # Load configuration
    config = load_json_data(config_path)
    default_config = config.get('default_experiment_config', {})
    interview_config = config.get('experiments', {}).get('interview_summarisation', {})
    
    # Merge default config with interview-specific config
    merged_config = {**default_config, **interview_config}
    
    # Initialize summarizer
    summarizer = InterviewSummarizer(merged_config)
    
    # Load interviews - use merged config for dataset path
    dataset_path = merged_config.get('dataset', 'datasets/interview_transcripts')
    # Ensure full path if only directory name is provided
    if not dataset_path.startswith('datasets/'):
        dataset_path = f'datasets/{dataset_path}'
    interviews = load_interviews(dataset_path)
    
    # Summarize all interviews
    summaries = summarizer.summarize_multiple(interviews)
    
    # Rank candidates
    rankings = summarizer.rank_candidates(summaries)
    
    # Calculate metrics
    scores = [s.get('summary', {}).get('overall_score', 0) for s in summaries]
    recommendations = [s.get('summary', {}).get('recommendation', '') for s in summaries]
    
    metrics = {
        'total_interviews': len(summaries),
        'average_score': sum(scores) / len(scores) if scores else 0,
        'max_score': max(scores) if scores else 0,
        'min_score': min(scores) if scores else 0,
        'strong_hire': recommendations.count('Strong Hire'),
        'hire': recommendations.count('Hire'),
        'maybe': recommendations.count('Maybe'),
        'no_hire': recommendations.count('No Hire'),
        'average_interview_duration': sum(
            i.get('duration_minutes', 0) for i in interviews
        ) / len(interviews) if interviews else 0
    }
    
    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    save_results(
        summaries,
        str(output_path / f"interview_summaries_{timestamp}.json")
    )
    
    save_results(
        rankings,
        str(output_path / f"candidate_rankings_{timestamp}.json")
    )
    
    save_results(
        metrics,
        str(output_path / f"summarization_metrics_{timestamp}.json")
    )
    
    logger.info(f"Interview Summarization Experiment completed. Results saved to {output_dir}")
    logger.info(f"Metrics: {json.dumps(metrics, indent=2)}")
    
    # Generate dashboard
    try:
        import sys
        sys.path.append(str(Path(__file__).parent.parent.parent / "results" / "dashboards"))
        from interview_summarization_dashboard import generate_dashboard
        
        dashboard_path = generate_dashboard(
            summaries_path=str(output_path / f"interview_summaries_{timestamp}.json"),
            metrics_path=str(output_path / f"summarization_metrics_{timestamp}.json"),
            rankings_path=str(output_path / f"candidate_rankings_{timestamp}.json"),
            output_path=str(Path("results") / "dashboards" / f"interview_dashboard_{timestamp}.html")
        )
        logger.info(f"Dashboard generated: {dashboard_path}")
    except Exception as e:
        logger.warning(f"Could not generate dashboard: {e}")
    
    return {
        'summaries': summaries,
        'rankings': rankings,
        'metrics': metrics,
        'config': interview_config
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run Interview Summarization Experiment')
    parser.add_argument('--config', default='config.json', help='Config file path')
    parser.add_argument('--output', default='results/interview_summarization', help='Output directory')
    
    args = parser.parse_args()
    
    results = run_interview_summarization_experiment(
        config_path=args.config,
        output_dir=args.output
    )
    
    print(f"\n✅ Summarization complete!")
    print(f"📊 Processed {results['metrics']['total_interviews']} interviews")
    print(f"⭐ Average score: {results['metrics']['average_score']:.1f}/100")
    print(f"🎯 Strong Hire: {results['metrics']['strong_hire']}")
    print(f"✓ Hire: {results['metrics']['hire']}")
    print(f"? Maybe: {results['metrics']['maybe']}")
    print(f"✗ No Hire: {results['metrics']['no_hire']}")
