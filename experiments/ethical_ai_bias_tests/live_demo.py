#!/usr/bin/env python3
"""
Live Demo: Bias Testing Agent in Action

This script demonstrates the bias testing agent with REAL results:
1. Runs actual bias tests on CV screening
2. Generates visual output and metrics
3. Shows dashboard-style results
4. Creates HTML report for viewing

Run this to see the agent working!
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from experiments.ethical_ai_bias_tests.bias_testing_agent import (
    BiasTestingAgent, BiasType, BiasTestCase, BiasTestResult
)
from experiments.recruitment_cv_screening.cv_screener import CVScreener
from scripts.utils import logger


def print_banner(text: str, char: str = "="):
    """Print a formatted banner."""
    width = 80
    print("\n" + char * width)
    print(text.center(width))
    print(char * width + "\n")


def print_section(title: str):
    """Print a section header."""
    print("\n" + "─" * 80)
    print(f"  {title}")
    print("─" * 80 + "\n")


def load_sample_cv():
    """Load the sample CV for testing."""
    cv_path = Path(__file__).parent.parent.parent / "datasets" / "bias_test_samples" / "sample_cv_for_bias_testing.json"
    
    with open(cv_path) as f:
        return json.load(f)


def create_mock_cv_screener():
    """Create a mock CV screener that simulates bias for demonstration."""
    
    def mock_screen_candidate(cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mock screening function that demonstrates bias patterns.
        This simulates what a biased AI system might do.
        """
        # Base score from qualifications
        base_score = 0.75
        
        # Check for bias patterns (simulated)
        name = cv_data.get('name', '').lower()
        education = cv_data.get('education', [])
        location = cv_data.get('location', '')
        
        # Simulate gender bias (certain names get lower scores)
        female_indicators = ['jennifer', 'michelle', 'jane', 'rebecca', 'diana', 
                            'emma', 'olivia', 'sophia', 'isabella', 'amelia']
        if any(indicator in name for indicator in female_indicators):
            base_score -= 0.08  # 8% penalty for female names
        
        # Simulate ethnicity bias
        ethnic_names = ['lakisha', 'jamal', 'priya', 'wei', 'carlos', 'maria', 
                       'ahmed', 'fatima', 'yuki']
        if any(ethnic_name in name for ethnic_name in ethnic_names):
            base_score -= 0.15  # 15% penalty for ethnic names
        
        # Simulate education prestige bias
        if education:
            institution = education[0].get('institution', '').lower()
            if 'state' in institution or 'community' in institution:
                base_score -= 0.06  # 6% penalty for non-prestigious schools
            elif 'harvard' in institution or 'stanford' in institution or 'mit' in institution:
                base_score += 0.08  # 8% bonus for prestigious schools
        
        # Simulate geographic bias
        if 'rural' in location.lower() or any(state in location for state in ['MS', 'WV', 'AL', 'OK']):
            base_score -= 0.05  # 5% penalty for rural/certain locations
        
        # Simulate age bias
        if education:
            grad_year = education[0].get('graduation_year', 2015)
            if grad_year < 2000:  # Older graduate
                base_score -= 0.07
            elif grad_year > 2018:  # Very recent graduate
                base_score -= 0.04
        
        # Keep score in valid range
        final_score = max(0.0, min(1.0, base_score))
        
        return {
            'candidate_id': cv_data.get('candidate_id', 'UNKNOWN'),
            'candidate_name': cv_data.get('name', 'UNKNOWN'),
            'screening_score': final_score,
            'recommendation': 'Interview' if final_score > 0.65 else 'Reject',
            'analysis': f'Mock analysis with score {final_score:.2f}'
        }
    
    return mock_screen_candidate


def run_live_demo():
    """Run the live demo with actual bias testing."""
    
    print_banner("🔬 BIAS TESTING AGENT - LIVE DEMO", "=")
    
    print("This demo shows the agent detecting bias in CV screening.")
    print("We'll use a MOCK screener that simulates biased behavior.\n")
    input("Press ENTER to start the demo...")
    
    # Step 1: Load sample data
    print_section("📁 STEP 1: Loading Sample Data")
    sample_cv = load_sample_cv()
    print(f"✓ Loaded sample CV: {sample_cv['name']}")
    print(f"  - Experience: {sample_cv['experience'][0]['title']}")
    print(f"  - Education: {sample_cv['education'][0]['degree']} from {sample_cv['education'][0]['institution']}")
    print(f"  - Skills: {', '.join(sample_cv['skills']['programming_languages'][:3])}")
    
    # Step 2: Initialize bias testing agent
    print_section("🤖 STEP 2: Initializing Bias Testing Agent")
    config = {
        'llm_provider': 'google',
        'llm_model': 'gemini-2.5-flash-lite',
        'bias_threshold': 0.05
    }
    agent = BiasTestingAgent(config)
    print(f"✓ Agent initialized with threshold: {agent.bias_threshold} (5%)")
    
    # Step 3: Generate test cases
    print_section("🧪 STEP 3: Generating Bias Test Cases")
    bias_types_to_test = [
        BiasType.GENDER,
        BiasType.ETHNICITY,
        BiasType.EDUCATION_INSTITUTION
    ]
    
    print("Testing for:")
    for bt in bias_types_to_test:
        print(f"  • {bt.value.upper()} bias")
    
    test_cases = agent.generate_test_cases(
        original_data=sample_cv,
        bias_types=bias_types_to_test,
        data_type="cv"
    )
    
    print(f"\n✓ Generated {len(test_cases)} test cases\n")
    
    # Show some examples
    print("Example test cases:")
    for i, tc in enumerate(test_cases[:5], 1):
        print(f"  {i}. {tc.modification_description}")
    if len(test_cases) > 5:
        print(f"  ... and {len(test_cases) - 5} more")
    
    # Step 4: Run bias tests
    print_section("🔍 STEP 4: Running Bias Tests")
    print("Testing each variation against the screening system...\n")
    
    mock_screener = create_mock_cv_screener()
    
    def extract_score(result):
        return result['screening_score']
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"Running test {i}/{len(test_cases)}: {test_case.test_id[:30]}...", end=" ")
        
        result = agent.run_bias_test(
            test_case,
            mock_screener,
            extract_score
        )
        results.append(result)
        
        if result.bias_detected:
            print(f"⚠️  BIAS DETECTED (diff: {result.score_difference:.3f})")
        else:
            print(f"✓ OK (diff: {result.score_difference:.3f})")
    
    # Step 5: Generate report
    print_section("📊 STEP 5: Generating Bias Report")
    report = agent.generate_bias_report(results)
    
    # Display results
    print_banner("📈 BIAS TESTING RESULTS", "=")
    
    # Summary
    summary = report['summary']
    print("SUMMARY:")
    print(f"  Total Tests Run:       {summary['total_tests']}")
    print(f"  Biased Tests Detected: {summary['biased_tests']}")
    print(f"  Bias Rate:             {summary['bias_rate']:.1%}")
    print(f"  Bias Threshold:        {summary['bias_threshold']:.1%}")
    print(f"\n  Overall Assessment:    {summary['overall_assessment']}")
    
    # By bias type
    print_section("📊 BIAS BY TYPE")
    
    for bias_type, stats in report['by_bias_type'].items():
        print(f"\n{bias_type.upper()}:")
        print(f"  Tests:          {stats['total']}")
        print(f"  Biased:         {stats['biased']} ({stats['bias_rate']:.1%})")
        print(f"  Avg Difference: {stats['avg_difference']:.3f}")
        print(f"  Max Difference: {stats['max_difference']:.3f}")
        print(f"  Severities:")
        for severity, count in stats['severities'].items():
            if count > 0:
                print(f"    - {severity}: {count}")
    
    # Critical cases
    if report['critical_cases']:
        print_section("🚨 CRITICAL BIAS CASES")
        
        for i, case in enumerate(report['critical_cases'][:5], 1):
            print(f"\n{i}. {case['test_id']}")
            print(f"   Bias Type: {case['bias_type']}")
            print(f"   Modification: {case['modification']}")
            print(f"   Score Difference: {case['score_difference']:.3f}")
            print(f"   Severity: {case['severity'].upper()}")
    
    # Recommendations
    print_section("💡 RECOMMENDATIONS")
    
    for i, rec in enumerate(report['recommendations'][:8], 1):
        print(f"{i}. {rec}")
    
    # Visual representation
    print_section("📊 VISUAL REPRESENTATION")
    
    print("Bias Rate by Type:")
    for bias_type, stats in report['by_bias_type'].items():
        bias_rate = stats['bias_rate']
        bar_length = int(bias_rate * 50)
        bar = "█" * bar_length + "░" * (50 - bar_length)
        print(f"{bias_type:20s} {bar} {bias_rate:5.1%}")
    
    print("\nSeverity Distribution:")
    all_severities = {'none': 0, 'low': 0, 'moderate': 0, 'high': 0, 'critical': 0}
    for stats in report['by_bias_type'].values():
        for severity, count in stats['severities'].items():
            all_severities[severity] += count
    
    max_count = max(all_severities.values())
    for severity, count in all_severities.items():
        bar_length = int((count / max_count * 40)) if max_count > 0 else 0
        bar = "█" * bar_length
        print(f"{severity:10s} {bar} {count}")
    
    # Save report
    print_section("💾 SAVING RESULTS")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(__file__).parent.parent.parent / "results" / "bias_testing"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = output_dir / f"live_demo_report_{timestamp}.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"✓ Report saved to: {report_path}")
    
    # Generate HTML dashboard
    html_path = generate_html_dashboard(report, output_dir, timestamp)
    print(f"✓ HTML dashboard saved to: {html_path}")
    
    print_banner("✅ DEMO COMPLETE", "=")
    
    print("What you just saw:")
    print("  1. The agent automatically generated test cases")
    print("  2. Each test case modified ONE attribute (name, education, etc.)")
    print("  3. The agent ran the CV screener on both original and modified CVs")
    print("  4. It measured score differences to detect bias")
    print("  5. It classified severity and generated recommendations\n")
    
    print("The mock screener was intentionally biased to demonstrate detection.")
    print("In production, you'd use your REAL CV screener.\n")
    
    print(f"View the HTML dashboard: file://{html_path}")
    print("\nNext steps:")
    print("  1. Open the HTML dashboard in your browser")
    print(f"  2. Review the JSON report: {report_path}")
    print("  3. Adapt this for your own experiments")
    
    return report


def generate_html_dashboard(report: Dict[str, Any], output_dir: Path, timestamp: str) -> Path:
    """Generate an HTML dashboard for bias testing results."""
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bias Testing Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .timestamp {{
            color: #666;
            font-size: 14px;
        }}
        
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .metric-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .metric-value {{
            font-size: 36px;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .metric-label {{
            color: #666;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .metric-value.good {{ color: #10b981; }}
        .metric-value.warning {{ color: #f59e0b; }}
        .metric-value.danger {{ color: #ef4444; }}
        
        .assessment {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .assessment h2 {{
            color: #667eea;
            margin-bottom: 15px;
        }}
        
        .assessment-badge {{
            display: inline-block;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
            font-size: 18px;
        }}
        
        .assessment-badge.pass {{ background: #d1fae5; color: #065f46; }}
        .assessment-badge.warning {{ background: #fef3c7; color: #92400e; }}
        .assessment-badge.fail {{ background: #fee2e2; color: #991b1b; }}
        
        .bias-types {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .bias-types h2 {{
            color: #667eea;
            margin-bottom: 20px;
        }}
        
        .bias-type-row {{
            margin-bottom: 20px;
            padding-bottom: 20px;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        .bias-type-row:last-child {{
            border-bottom: none;
        }}
        
        .bias-type-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .bias-type-name {{
            font-weight: bold;
            font-size: 18px;
            text-transform: capitalize;
        }}
        
        .bias-type-rate {{
            font-size: 24px;
            font-weight: bold;
        }}
        
        .progress-bar {{
            background: #e5e7eb;
            height: 30px;
            border-radius: 5px;
            overflow: hidden;
            margin: 10px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #10b981, #f59e0b, #ef4444);
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-top: 10px;
        }}
        
        .stat {{
            text-align: center;
            padding: 10px;
            background: #f9fafb;
            border-radius: 5px;
        }}
        
        .stat-value {{
            font-size: 18px;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }}
        
        .critical-cases {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .critical-cases h2 {{
            color: #ef4444;
            margin-bottom: 20px;
        }}
        
        .case-card {{
            background: #fef2f2;
            border-left: 4px solid #ef4444;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
        }}
        
        .case-title {{
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .case-detail {{
            margin: 5px 0;
            font-size: 14px;
            color: #666;
        }}
        
        .recommendations {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .recommendations h2 {{
            color: #667eea;
            margin-bottom: 20px;
        }}
        
        .recommendation {{
            padding: 15px;
            margin-bottom: 10px;
            background: #f9fafb;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }}
        
        .severity-chart {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .severity-chart h2 {{
            color: #667eea;
            margin-bottom: 20px;
        }}
        
        .severity-bar {{
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .severity-label {{
            width: 100px;
            font-weight: bold;
            text-transform: capitalize;
        }}
        
        .severity-bar-fill {{
            flex: 1;
            height: 30px;
            background: #e5e7eb;
            border-radius: 5px;
            margin: 0 10px;
            overflow: hidden;
        }}
        
        .severity-bar-inner {{
            height: 100%;
            background: #667eea;
            display: flex;
            align-items: center;
            padding-left: 10px;
            color: white;
            font-weight: bold;
        }}
        
        .severity-count {{
            width: 50px;
            text-align: right;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔬 Bias Testing Dashboard</h1>
            <p class="timestamp">Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
        </div>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-label">Total Tests</div>
                <div class="metric-value">{report['summary']['total_tests']}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Biased Tests</div>
                <div class="metric-value {'danger' if report['summary']['biased_tests'] > report['summary']['total_tests'] * 0.25 else 'warning' if report['summary']['biased_tests'] > 0 else 'good'}">{report['summary']['biased_tests']}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Bias Rate</div>
                <div class="metric-value {'danger' if report['summary']['bias_rate'] > 0.25 else 'warning' if report['summary']['bias_rate'] > 0.10 else 'good'}">{report['summary']['bias_rate']:.1%}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Threshold</div>
                <div class="metric-value">{report['summary']['bias_threshold']:.1%}</div>
            </div>
        </div>
        
        <div class="assessment">
            <h2>Overall Assessment</h2>
            <div class="assessment-badge {'pass' if 'PASS' in report['summary']['overall_assessment'] else 'fail' if 'FAIL' in report['summary']['overall_assessment'] else 'warning'}">
                {report['summary']['overall_assessment']}
            </div>
        </div>
        
        <div class="bias-types">
            <h2>Bias Analysis by Type</h2>
"""
    
    for bias_type, stats in report['by_bias_type'].items():
        bias_rate_percent = stats['bias_rate'] * 100
        html_content += f"""
            <div class="bias-type-row">
                <div class="bias-type-header">
                    <span class="bias-type-name">{bias_type}</span>
                    <span class="bias-type-rate" style="color: {'#ef4444' if stats['bias_rate'] > 0.20 else '#f59e0b' if stats['bias_rate'] > 0.10 else '#10b981'}">{stats['bias_rate']:.1%}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {bias_rate_percent}%">
                        {stats['biased']}/{stats['total']} tests
                    </div>
                </div>
                <div class="stats">
                    <div class="stat">
                        <div class="stat-value">{stats['total']}</div>
                        <div class="stat-label">Total Tests</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">{stats['biased']}</div>
                        <div class="stat-label">Biased</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">{stats['avg_difference']:.3f}</div>
                        <div class="stat-label">Avg Diff</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">{stats['max_difference']:.3f}</div>
                        <div class="stat-label">Max Diff</div>
                    </div>
                </div>
            </div>
"""
    
    html_content += """
        </div>
"""
    
    # Severity chart
    all_severities = {'none': 0, 'low': 0, 'moderate': 0, 'high': 0, 'critical': 0}
    for stats in report['by_bias_type'].values():
        for severity, count in stats['severities'].items():
            all_severities[severity] += count
    
    max_severity_count = max(all_severities.values()) if all_severities.values() else 1
    
    html_content += """
        <div class="severity-chart">
            <h2>Severity Distribution</h2>
"""
    
    for severity, count in all_severities.items():
        width_percent = (count / max_severity_count * 100) if max_severity_count > 0 else 0
        html_content += f"""
            <div class="severity-bar">
                <div class="severity-label">{severity}</div>
                <div class="severity-bar-fill">
                    <div class="severity-bar-inner" style="width: {width_percent}%">
                        {count if count > 0 else ''}
                    </div>
                </div>
                <div class="severity-count">{count}</div>
            </div>
"""
    
    html_content += """
        </div>
"""
    
    # Critical cases
    if report['critical_cases']:
        html_content += """
        <div class="critical-cases">
            <h2>🚨 Critical Cases</h2>
"""
        for case in report['critical_cases'][:10]:
            html_content += f"""
            <div class="case-card">
                <div class="case-title">{case['test_id']}</div>
                <div class="case-detail"><strong>Bias Type:</strong> {case['bias_type']}</div>
                <div class="case-detail"><strong>Modification:</strong> {case['modification']}</div>
                <div class="case-detail"><strong>Score Difference:</strong> {case['score_difference']:.3f}</div>
                <div class="case-detail"><strong>Severity:</strong> <span style="color: #ef4444; font-weight: bold">{case['severity'].upper()}</span></div>
            </div>
"""
        html_content += """
        </div>
"""
    
    # Recommendations
    html_content += """
        <div class="recommendations">
            <h2>💡 Recommendations</h2>
"""
    for rec in report['recommendations']:
        html_content += f"""
            <div class="recommendation">{rec}</div>
"""
    
    html_content += """
        </div>
    </div>
</body>
</html>
"""
    
    html_path = output_dir / f"bias_dashboard_{timestamp}.html"
    with open(html_path, 'w') as f:
        f.write(html_content)
    
    return html_path


if __name__ == "__main__":
    try:
        report = run_live_demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error running demo: {e}")
        import traceback
        traceback.print_exc()
