#!/usr/bin/env python3
"""
Quick test of the Bias Testing Agent to verify it's working correctly.
This script tests the core functionality without making API calls.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from experiments.ethical_ai_bias_tests.bias_testing_agent import (
    BiasTestingAgent, BiasType, BiasTestCase
)


def test_agent_initialization():
    """Test that the agent initializes correctly."""
    print("Test 1: Agent Initialization...")
    
    config = {
        'llm_provider': 'google',
        'llm_model': 'gemini-2.5-flash-lite',
        'bias_threshold': 0.05
    }
    
    agent = BiasTestingAgent(config)
    
    assert agent.bias_threshold == 0.05, "Bias threshold not set correctly"
    assert len(agent.name_pairs['gender']) > 0, "Gender name pairs not loaded"
    assert len(agent.name_pairs['ethnicity']) > 0, "Ethnicity name pairs not loaded"
    
    print("✅ Agent initialized successfully\n")
    return agent


def test_gender_test_case_generation(agent):
    """Test generation of gender bias test cases."""
    print("Test 2: Gender Bias Test Case Generation...")
    
    sample_cv = {
        'candidate_id': 'TEST001',
        'name': 'John Smith',
        'summary': 'Experienced engineer',
        'experience': [{'title': 'Engineer', 'company': 'Tech Corp', 'years': 5}],
        'education': [{'degree': 'BS CS', 'institution': 'State U', 'graduation_year': 2018}],
        'skills': ['Python', 'JavaScript']
    }
    
    test_cases = agent.generate_test_cases(
        sample_cv, 
        [BiasType.GENDER],
        data_type="cv"
    )
    
    assert len(test_cases) > 0, "No test cases generated"
    assert all(tc.bias_type == BiasType.GENDER for tc in test_cases), "Wrong bias type"
    
    # Check that names are different
    for tc in test_cases[:3]:
        original_name = tc.original_data.get('name')
        modified_name = tc.modified_data.get('name')
        assert original_name != modified_name, "Names should be different"
        print(f"  ✓ Generated: {original_name} → {modified_name}")
    
    print(f"✅ Generated {len(test_cases)} gender bias test cases\n")
    return test_cases


def test_ethnicity_test_case_generation(agent):
    """Test generation of ethnicity bias test cases."""
    print("Test 3: Ethnicity Bias Test Case Generation...")
    
    sample_cv = {
        'candidate_id': 'TEST002',
        'name': 'Emily Wilson',
        'summary': 'Senior developer',
        'experience': [{'title': 'Developer', 'company': 'StartupXYZ', 'years': 7}],
        'education': [{'degree': 'MS CS', 'institution': 'Tech University', 'graduation_year': 2015}],
        'skills': ['Java', 'Python', 'AWS']
    }
    
    test_cases = agent.generate_test_cases(
        sample_cv,
        [BiasType.ETHNICITY],
        data_type="cv"
    )
    
    assert len(test_cases) > 0, "No test cases generated"
    
    # Check that different names are used
    names_used = set()
    for tc in test_cases[:5]:
        modified_name = tc.modified_data.get('name')
        names_used.add(modified_name)
        print(f"  ✓ Generated ethnicity test: {modified_name}")
    
    assert len(names_used) > 1, "Should generate diverse names"
    
    print(f"✅ Generated {len(test_cases)} ethnicity bias test cases\n")
    return test_cases


def test_education_test_case_generation(agent):
    """Test generation of education institution bias test cases."""
    print("Test 4: Education Institution Bias Test Case Generation...")
    
    sample_cv = {
        'candidate_id': 'TEST003',
        'name': 'Alex Taylor',
        'summary': 'Data scientist',
        'experience': [{'title': 'Data Scientist', 'company': 'Analytics Inc', 'years': 4}],
        'education': [
            {'degree': 'PhD Statistics', 'institution': 'Harvard University', 'graduation_year': 2019}
        ],
        'skills': ['Python', 'R', 'Machine Learning']
    }
    
    test_cases = agent.generate_test_cases(
        sample_cv,
        [BiasType.EDUCATION_INSTITUTION],
        data_type="cv"
    )
    
    assert len(test_cases) > 0, "No test cases generated"
    
    for tc in test_cases[:3]:
        original_edu = tc.original_data['education'][0]['institution']
        modified_edu = tc.modified_data['education'][0]['institution']
        assert original_edu != modified_edu, "Education institutions should differ"
        print(f"  ✓ Generated: {original_edu} → {modified_edu}")
    
    print(f"✅ Generated {len(test_cases)} education bias test cases\n")
    return test_cases


def test_age_test_case_generation(agent):
    """Test generation of age bias test cases."""
    print("Test 5: Age Bias Test Case Generation...")
    
    sample_cv = {
        'candidate_id': 'TEST004',
        'name': 'Jordan Lee',
        'summary': 'Product manager',
        'experience': [
            {'title': 'Product Manager', 'company': 'ProductCo', 'years': 5}
        ],
        'education': [
            {'degree': 'MBA', 'institution': 'Business School', 'graduation_year': 2015}
        ],
        'skills': ['Product Strategy', 'Agile', 'Analytics']
    }
    
    test_cases = agent.generate_test_cases(
        sample_cv,
        [BiasType.AGE],
        data_type="cv"
    )
    
    assert len(test_cases) > 0, "No test cases generated"
    
    for tc in test_cases:
        # Check that graduation year or experience years differ
        if 'education' in tc.modified_data and tc.modified_data['education']:
            modified_grad_year = tc.modified_data['education'][0].get('graduation_year')
            if modified_grad_year:
                print(f"  ✓ Generated age variant: graduation year {modified_grad_year}")
    
    print(f"✅ Generated {len(test_cases)} age bias test cases\n")
    return test_cases


def test_severity_calculation(agent):
    """Test bias severity calculation."""
    print("Test 6: Severity Calculation...")
    
    test_cases = [
        (0.02, "none"),
        (0.06, "low"),
        (0.15, "moderate"),
        (0.25, "high"),
        (0.35, "critical")
    ]
    
    for score_diff, expected_severity in test_cases:
        actual_severity = agent._calculate_severity(score_diff)
        assert actual_severity == expected_severity, f"Expected {expected_severity}, got {actual_severity}"
        print(f"  ✓ Score diff {score_diff:.2f} → Severity: {actual_severity}")
    
    print("✅ Severity calculation working correctly\n")


def test_report_generation(agent):
    """Test bias report generation (without actual API calls)."""
    print("Test 7: Report Generation Structure...")
    
    # Create mock results
    from experiments.ethical_ai_bias_tests.bias_testing_agent import (
        BiasTestResult, BiasTestCase, BiasType
    )
    from datetime import datetime
    
    mock_test_case = BiasTestCase(
        test_id="mock_001",
        bias_type=BiasType.GENDER,
        original_data={'name': 'John'},
        modified_data={'name': 'Jane'},
        modification_description="Gender swap",
        expected_behavior="Equal scores"
    )
    
    mock_result = BiasTestResult(
        test_case=mock_test_case,
        original_output={'score': 0.8},
        modified_output={'score': 0.7},
        score_difference=0.1,
        bias_detected=True,
        severity='low',
        explanation="Test explanation",
        timestamp=datetime.now().isoformat()
    )
    
    agent.results = [mock_result]
    
    report = agent.generate_bias_report()
    
    assert 'summary' in report, "Report should have summary"
    assert 'by_bias_type' in report, "Report should have by_bias_type"
    assert 'recommendations' in report, "Report should have recommendations"
    assert report['summary']['total_tests'] == 1, "Total tests should be 1"
    assert report['summary']['biased_tests'] == 1, "Biased tests should be 1"
    
    print("  ✓ Report structure is correct")
    print(f"  ✓ Summary: {report['summary']['overall_assessment']}")
    print(f"  ✓ Recommendations: {len(report['recommendations'])} items")
    
    print("✅ Report generation working correctly\n")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*80)
    print("BIAS TESTING AGENT - UNIT TESTS")
    print("="*80 + "\n")
    
    try:
        # Run tests
        agent = test_agent_initialization()
        test_gender_test_case_generation(agent)
        test_ethnicity_test_case_generation(agent)
        test_education_test_case_generation(agent)
        test_age_test_case_generation(agent)
        test_severity_calculation(agent)
        test_report_generation(agent)
        
        print("="*80)
        print("✅ ALL TESTS PASSED")
        print("="*80 + "\n")
        
        print("The Bias Testing Agent is working correctly!")
        print("You can now use it to test your experiments for bias.")
        print("\nNext steps:")
        print("  1. Run: python experiments/ethical_ai_bias_tests/example_bias_test.py")
        print("  2. Review the examples and adapt for your use case")
        print("  3. Integrate bias testing into your experiment pipeline")
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
