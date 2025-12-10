# HRIS Data Quality Agent (Experiment G)

An AI-powered agent for comprehensive HRIS (Human Resources Information System) data quality assessment and improvement.

## Overview

The HRIS Data Quality Agent automatically detects, categorizes, and reports data quality issues in employee records and other HR data. It combines rule-based validation with AI-powered pattern recognition to identify problems and provide actionable recommendations for data cleansing.

## Key Features

### 🔍 **Comprehensive Quality Checks**
- **Missing Data Detection**: Identifies null, empty, or missing required fields
- **Format Consistency**: Detects inconsistent formatting across records (emails, phones, names, etc.)
- **Data Validation**: Validates data against expected formats and value ranges
- **Business Rule Compliance**: Checks adherence to organizational policies and rules
- **Duplicate Detection**: Identifies duplicate records and conflicting data
- **Referential Integrity**: Validates relationships between records (e.g., manager IDs)
- **Anomaly Detection**: Flags unusual patterns or outliers in the data

### 📊 **Quality Reporting**
- Quality score calculation (0-100)
- Issues categorized by type and severity
- AI-generated executive summaries
- Detailed issue-by-issue analysis
- Actionable recommendations

### 🛠️ **Automated Remediation**
- Identifies auto-fixable issues
- Generates Python scripts for automated data cleansing
- Provides manual fix recommendations for complex issues

### 📈 **Multiple Export Formats**
- Detailed JSON reports for programmatic access
- Human-readable text summaries
- CSV exports for spreadsheet analysis

## Quality Issue Types

### 1. Missing Data
Critical fields that are null, empty, or absent:
- Employee IDs, names, emails
- Department, job title assignments
- Manager relationships
- Employment status

**Severity**: CRITICAL to HIGH

### 2. Inconsistent Format
Data that doesn't follow standard patterns:
- Email addresses (mixed case, missing domains, wrong company domain)
- Phone numbers (different formats: +1-555-0000 vs 555.0000)
- Department names (Engineering vs engineering)
- Location formats (San Francisco vs San Francisco, CA)
- Name capitalization (john vs John)

**Severity**: LOW to MEDIUM

### 3. Invalid Data
Data that violates expected formats or ranges:
- Malformed email addresses
- Invalid employee ID formats
- Out-of-range performance ratings
- Negative or zero salaries
- Invalid date formats

**Severity**: MEDIUM to HIGH

### 4. Duplicate Data
Records or fields that should be unique but aren't:
- Duplicate employee IDs
- Duplicate email addresses
- Multiple active records for same person

**Severity**: CRITICAL

### 5. Referential Integrity
Broken relationships between records:
- Manager IDs that don't exist
- Department references to non-existent departments
- Invalid organizational hierarchy links

**Severity**: HIGH

### 6. Business Rule Violations
Data that violates organizational policies:
- Terminated employees with active manager assignments
- Missing performance reviews for tenured employees
- Salary ranges outside policy limits
- Missing required certifications

**Severity**: MEDIUM to HIGH

### 7. Anomalies
Unusual patterns that may indicate errors:
- Exceptionally high/low salaries for role
- Unusually long gaps in employment history
- Performance ratings far from team average

**Severity**: MEDIUM

### 8. Outdated Data
Information that hasn't been updated:
- Performance reviews overdue
- Contact information not recently verified
- Stale employment status

**Severity**: LOW to MEDIUM

## Installation & Setup

### Prerequisites
```bash
# Install required packages
pip install google-generativeai python-dotenv
```

### Environment Configuration
Create a `.env` file with your API key:
```bash
GOOGLE_API_KEY=your_api_key_here
```

## Usage

### Basic Quality Check

```python
from experiments.hris_data_quality_agent.hris_data_quality_agent import HRISDataQualityAgent
import json

# Configure the agent
config = {
    'llm_provider': 'google',
    'llm_model': 'gemini-2.5-flash-lite',
    'required_fields': [
        'employee_id', 'first_name', 'last_name', 'email',
        'department', 'job_title', 'manager_id', 'hire_date',
        'employment_status'
    ]
}

# Initialize agent
agent = HRISDataQualityAgent(config)

# Load your employee data
with open('employee_data.json', 'r') as f:
    employee_data = json.load(f)

# Run analysis
report = agent.analyze_dataset(employee_data)

# View results
print(f"Quality Score: {report.quality_score}/100")
print(f"Total Issues: {report.total_issues}")
print(f"Records Affected: {report.records_with_issues}")

# Export reports
agent.export_report(report, 'output_directory/')
```

### Running the Example

```bash
# From the project root
cd experiments/hris_data_quality_agent

# Run the comprehensive example
python example_quality_check.py
```

### Custom Business Rules

```python
config = {
    'llm_provider': 'google',
    'llm_model': 'gemini-2.5-flash-lite',
    'required_fields': ['employee_id', 'email', 'department'],
    'business_rules': {
        'max_salary': 500000,
        'min_salary': 30000,
        'required_review_months': 12,
        'valid_departments': ['Engineering', 'Product', 'Sales', 'Marketing'],
        'valid_statuses': ['Active', 'Terminated', 'On Leave']
    }
}

agent = HRISDataQualityAgent(config)
```

## Output Examples

### Quality Report Summary
```
================================================================================
HRIS DATA QUALITY REPORT
================================================================================

Report ID: QR_20251211_143022
Generated: 2025-12-11T14:30:22

Total Records: 19
Records with Issues: 15 (78.9%)
Total Issues: 45
Quality Score: 67.24/100

--------------------------------------------------------------------------------
SUMMARY
--------------------------------------------------------------------------------
Analysis of 19 employee records revealed significant data quality challenges, 
with 45 issues affecting 15 records. Critical problems include invalid employee 
IDs and duplicate entries. Format inconsistencies across emails, phone numbers, 
and department names are prevalent. Immediate attention needed for critical 
issues to ensure system stability.

--------------------------------------------------------------------------------
ISSUES BY SEVERITY
--------------------------------------------------------------------------------
  CRITICAL: 3
  HIGH: 12
  MEDIUM: 22
  LOW: 8

--------------------------------------------------------------------------------
RECOMMENDATIONS
--------------------------------------------------------------------------------
1. 🚨 CRITICAL: Address 3 critical issues immediately (duplicate IDs, 
   invalid formats, system-breaking errors)
2. ⚠️  HIGH PRIORITY: Resolve 12 high-priority issues affecting data 
   integrity and operations
3. 📋 Fill in 8 missing data fields from source HR systems
4. ✏️  Standardize 22 formatting inconsistencies to improve data quality
5. 🔗 Fix 5 referential integrity issues (invalid manager IDs)
6. 🔄 Implement automated data validation rules at data entry points
7. 📈 Schedule regular data quality audits (monthly recommended)
```

### Issue Details (CSV Export)
```csv
Issue ID,Type,Severity,Field,Record ID,Current Value,Expected Value,Description,Auto-Fixable
EMP003_last_name_missing,missing_data,high,last_name,EMP003,,Non-null value required,Required field 'last_name' is missing or null,False
EMP004_email_case,inconsistent_format,low,email,EMP004,ROBERT.TAYLOR@COMPANY.COM,robert.taylor@company.com,Email contains uppercase letters,True
EMP002_department_format,inconsistent_format,medium,department,EMP002,engineering,Engineering,Department name inconsistent,True
```

## Quality Score Calculation

The quality score (0-100) is calculated based on:

1. **Issue Penalty** (max -50 points): Based on total number of issues relative to dataset size
2. **Record Penalty** (max -50 points): Based on percentage of records affected

```python
quality_score = 100 - issue_penalty - record_penalty
```

Higher scores indicate better data quality. Scores below 70 require immediate attention.

## Automated Data Cleansing

The agent can generate Python scripts to automatically fix certain issues:

```python
# Generate cleansing script
cleansing_script = agent.generate_cleansing_script(report)

# Save and run
with open('fix_data.py', 'w') as f:
    f.write(cleansing_script)

# Then run: python fix_data.py
```

Auto-fixable issues include:
- Email case normalization
- Name capitalization
- Department name standardization
- Phone number formatting
- Status value consistency

## Integration Examples

### Scheduled Quality Audits

```python
import schedule
import time

def run_daily_audit():
    agent = HRISDataQualityAgent(config)
    data = load_from_hris_system()
    report = agent.analyze_dataset(data)
    
    if report.quality_score < 80:
        send_alert(report)
    
    agent.export_report(report, f'audits/{datetime.now():%Y%m%d}/')

# Run daily at 2 AM
schedule.every().day.at("02:00").do(run_daily_audit)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### CI/CD Pipeline Integration

```python
def validate_data_before_deploy(data_file):
    """Prevent deployment if data quality is too low."""
    agent = HRISDataQualityAgent(config)
    
    with open(data_file) as f:
        data = json.load(f)
    
    report = agent.analyze_dataset(data)
    
    # Fail build if quality score below threshold
    if report.quality_score < 90:
        raise Exception(f"Data quality score {report.quality_score} below threshold 90")
    
    # Fail if critical issues exist
    if report.issues_by_severity.get('critical', 0) > 0:
        raise Exception("Critical data quality issues detected")
    
    return True
```

### Real-time Validation

```python
def validate_employee_record(employee_dict):
    """Validate a single record before insertion."""
    agent = HRISDataQualityAgent(config)
    
    # Analyze single record
    report = agent.analyze_dataset([employee_dict])
    
    # Check for critical issues
    critical_issues = [
        issue for issue in report.issues 
        if issue.get('severity') == 'critical'
    ]
    
    if critical_issues:
        return False, [issue['description'] for issue in critical_issues]
    
    return True, []
```

## Architecture

```
HRISDataQualityAgent
├── analyze_dataset()          # Main entry point
├── Quality Checks
│   ├── _check_missing_data()
│   ├── _check_format_consistency()
│   ├── _check_data_validity()
│   ├── _check_business_rules()
│   ├── _check_duplicates()
│   └── _check_referential_integrity()
├── Reporting
│   ├── _generate_report()
│   ├── _generate_summary_with_llm()
│   └── _generate_recommendations()
├── Remediation
│   └── generate_cleansing_script()
└── Export
    └── export_report()
```

## Data Model

### QualityIssue
```python
@dataclass
class QualityIssue:
    issue_id: str                    # Unique identifier
    issue_type: QualityIssueType     # Type of issue
    severity: Severity               # Critical/High/Medium/Low
    field_name: str                  # Affected field
    record_id: str                   # Record identifier
    current_value: Any               # Current (problematic) value
    expected_value: Optional[Any]    # Expected or suggested value
    description: str                 # Human-readable description
    recommendation: str              # How to fix it
    auto_fixable: bool              # Can be automatically fixed?
```

### QualityReport
```python
@dataclass
class QualityReport:
    report_id: str                   # Report identifier
    timestamp: str                   # When generated
    total_records: int               # Dataset size
    records_with_issues: int         # Affected records
    total_issues: int                # Total issue count
    issues_by_type: Dict[str, int]   # Breakdown by type
    issues_by_severity: Dict[str, int]  # Breakdown by severity
    quality_score: float             # 0-100 score
    issues: List[QualityIssue]       # All detected issues
    summary: str                     # AI-generated summary
    recommendations: List[str]       # Action items
```

## Best Practices

### 1. Regular Audits
- Run quality checks weekly or monthly
- Track quality score trends over time
- Set up alerts for score drops

### 2. Progressive Improvement
- Start by fixing CRITICAL issues
- Move to HIGH priority issues
- Establish data entry standards to prevent new issues

### 3. Automation
- Use auto-fix scripts for routine formatting issues
- Implement validation at data entry points
- Integrate quality checks into data pipelines

### 4. Continuous Monitoring
- Add quality checks to CI/CD pipelines
- Monitor quality metrics in dashboards
- Set quality thresholds for production data

### 5. Stakeholder Communication
- Share quality reports with data owners
- Use AI-generated summaries for executives
- Track remediation progress

## Performance Considerations

- **Dataset Size**: Optimized for datasets up to 10,000 records
- **LLM Calls**: Minimal - only for summary generation and complex pattern analysis
- **Processing Time**: ~1-2 seconds per 100 records
- **Memory Usage**: Low - processes records iteratively

## Limitations

1. **AI Summaries**: Require LLM API access (can fall back to template summaries)
2. **Custom Rules**: Business rules must be explicitly configured
3. **Language**: Currently optimized for English text
4. **Context**: Cannot detect issues requiring external business context

## Future Enhancements

- [ ] Machine learning for pattern recognition
- [ ] Historical trend analysis
- [ ] Interactive web dashboard
- [ ] Integration with popular HRIS systems (Workday, BambooHR, etc.)
- [ ] Multi-language support
- [ ] Advanced anomaly detection using statistical models
- [ ] Real-time monitoring dashboard

## Contributing

When adding new quality checks:

1. Add the check method to the agent class
2. Update the `QualityIssueType` enum if needed
3. Call the check from `analyze_dataset()`
4. Update this README with examples
5. Add test cases

## License

Part of the HR AI Lab project. See main repository LICENSE for details.

## Support

For issues or questions:
1. Check the example script: `example_quality_check.py`
2. Review sample data: `datasets/hris_samples/`
3. Consult the main project documentation

## Related Experiments

- **Experiment A**: CV Screening - Uses quality data for better candidate matching
- **Experiment C**: Performance Reviews - Requires clean employee data
- **Experiment E**: Workflow Automation - Depends on data integrity
- **Experiment F**: Bias Testing - Quality issues can introduce bias

---

**Built with ❤️ as part of the HR AI Lab** | Experiment G: HRIS Data Quality Agent
