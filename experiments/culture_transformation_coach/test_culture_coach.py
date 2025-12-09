"""
Test suite for Culture Transformation Coach.
"""

import json
import os
from dotenv import load_dotenv
from culture_coach import CultureTransformationCoach
from generate_culture_data import CultureDataGenerator

# Load environment variables
load_dotenv()


def test_culture_analysis():
    """Test culture survey analysis."""
    
    print("\n" + "="*60)
    print("Testing Culture Survey Analysis")
    print("="*60)
    
    # Generate test data
    generator = CultureDataGenerator()
    responses = generator.generate_survey_responses(num_responses=50)
    context = generator.generate_organization_context()
    
    # Initialize coach
    coach = CultureTransformationCoach()
    
    # Run analysis
    print("\nAnalyzing survey responses...")
    analysis = coach.analyze_culture_survey(responses, context)
    
    print("\nCulture Analysis Results:")
    if analysis.get("parsed", True):
        print(json.dumps(analysis, indent=2)[:1000] + "...")
    else:
        print(analysis.get("raw_analysis", "")[:1000] + "...")
    
    return analysis


def test_transformation_plan():
    """Test transformation plan generation."""
    
    print("\n" + "="*60)
    print("Testing Transformation Plan Generation")
    print("="*60)
    
    # Sample analysis
    analysis = {
        "key_themes": ["Low innovation scores", "Communication gaps"],
        "strengths": ["Strong collaboration", "Good work-life balance"],
        "areas_for_improvement": ["Leadership transparency", "Career development"]
    }
    
    goals = [
        "Improve innovation culture",
        "Enhance leadership communication",
        "Create clear career pathways"
    ]
    
    constraints = {
        "budget": "moderate",
        "timeline": "12 months",
        "leadership_support": "high"
    }
    
    coach = CultureTransformationCoach()
    print("\nGenerating transformation plan...")
    plan = coach.generate_transformation_plan(analysis, goals, constraints)
    
    print("\nTransformation Plan:")
    if plan.get("parsed", True):
        print(json.dumps(plan, indent=2)[:1000] + "...")
    else:
        print(plan.get("raw_plan", "")[:1000] + "...")
    
    return plan


def test_coaching_guidance():
    """Test coaching guidance for specific scenarios."""
    
    print("\n" + "="*60)
    print("Testing Coaching Guidance")
    print("="*60)
    
    scenario = "Resistance to new remote work policy from middle managers"
    context = {
        "company_size": "mid_size",
        "industry": "Technology",
        "remote_policy": "3 days remote, 2 days office"
    }
    
    coach = CultureTransformationCoach()
    print("\nGenerating coaching guidance...")
    guidance = coach.provide_coaching_guidance(scenario, context)
    
    print("\nCoaching Guidance:")
    if guidance.get("parsed", True):
        print(json.dumps(guidance, indent=2)[:1000] + "...")
    else:
        print(guidance.get("raw_guidance", "")[:1000] + "...")
    
    return guidance


def test_health_assessment():
    """Test culture health assessment."""
    
    print("\n" + "="*60)
    print("Testing Culture Health Assessment")
    print("="*60)
    
    metrics = {
        "employee_engagement": 7.2,
        "retention_rate": 0.85,
        "innovation_index": 6.5,
        "collaboration_score": 8.1,
        "leadership_trust": 6.8
    }
    
    historical_data = [
        {"month": "2024-09", "employee_engagement": 7.0},
        {"month": "2024-10", "employee_engagement": 7.1},
        {"month": "2024-11", "employee_engagement": 7.2}
    ]
    
    coach = CultureTransformationCoach()
    print("\nAssessing culture health...")
    assessment = coach.assess_culture_health(metrics, historical_data)
    
    print("\nCulture Health Assessment:")
    if assessment.get("parsed", True):
        print(json.dumps(assessment, indent=2)[:1000] + "...")
    else:
        print(assessment.get("raw_assessment", "")[:1000] + "...")
    
    return assessment


def run_all_tests():
    """Run all test functions."""
    
    print("\n" + "="*60)
    print("CULTURE TRANSFORMATION COACH - TEST SUITE")
    print("="*60)
    
    results = {}
    
    # Check for API key
    if not os.environ.get("GOOGLE_API_KEY"):
        print("\n⚠️  WARNING: GOOGLE_API_KEY not set!")
        print("Please set your API key: export GOOGLE_API_KEY='your-key-here'")
        return
    
    try:
        results['analysis'] = test_culture_analysis()
    except Exception as e:
        print(f"\n❌ Culture analysis test failed: {e}")
    
    try:
        results['plan'] = test_transformation_plan()
    except Exception as e:
        print(f"\n❌ Transformation plan test failed: {e}")
    
    try:
        results['guidance'] = test_coaching_guidance()
    except Exception as e:
        print(f"\n❌ Coaching guidance test failed: {e}")
    
    try:
        results['assessment'] = test_health_assessment()
    except Exception as e:
        print(f"\n❌ Health assessment test failed: {e}")
    
    print("\n" + "="*60)
    print("All Culture Coach Tests Completed")
    print(f"Successful tests: {len(results)}/4")
    print("="*60)
    
    return results


if __name__ == "__main__":
    run_all_tests()
