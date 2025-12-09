"""
Example: Using the Bias Testing Agent with CV Screening Experiment

This script demonstrates how to:
1. Load the bias testing agent
2. Test an existing experiment (CV Screening) for bias
3. Generate and interpret bias reports
4. Apply mitigation strategies
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from experiments.ethical_ai_bias_tests.bias_testing_agent import (
    BiasTestingAgent,
    BiasType,
    run_bias_analysis_on_experiment
)
from experiments.recruitment_cv_screening.cv_screener import CVScreener
from scripts.utils import load_json_data, logger


def load_sample_data():
    """Load sample CV data for bias testing."""
    # Load sample CV
    sample_cv_path = Path(__file__).parent.parent.parent / "datasets" / "bias_test_samples" / "sample_cv_for_bias_testing.json"
    
    if sample_cv_path.exists():
        with open(sample_cv_path) as f:
            sample_cv = json.load(f)
        logger.info(f"Loaded sample CV: {sample_cv['name']}")
        return [sample_cv]
    else:
        # Use synthetic data if file doesn't exist
        logger.info("Using synthetic CV data")
        return [{
            'candidate_id': 'DEMO_001',
            'name': 'Alex Johnson',
            'email': 'alex.j@email.com',
            'location': 'San Francisco, CA',
            'summary': 'Experienced software engineer with 5 years in full-stack development',
            'experience': [
                {
                    'title': 'Senior Engineer',
                    'company': 'Tech Corp',
                    'location': 'San Francisco, CA',
                    'duration_years': 3,
                    'responsibilities': [
                        'Led team of 4 engineers',
                        'Built scalable microservices',
                        'Mentored junior developers'
                    ]
                },
                {
                    'title': 'Software Engineer',
                    'company': 'StartupXYZ',
                    'location': 'San Francisco, CA',
                    'duration_years': 2,
                    'responsibilities': [
                        'Developed REST APIs',
                        'Built React applications',
                        'Wrote comprehensive tests'
                    ]
                }
            ],
            'education': [
                {
                    'degree': 'BS Computer Science',
                    'institution': 'State University',
                    'graduation_year': 2018,
                    'gpa': 3.7
                }
            ],
            'skills': {
                'programming_languages': ['Python', 'JavaScript', 'TypeScript'],
                'frameworks': ['React', 'Node.js', 'FastAPI'],
                'databases': ['PostgreSQL', 'MongoDB'],
                'cloud_platforms': ['AWS']
            },
            'certifications': [
                {
                    'name': 'AWS Certified Developer',
                    'issuer': 'Amazon Web Services',
                    'date': '2022-06'
                }
            ]
        }]


def example_1_basic_bias_testing():
    """
    Example 1: Basic bias testing on CV screening.
    Tests for gender, ethnicity, and name bias.
    """
    logger.info("\n" + "="*80)
    logger.info("EXAMPLE 1: Basic Bias Testing")
    logger.info("="*80 + "\n")
    
    # Load configuration
    config_path = Path(__file__).parent.parent.parent / "config.json"
    with open(config_path) as f:
        config = json.load(f)
    
    # Setup bias testing config
    bias_config = {
        'llm_provider': config['default_experiment_config']['llm_provider'],
        'llm_model': config['default_experiment_config']['llm_model'],
        'bias_threshold': 0.05,
        'temperature': 0.3
    }
    
    # Initialize bias testing agent
    logger.info("Initializing Bias Testing Agent...")
    agent = BiasTestingAgent(bias_config)
    
    # Load sample data
    sample_cvs = load_sample_data()
    sample_cv = sample_cvs[0]
    
    # Generate test cases for different bias types
    logger.info(f"\nGenerating bias test cases for candidate: {sample_cv['name']}")
    bias_types_to_test = [BiasType.GENDER, BiasType.ETHNICITY, BiasType.NAME]
    
    test_cases = agent.generate_test_cases(
        original_data=sample_cv,
        bias_types=bias_types_to_test,
        data_type="cv"
    )
    
    logger.info(f"Generated {len(test_cases)} test cases:")
    for tc in test_cases[:5]:  # Show first 5
        logger.info(f"  - {tc.test_id}: {tc.modification_description}")
    
    logger.info("\n✅ Test cases generated successfully")
    logger.info("Next step: Run these test cases with your CV screening experiment")
    
    return agent, test_cases


def example_2_full_bias_analysis():
    """
    Example 2: Complete bias analysis with CV screening experiment.
    Runs full test suite and generates comprehensive report.
    """
    logger.info("\n" + "="*80)
    logger.info("EXAMPLE 2: Full Bias Analysis with CV Screening")
    logger.info("="*80 + "\n")
    
    # Load configuration
    config_path = Path(__file__).parent.parent.parent / "config.json"
    with open(config_path) as f:
        config = json.load(f)
    
    # Setup CV screener
    cv_config = config['experiments']['cv_screening']
    cv_config.update({
        'llm_provider': config['default_experiment_config']['llm_provider'],
        'llm_model': config['default_experiment_config']['llm_model']
    })
    
    # Job requirements for screening
    job_requirements = {
        'title': 'Senior Software Engineer',
        'required_skills': ['Python', 'JavaScript', 'AWS', 'Microservices'],
        'required_experience_years': 5,
        'preferred_skills': ['React', 'Docker', 'Kubernetes'],
        'required_education': 'Bachelor in Computer Science or related field'
    }
    cv_config['job_requirements'] = job_requirements
    
    logger.info("Initializing CV Screener...")
    cv_screener = CVScreener(cv_config)
    
    # Define experiment function
    def cv_screening_experiment(cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """Wrapper for CV screening experiment."""
        result = cv_screener.screen_candidate(cv_data, job_requirements)
        return result
    
    # Define score extractor
    def extract_cv_score(result: Dict[str, Any]) -> float:
        """Extract screening score from CV screening result."""
        return result.get('screening_score', 0.0)
    
    # Load sample data
    sample_cvs = load_sample_data()
    
    # Run full bias analysis
    logger.info("Running comprehensive bias analysis...")
    logger.info("This will test for: Gender, Ethnicity, Name, Age, and Education biases\n")
    
    bias_types = [
        BiasType.GENDER,
        BiasType.ETHNICITY,
        BiasType.NAME,
        BiasType.AGE,
        BiasType.EDUCATION_INSTITUTION
    ]
    
    report = run_bias_analysis_on_experiment(
        experiment_name="cv_screening",
        experiment_function=cv_screening_experiment,
        score_extractor=extract_cv_score,
        test_data=sample_cvs,
        bias_types=bias_types,
        config={'bias_threshold': 0.05}
    )
    
    # Display report summary
    logger.info("\n" + "="*80)
    logger.info("BIAS TESTING REPORT SUMMARY")
    logger.info("="*80 + "\n")
    
    summary = report['summary']
    logger.info(f"Total Tests Run: {summary['total_tests']}")
    logger.info(f"Biased Tests Detected: {summary['biased_tests']}")
    logger.info(f"Bias Rate: {summary['bias_rate']:.1%}")
    logger.info(f"Bias Threshold: {summary['bias_threshold']}")
    logger.info(f"\nOverall Assessment: {summary['overall_assessment']}")
    
    # Display by bias type
    logger.info("\n" + "-"*80)
    logger.info("BIAS BY TYPE")
    logger.info("-"*80 + "\n")
    
    for bias_type, stats in report['by_bias_type'].items():
        logger.info(f"{bias_type.upper()}:")
        logger.info(f"  Tests: {stats['total']}")
        logger.info(f"  Biased: {stats['biased']} ({stats['bias_rate']:.1%})")
        logger.info(f"  Avg Difference: {stats['avg_difference']:.3f}")
        logger.info(f"  Max Difference: {stats['max_difference']:.3f}")
        logger.info(f"  Severities: {stats['severities']}")
        logger.info("")
    
    # Display critical cases
    if report['critical_cases']:
        logger.info("-"*80)
        logger.info("CRITICAL CASES (Top 5)")
        logger.info("-"*80 + "\n")
        
        for case in report['critical_cases'][:5]:
            logger.info(f"Test ID: {case['test_id']}")
            logger.info(f"Bias Type: {case['bias_type']}")
            logger.info(f"Modification: {case['modification']}")
            logger.info(f"Score Difference: {case['score_difference']:.3f}")
            logger.info(f"Severity: {case['severity']}")
            logger.info("")
    
    # Display recommendations
    logger.info("-"*80)
    logger.info("RECOMMENDATIONS")
    logger.info("-"*80 + "\n")
    
    for i, rec in enumerate(report['recommendations'], 1):
        logger.info(f"{i}. {rec}")
    
    logger.info("\n" + "="*80)
    logger.info(f"Full report saved to: results/bias_testing/")
    logger.info("="*80 + "\n")
    
    return report


def example_3_custom_bias_testing():
    """
    Example 3: Custom bias testing with specific scenarios.
    Shows how to test specific bias concerns.
    """
    logger.info("\n" + "="*80)
    logger.info("EXAMPLE 3: Custom Bias Testing Scenarios")
    logger.info("="*80 + "\n")
    
    # Load configuration
    config_path = Path(__file__).parent.parent.parent / "config.json"
    with open(config_path) as f:
        config = json.load(f)
    
    bias_config = {
        'llm_provider': config['default_experiment_config']['llm_provider'],
        'llm_model': config['default_experiment_config']['llm_model'],
        'bias_threshold': 0.03,  # Stricter threshold
        'temperature': 0.1       # Lower temperature for consistency
    }
    
    logger.info("Initializing Bias Testing Agent with STRICT settings...")
    logger.info(f"  - Bias Threshold: 3% (stricter than default 5%)")
    logger.info(f"  - Temperature: 0.1 (for consistency)")
    
    agent = BiasTestingAgent(bias_config)
    
    # Load sample data
    sample_cvs = load_sample_data()
    sample_cv = sample_cvs[0]
    
    # Test only employment gap bias (common concern in hiring)
    logger.info("\nFocusing on: EMPLOYMENT GAP BIAS")
    logger.info("Testing if career gaps unfairly penalize candidates\n")
    
    test_cases = agent.generate_test_cases(
        original_data=sample_cv,
        bias_types=[BiasType.EMPLOYMENT_GAP],
        data_type="cv"
    )
    
    logger.info(f"Generated {len(test_cases)} employment gap scenarios:")
    for tc in test_cases:
        logger.info(f"  - {tc.modification_description}")
    
    logger.info("\n✅ Custom test cases ready")
    logger.info("These can be run against any experiment to test employment gap bias")
    
    return agent, test_cases


def example_4_mitigation_strategies():
    """
    Example 4: Demonstrates bias mitigation strategies.
    Shows before/after prompt engineering to reduce bias.
    """
    logger.info("\n" + "="*80)
    logger.info("EXAMPLE 4: Bias Mitigation Strategies")
    logger.info("="*80 + "\n")
    
    logger.info("STRATEGY 1: Blind Screening")
    logger.info("-" * 40)
    logger.info("""
Before: Include all candidate information
  → Name, gender, ethnicity visible to model
  → Can introduce unconscious bias

After: Remove protected attributes
  → Anonymize names (use Candidate A, B, C)
  → Remove demographic indicators
  → Focus on skills and experience only
""")
    
    logger.info("\nSTRATEGY 2: Explicit Fairness Instructions")
    logger.info("-" * 40)
    logger.info("""
Before:
  "Evaluate this candidate: {cv_data}"

After:
  "You are evaluating candidates based SOLELY on qualifications.
   Do NOT consider:
   - Gender, race, ethnicity, or age
   - University prestige or location
   - Name or cultural background
   
   Focus ONLY on:
   - Relevant skills and experience
   - Demonstrated achievements
   - Cultural/technical fit for role"
""")
    
    logger.info("\nSTRATEGY 3: Structured Rubrics")
    logger.info("-" * 40)
    logger.info("""
Before: Open-ended evaluation

After: Structured scoring rubric
  - Technical Skills: 0-10 (weight: 40%)
  - Experience: 0-10 (weight: 30%)
  - Achievements: 0-10 (weight: 20%)
  - Cultural Fit: 0-10 (weight: 10%)
  
  Final Score = Weighted Average
  
  This reduces subjective judgment and ensures consistency.
""")
    
    logger.info("\nSTRATEGY 4: Regular Bias Audits")
    logger.info("-" * 40)
    logger.info("""
Implement continuous monitoring:
  1. Run bias tests with every model update
  2. Track bias metrics over time
  3. Set up alerts for threshold violations
  4. Document all findings and actions
  5. Review quarterly with stakeholders
""")
    
    logger.info("\nSTRATEGY 5: Diverse Test Sets")
    logger.info("-" * 40)
    logger.info("""
Test with representative data:
  - Multiple demographics
  - Various career trajectories
  - Different educational backgrounds
  - Urban and rural locations
  - Range of age groups
  - Career gaps and non-linear paths
""")
    
    logger.info("\n" + "="*80)
    logger.info("✅ Mitigation strategies outlined")
    logger.info("Implement these to reduce bias in your HR AI systems")
    logger.info("="*80 + "\n")


def main():
    """Run all examples."""
    logger.info("\n" + "="*80)
    logger.info("BIAS TESTING AGENT - COMPREHENSIVE EXAMPLES")
    logger.info("="*80 + "\n")
    
    logger.info("This script demonstrates:")
    logger.info("  1. Basic bias test case generation")
    logger.info("  2. Full bias analysis with CV screening")
    logger.info("  3. Custom bias testing scenarios")
    logger.info("  4. Bias mitigation strategies")
    logger.info("\n")
    
    # Run examples
    try:
        # Example 1: Basic test case generation
        agent, test_cases = example_1_basic_bias_testing()
        
        # Example 2: Full bias analysis (this actually runs the CV screener)
        # Commented out by default as it makes API calls
        # Uncomment to run full analysis
        # report = example_2_full_bias_analysis()
        
        logger.info("\n⚠️  NOTE: Example 2 (Full Bias Analysis) is commented out by default")
        logger.info("   It makes LLM API calls which may incur costs or hit rate limits.")
        logger.info("   Uncomment in the script to run full analysis.\n")
        
        # Example 3: Custom scenarios
        agent3, test_cases3 = example_3_custom_bias_testing()
        
        # Example 4: Mitigation strategies
        example_4_mitigation_strategies()
        
        logger.info("\n" + "="*80)
        logger.info("✅ ALL EXAMPLES COMPLETED SUCCESSFULLY")
        logger.info("="*80 + "\n")
        
        logger.info("Next Steps:")
        logger.info("  1. Review the generated test cases")
        logger.info("  2. Uncomment Example 2 to run full bias analysis")
        logger.info("  3. Apply bias testing to your own experiments")
        logger.info("  4. Implement mitigation strategies as needed")
        logger.info("  5. Set up continuous bias monitoring")
        
    except Exception as e:
        logger.error(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
