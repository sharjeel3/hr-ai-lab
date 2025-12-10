"""
Example: HRIS Data Quality Check

This script demonstrates how to use the HRIS Data Quality Agent to:
1. Analyze employee data for quality issues
2. Generate detailed quality reports
3. Create automated cleansing scripts
4. Export results in multiple formats
"""

import os
import sys
import json
from pathlib import Path

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from experiments.hris_data_quality_agent.hris_data_quality_agent import (
    HRISDataQualityAgent,
    QualityIssueType,
    Severity
)
from scripts.utils import logger


def run_basic_quality_check():
    """Run a basic data quality check on sample HRIS data."""
    
    print("=" * 80)
    print("HRIS DATA QUALITY AGENT - BASIC EXAMPLE")
    print("=" * 80)
    print()
    
    # Configuration
    config = {
        'llm_provider': 'google',
        'llm_model': 'gemini-2.5-flash-lite',
        'required_fields': [
            'employee_id',
            'first_name',
            'last_name',
            'email',
            'department',
            'job_title',
            'manager_id',
            'hire_date',
            'employment_status'
        ]
    }
    
    # Initialize agent
    print("Initializing HRIS Data Quality Agent...")
    agent = HRISDataQualityAgent(config)
    
    # Load sample data with known quality issues
    data_path = Path(__file__).parent.parent.parent / 'datasets' / 'hris_samples' / 'employee_data_with_quality_issues.json'
    
    print(f"Loading employee data from: {data_path}")
    with open(data_path, 'r') as f:
        employee_data = json.load(f)
    
    print(f"Loaded {len(employee_data)} employee records")
    print()
    
    # Run quality analysis
    print("Running comprehensive data quality analysis...")
    print()
    report = agent.analyze_dataset(employee_data)
    
    # Display results
    print("=" * 80)
    print("QUALITY ANALYSIS RESULTS")
    print("=" * 80)
    print()
    print(f"Report ID: {report.report_id}")
    print(f"Timestamp: {report.timestamp}")
    print()
    print(f"📊 Overall Quality Score: {report.quality_score}/100")
    print()
    print(f"Total Records Analyzed: {report.total_records}")
    print(f"Records with Issues: {report.records_with_issues} ({report.records_with_issues/report.total_records*100:.1f}%)")
    print(f"Total Issues Found: {report.total_issues}")
    print()
    
    # Issues by severity
    print("-" * 80)
    print("ISSUES BY SEVERITY")
    print("-" * 80)
    severity_order = ['critical', 'high', 'medium', 'low']
    for severity in severity_order:
        count = report.issues_by_severity.get(severity, 0)
        if count > 0:
            emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}[severity]
            print(f"{emoji} {severity.upper()}: {count} issues")
    print()
    
    # Issues by type
    print("-" * 80)
    print("ISSUES BY TYPE")
    print("-" * 80)
    for issue_type, count in sorted(report.issues_by_type.items(), 
                                    key=lambda x: x[1], reverse=True):
        print(f"  • {issue_type.replace('_', ' ').title()}: {count}")
    print()
    
    # Summary
    print("-" * 80)
    print("EXECUTIVE SUMMARY")
    print("-" * 80)
    print(report.summary)
    print()
    
    # Recommendations
    print("-" * 80)
    print("RECOMMENDATIONS")
    print("-" * 80)
    for i, recommendation in enumerate(report.recommendations, 1):
        print(f"{i}. {recommendation}")
    print()
    
    # Show sample of critical issues
    critical_issues = [
        issue for issue in report.issues
        if isinstance(issue, dict) and issue.get('severity') == 'critical'
    ]
    
    if critical_issues:
        print("-" * 80)
        print("CRITICAL ISSUES (Sample)")
        print("-" * 80)
        for issue in critical_issues[:5]:  # Show first 5
            print(f"\n🔴 {issue['description']}")
            print(f"   Record: {issue['record_id']}")
            print(f"   Field: {issue['field_name']}")
            print(f"   Current: {issue['current_value']}")
            print(f"   Expected: {issue['expected_value']}")
            print(f"   📋 {issue['recommendation']}")
        
        if len(critical_issues) > 5:
            print(f"\n   ... and {len(critical_issues) - 5} more critical issues")
        print()
    
    # Show sample of auto-fixable issues
    auto_fixable = [
        issue for issue in report.issues
        if isinstance(issue, dict) and issue.get('auto_fixable', False)
    ]
    
    if auto_fixable:
        print("-" * 80)
        print(f"AUTO-FIXABLE ISSUES: {len(auto_fixable)} issues can be automatically corrected")
        print("-" * 80)
        for issue in auto_fixable[:3]:  # Show first 3
            print(f"\n✏️  {issue['description']}")
            print(f"   Record: {issue['record_id']}")
            print(f"   Fix: {issue['current_value']} → {issue['expected_value']}")
        
        if len(auto_fixable) > 3:
            print(f"\n   ... and {len(auto_fixable) - 3} more auto-fixable issues")
        print()
    
    # Export reports
    output_dir = Path(__file__).parent.parent.parent / 'results' / 'hris_data_quality'
    print("-" * 80)
    print("EXPORTING REPORTS")
    print("-" * 80)
    export_paths = agent.export_report(report, output_dir)
    
    for report_type, path in export_paths.items():
        print(f"✓ {report_type.upper()}: {path}")
    print()
    
    # Generate cleansing script
    if auto_fixable:
        print("-" * 80)
        print("GENERATING AUTOMATED CLEANSING SCRIPT")
        print("-" * 80)
        cleansing_script = agent.generate_cleansing_script(report)
        
        from datetime import datetime
        script_path = output_dir / f"cleansing_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        with open(script_path, 'w') as f:
            f.write(cleansing_script)
        
        print(f"✓ Generated cleansing script: {script_path}")
        print(f"  This script can automatically fix {len(auto_fixable)} issues")
        print()
    
    print("=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print()
    print("Next Steps:")
    print("1. Review the detailed reports in:", output_dir)
    print("2. Address CRITICAL issues immediately")
    print("3. Run the cleansing script to fix auto-fixable issues")
    print("4. Schedule regular data quality audits")
    print()
    
    return report


def run_custom_quality_check():
    """Example with custom configuration and business rules."""
    
    print("\n" + "=" * 80)
    print("CUSTOM QUALITY CHECK WITH BUSINESS RULES")
    print("=" * 80)
    print()
    
    # Custom configuration with specific business rules
    config = {
        'llm_provider': 'google',
        'llm_model': 'gemini-2.5-flash-lite',
        'required_fields': [
            'employee_id',
            'first_name',
            'last_name',
            'email',
            'department',
            'job_title',
            'employment_status'
        ],
        'business_rules': {
            'max_salary': 500000,
            'min_salary': 30000,
            'required_review_months': 12,
            'valid_departments': [
                'Engineering', 'Product', 'Sales', 'Marketing',
                'HR', 'Finance', 'Data', 'Design'
            ],
            'valid_statuses': ['Active', 'Terminated', 'On Leave']
        }
    }
    
    print("Configuration:")
    print(f"  • Required fields: {len(config['required_fields'])}")
    print(f"  • Custom business rules: {len(config['business_rules'])}")
    print()
    
    # Initialize agent with custom config
    agent = HRISDataQualityAgent(config)
    
    # Load data
    data_path = Path(__file__).parent.parent.parent / 'datasets' / 'hris_samples' / 'employee_data_with_quality_issues.json'
    with open(data_path, 'r') as f:
        employee_data = json.load(f)
    
    print(f"Analyzing {len(employee_data)} records with custom rules...")
    report = agent.analyze_dataset(employee_data)
    
    print(f"\n✓ Quality Score: {report.quality_score}/100")
    print(f"✓ Total Issues: {report.total_issues}")
    print(f"✓ Critical Issues: {report.issues_by_severity.get('critical', 0)}")
    print()
    
    return report


def demonstrate_issue_filtering():
    """Demonstrate filtering and analyzing specific types of issues."""
    
    print("\n" + "=" * 80)
    print("FILTERING ISSUES BY TYPE")
    print("=" * 80)
    print()
    
    # Run analysis
    config = {'llm_provider': 'google', 'llm_model': 'gemini-2.5-flash-lite'}
    agent = HRISDataQualityAgent(config)
    
    data_path = Path(__file__).parent.parent.parent / 'datasets' / 'hris_samples' / 'employee_data_with_quality_issues.json'
    with open(data_path, 'r') as f:
        employee_data = json.load(f)
    
    report = agent.analyze_dataset(employee_data)
    
    # Filter by issue type
    issue_types = set(
        issue.get('issue_type', '') for issue in report.issues if isinstance(issue, dict)
    )
    
    for issue_type in sorted(issue_types):
        filtered_issues = [
            issue for issue in report.issues
            if isinstance(issue, dict) and issue.get('issue_type') == issue_type
        ]
        
        print(f"\n{issue_type.replace('_', ' ').upper()}")
        print(f"  Count: {len(filtered_issues)}")
        
        if filtered_issues:
            # Show one example
            example = filtered_issues[0]
            print(f"  Example: {example['description']}")
            print(f"           {example['recommendation']}")
    
    print()


def analyze_quality_trends():
    """Example: Track quality trends over time (simulated)."""
    
    print("\n" + "=" * 80)
    print("QUALITY TRENDS ANALYSIS")
    print("=" * 80)
    print()
    
    # In a real scenario, you would compare reports from different time periods
    config = {'llm_provider': 'google', 'llm_model': 'gemini-2.5-flash-lite'}
    agent = HRISDataQualityAgent(config)
    
    data_path = Path(__file__).parent.parent.parent / 'datasets' / 'hris_samples' / 'employee_data_with_quality_issues.json'
    with open(data_path, 'r') as f:
        employee_data = json.load(f)
    
    report = agent.analyze_dataset(employee_data)
    
    print("Current Quality Metrics:")
    print(f"  • Quality Score: {report.quality_score}/100")
    print(f"  • Data Completeness: {(1 - report.issues_by_type.get('missing_data', 0) / (len(employee_data) * 10)) * 100:.1f}%")
    print(f"  • Format Consistency: {(1 - report.issues_by_type.get('inconsistent_format', 0) / len(employee_data)) * 100:.1f}%")
    print(f"  • Data Validity: {(1 - report.issues_by_type.get('invalid_data', 0) / len(employee_data)) * 100:.1f}%")
    print()
    print("💡 TIP: Run this analysis monthly to track improvements")
    print()


if __name__ == '__main__':
    """Run all examples."""
    
    try:
        # Example 1: Basic quality check
        report1 = run_basic_quality_check()
        
        # Example 2: Custom configuration
        report2 = run_custom_quality_check()
        
        # Example 3: Issue filtering
        demonstrate_issue_filtering()
        
        # Example 4: Trends analysis
        analyze_quality_trends()
        
        print("\n" + "=" * 80)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print()
        
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user")
    except Exception as e:
        logger.error(f"Error running examples: {e}")
        raise
