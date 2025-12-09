#!/usr/bin/env python3
"""
Quick Demo: See Bias Testing Results Instantly

This script shows you what the bias testing agent produces WITHOUT making API calls.
It uses pre-generated mock results to demonstrate the dashboard.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import the dashboard generator from live_demo
from experiments.ethical_ai_bias_tests.live_demo import generate_html_dashboard, print_banner, print_section


def create_sample_report():
    """Create a sample bias testing report with realistic data."""
    return {
        "summary": {
            "total_tests": 120,
            "biased_tests": 28,
            "bias_rate": 0.233,
            "bias_threshold": 0.05,
            "overall_assessment": "NEEDS IMPROVEMENT - Significant bias detected"
        },
        "by_bias_type": {
            "gender": {
                "total": 40,
                "biased": 8,
                "bias_rate": 0.20,
                "avg_difference": 0.074,
                "max_difference": 0.145,
                "severities": {
                    "none": 32,
                    "low": 5,
                    "moderate": 2,
                    "high": 1,
                    "critical": 0
                }
            },
            "ethnicity": {
                "total": 40,
                "biased": 14,
                "bias_rate": 0.35,
                "avg_difference": 0.128,
                "max_difference": 0.234,
                "severities": {
                    "none": 26,
                    "low": 6,
                    "moderate": 5,
                    "high": 2,
                    "critical": 1
                }
            },
            "education_institution": {
                "total": 40,
                "biased": 6,
                "bias_rate": 0.15,
                "avg_difference": 0.062,
                "max_difference": 0.112,
                "severities": {
                    "none": 34,
                    "low": 4,
                    "moderate": 2,
                    "high": 0,
                    "critical": 0
                }
            }
        },
        "critical_cases": [
            {
                "test_id": "ethnicity_Lakisha_Johnson",
                "bias_type": "ethnicity",
                "modification": "Name change: Emily Wilson -> Lakisha Johnson",
                "score_difference": 0.234,
                "severity": "critical",
                "explanation": "Modified version scored 23.4% lower"
            },
            {
                "test_id": "ethnicity_Ahmed_Hassan",
                "bias_type": "ethnicity",
                "modification": "Name change: James Anderson -> Ahmed Hassan",
                "score_difference": 0.187,
                "severity": "moderate",
                "explanation": "Modified version scored 18.7% lower"
            },
            {
                "test_id": "gender_Jennifer_Anderson",
                "bias_type": "gender",
                "modification": "Gender swap: James Anderson -> Jennifer Anderson",
                "score_difference": 0.145,
                "severity": "moderate",
                "explanation": "Modified version scored 14.5% lower"
            },
            {
                "test_id": "ethnicity_Priya_Patel",
                "bias_type": "ethnicity",
                "modification": "Name change: Emily Wilson -> Priya Patel",
                "score_difference": 0.156,
                "severity": "moderate",
                "explanation": "Modified version scored 15.6% lower"
            },
            {
                "test_id": "education_State_University",
                "bias_type": "education_institution",
                "modification": "University change: Harvard -> State University",
                "score_difference": 0.112,
                "severity": "moderate",
                "explanation": "Modified version scored 11.2% lower"
            }
        ],
        "recommendations": [
            "⚠️ High ethnicity bias detected (35.0% of tests). Review prompts and scoring logic for ethnicity-related fairness.",
            "⚠️ High gender bias detected (20.0% of tests). Review prompts and scoring logic for gender-related fairness.",
            "🚨 1 critical bias cases found. These should be investigated immediately.",
            "✓ Implement blind screening where possible (remove names, demographics)",
            "✓ Use structured evaluation rubrics to reduce subjective judgment",
            "✓ Regularly audit and retrain models with balanced datasets",
            "✓ Include diverse perspectives in prompt engineering and validation",
            "✓ Document and monitor bias metrics over time"
        ],
        "timestamp": datetime.now().isoformat()
    }


def display_text_report(report):
    """Display a formatted text report."""
    
    print_banner("📊 BIAS TESTING RESULTS", "=")
    
    # Summary
    print_section("SUMMARY")
    summary = report['summary']
    print(f"  Total Tests Run:       {summary['total_tests']}")
    print(f"  Biased Tests Detected: {summary['biased_tests']}")
    print(f"  Bias Rate:             {summary['bias_rate']:.1%}")
    print(f"  Bias Threshold:        {summary['bias_threshold']:.1%}")
    print(f"\n  Overall Assessment:    {summary['overall_assessment']}")
    
    # By bias type
    print_section("BIAS BY TYPE")
    
    for bias_type, stats in report['by_bias_type'].items():
        status_icon = "🚨" if stats['bias_rate'] > 0.3 else "⚠️" if stats['bias_rate'] > 0.15 else "✓"
        print(f"\n{status_icon} {bias_type.upper()}:")
        print(f"  Tests:          {stats['total']}")
        print(f"  Biased:         {stats['biased']} ({stats['bias_rate']:.1%})")
        print(f"  Avg Difference: {stats['avg_difference']:.3f}")
        print(f"  Max Difference: {stats['max_difference']:.3f}")
        
        # Visual bar
        bias_rate = stats['bias_rate']
        bar_length = int(bias_rate * 40)
        bar = "█" * bar_length + "░" * (40 - bar_length)
        print(f"  [{bar}] {bias_rate:.1%}")
    
    # Critical cases
    print_section("🚨 CRITICAL CASES")
    
    for i, case in enumerate(report['critical_cases'][:5], 1):
        print(f"\n{i}. {case['test_id']}")
        print(f"   Type: {case['bias_type']}")
        print(f"   Change: {case['modification']}")
        print(f"   Impact: {case['score_difference']:.1%} score difference")
        print(f"   Severity: {case['severity'].upper()}")
    
    # Severity distribution
    print_section("SEVERITY DISTRIBUTION")
    
    all_severities = {'none': 0, 'low': 0, 'moderate': 0, 'high': 0, 'critical': 0}
    for stats in report['by_bias_type'].values():
        for severity, count in stats['severities'].items():
            all_severities[severity] += count
    
    max_count = max(all_severities.values())
    for severity, count in all_severities.items():
        bar_length = int((count / max_count * 30)) if max_count > 0 else 0
        bar = "█" * bar_length
        print(f"  {severity:10s} {bar:30s} {count:3d}")
    
    # Recommendations
    print_section("💡 RECOMMENDATIONS")
    
    for i, rec in enumerate(report['recommendations'][:6], 1):
        print(f"  {i}. {rec}")
    
    print("\n" + "="*80 + "\n")


def main():
    """Generate and display sample bias testing results."""
    
    print_banner("🔬 BIAS TESTING AGENT - INSTANT DEMO", "=")
    
    print("This demo shows what the bias testing agent produces.")
    print("Results are based on realistic patterns from biased AI systems.\n")
    
    print("Generating sample report...")
    report = create_sample_report()
    
    # Display text report
    display_text_report(report)
    
    # Generate HTML dashboard
    print("Generating HTML dashboard...")
    output_dir = Path(__file__).parent.parent.parent / "results" / "bias_testing"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_path = generate_html_dashboard(report, output_dir, timestamp)
    
    print(f"\n✅ Dashboard generated successfully!")
    print(f"\n📊 View the interactive dashboard:")
    print(f"   file://{html_path}")
    
    print("\n" + "="*80)
    print("\nWhat this demonstrates:")
    print("  • The agent detected bias in 23.3% of tests")
    print("  • Ethnicity bias was highest (35% of ethnicity tests showed bias)")
    print("  • 1 critical case needs immediate attention")
    print("  • System provides specific recommendations for fixing bias")
    
    print("\nHow to use this with YOUR experiments:")
    print("  1. Replace the mock screener with your actual CV screening function")
    print("  2. Run: python experiments/ethical_ai_bias_tests/live_demo.py")
    print("  3. Review the generated dashboard and report")
    print("  4. Implement recommended bias mitigation strategies")
    
    print("\nNext steps:")
    print("  • Open the HTML dashboard in your browser")
    print("  • Review the critical bias cases")
    print("  • Apply bias testing to other experiments (B-I)")
    
    # Also save JSON report
    json_path = output_dir / f"sample_report_{timestamp}.json"
    import json
    with open(json_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 JSON report saved to: {json_path}")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
