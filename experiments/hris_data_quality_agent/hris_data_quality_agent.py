"""
HRIS Data Quality Agent (Experiment G)

This module implements an AI-powered data quality agent that:
1. Detects missing, incomplete, or null data
2. Identifies inconsistent formatting across records
3. Validates data against business rules
4. Detects anomalies and suspicious patterns
5. Generates detailed quality reports with recommendations
6. Provides automated data cleansing suggestions

The agent can work with various HRIS data types including employee records,
performance data, organizational structure, and more.
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, Counter

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from scripts.utils import LLMClient, load_json_data, save_results, logger


class QualityIssueType(Enum):
    """Types of data quality issues."""
    MISSING_DATA = "missing_data"
    INCONSISTENT_FORMAT = "inconsistent_format"
    INVALID_DATA = "invalid_data"
    DUPLICATE_DATA = "duplicate_data"
    REFERENTIAL_INTEGRITY = "referential_integrity"
    BUSINESS_RULE_VIOLATION = "business_rule_violation"
    ANOMALY = "anomaly"
    OUTDATED_DATA = "outdated_data"


class Severity(Enum):
    """Severity levels for quality issues."""
    CRITICAL = "critical"  # Data is unusable or causes system errors
    HIGH = "high"  # Significant impact on analytics or operations
    MEDIUM = "medium"  # Moderate impact, should be addressed
    LOW = "low"  # Minor issues, low priority


@dataclass
class QualityIssue:
    """Represents a single data quality issue."""
    issue_id: str
    issue_type: QualityIssueType
    severity: Severity
    field_name: str
    record_id: str
    current_value: Any
    expected_value: Optional[Any]
    description: str
    recommendation: str
    auto_fixable: bool


@dataclass
class QualityReport:
    """Comprehensive data quality report."""
    report_id: str
    timestamp: str
    total_records: int
    records_with_issues: int
    total_issues: int
    issues_by_type: Dict[str, int]
    issues_by_severity: Dict[str, int]
    quality_score: float
    issues: List[QualityIssue]
    summary: str
    recommendations: List[str]


class HRISDataQualityAgent:
    """
    AI-powered agent for HRIS data quality assessment and improvement.
    
    This agent can:
    - Detect various types of data quality issues
    - Validate data against business rules
    - Generate comprehensive quality reports
    - Provide automated cleansing suggestions
    - Learn data patterns for anomaly detection
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize HRIS data quality agent.
        
        Args:
            config: Configuration dictionary with quality checking parameters
        """
        self.config = config
        self.llm_client = LLMClient(
            provider=config.get('llm_provider', 'google'),
            model=config.get('llm_model', 'gemini-2.5-flash-lite')
        )
        self.required_fields = config.get('required_fields', [])
        self.business_rules = config.get('business_rules', {})
        self.issues: List[QualityIssue] = []
        
    def analyze_dataset(self, data: List[Dict[str, Any]]) -> QualityReport:
        """
        Analyze a complete dataset for quality issues.
        
        Args:
            data: List of employee records or other HRIS data
            
        Returns:
            Comprehensive quality report
        """
        logger.info(f"Analyzing dataset with {len(data)} records...")
        
        self.issues = []
        records_with_issues = set()
        
        # Run all quality checks
        for record in data:
            record_id = record.get('employee_id', 'Unknown')
            
            # 1. Check for missing data
            self._check_missing_data(record, record_id, records_with_issues)
            
            # 2. Check formatting consistency
            self._check_format_consistency(record, record_id, records_with_issues, data)
            
            # 3. Validate data values
            self._check_data_validity(record, record_id, records_with_issues)
            
            # 4. Check business rules
            self._check_business_rules(record, record_id, records_with_issues)
        
        # 5. Check for duplicates across dataset
        self._check_duplicates(data, records_with_issues)
        
        # 6. Check referential integrity
        self._check_referential_integrity(data, records_with_issues)
        
        # Generate report
        report = self._generate_report(data, records_with_issues)
        
        logger.info(f"Analysis complete. Found {len(self.issues)} issues across {len(records_with_issues)} records.")
        
        return report
    
    def _check_missing_data(
        self,
        record: Dict[str, Any],
        record_id: str,
        records_with_issues: set
    ):
        """Check for missing or null data."""
        required_fields = self.required_fields or [
            'employee_id', 'first_name', 'last_name', 'email',
            'department', 'job_title', 'manager_id', 'hire_date',
            'employment_status'
        ]
        
        for field in required_fields:
            value = record.get(field)
            
            # Check if field is missing, null, or empty string
            if value is None or value == "":
                severity = Severity.CRITICAL if field in ['employee_id', 'email'] else Severity.HIGH
                
                self.issues.append(QualityIssue(
                    issue_id=f"{record_id}_{field}_missing",
                    issue_type=QualityIssueType.MISSING_DATA,
                    severity=severity,
                    field_name=field,
                    record_id=record_id,
                    current_value=value,
                    expected_value="Non-null value required",
                    description=f"Required field '{field}' is missing or null",
                    recommendation=f"Populate '{field}' with valid data from HR records",
                    auto_fixable=False
                ))
                records_with_issues.add(record_id)
    
    def _check_format_consistency(
        self,
        record: Dict[str, Any],
        record_id: str,
        records_with_issues: set,
        all_data: List[Dict[str, Any]]
    ):
        """Check for formatting inconsistencies."""
        
        # Email format check
        email = record.get('email', '')
        if email:
            # Check for valid email format
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                self.issues.append(QualityIssue(
                    issue_id=f"{record_id}_email_format",
                    issue_type=QualityIssueType.INVALID_DATA,
                    severity=Severity.HIGH,
                    field_name='email',
                    record_id=record_id,
                    current_value=email,
                    expected_value="valid@domain.com",
                    description=f"Invalid email format: '{email}'",
                    recommendation="Fix email format to include proper domain",
                    auto_fixable=True
                ))
                records_with_issues.add(record_id)
            
            # Check for company domain consistency
            if '@' in email:
                domain = email.split('@')[1]
                common_domain = self._get_most_common_domain(all_data)
                if common_domain and domain != common_domain and 'company.com' in common_domain:
                    self.issues.append(QualityIssue(
                        issue_id=f"{record_id}_email_domain",
                        issue_type=QualityIssueType.INCONSISTENT_FORMAT,
                        severity=Severity.MEDIUM,
                        field_name='email',
                        record_id=record_id,
                        current_value=email,
                        expected_value=f"*@{common_domain}",
                        description=f"Email domain '{domain}' differs from standard '{common_domain}'",
                        recommendation=f"Update email domain to company standard: {common_domain}",
                        auto_fixable=True
                    ))
                    records_with_issues.add(record_id)
            
            # Check for case consistency (should be lowercase)
            if email != email.lower():
                self.issues.append(QualityIssue(
                    issue_id=f"{record_id}_email_case",
                    issue_type=QualityIssueType.INCONSISTENT_FORMAT,
                    severity=Severity.LOW,
                    field_name='email',
                    record_id=record_id,
                    current_value=email,
                    expected_value=email.lower(),
                    description=f"Email contains uppercase letters",
                    recommendation=f"Convert email to lowercase: {email.lower()}",
                    auto_fixable=True
                ))
                records_with_issues.add(record_id)
        
        # Phone number format check
        phone = record.get('phone', '')
        if phone:
            # Standardize and check phone format
            standard_format = self._get_most_common_phone_format(all_data)
            if not self._matches_phone_format(phone, standard_format):
                self.issues.append(QualityIssue(
                    issue_id=f"{record_id}_phone_format",
                    issue_type=QualityIssueType.INCONSISTENT_FORMAT,
                    severity=Severity.MEDIUM,
                    field_name='phone',
                    record_id=record_id,
                    current_value=phone,
                    expected_value=standard_format or "+1-555-0000",
                    description=f"Phone number format inconsistent: '{phone}'",
                    recommendation=f"Standardize to format: {standard_format or '+1-555-0000'}",
                    auto_fixable=True
                ))
                records_with_issues.add(record_id)
        
        # Department name consistency
        department = record.get('department', '')
        if department:
            standard_dept = self._get_standard_department_name(department, all_data)
            if standard_dept and department != standard_dept:
                self.issues.append(QualityIssue(
                    issue_id=f"{record_id}_department_format",
                    issue_type=QualityIssueType.INCONSISTENT_FORMAT,
                    severity=Severity.MEDIUM,
                    field_name='department',
                    record_id=record_id,
                    current_value=department,
                    expected_value=standard_dept,
                    description=f"Department name inconsistent: '{department}' should be '{standard_dept}'",
                    recommendation=f"Standardize to: {standard_dept}",
                    auto_fixable=True
                ))
                records_with_issues.add(record_id)
        
        # Employment status consistency
        status = record.get('employment_status', '')
        if status:
            standard_status = self._get_standard_status(status, all_data)
            if standard_status and status != standard_status:
                self.issues.append(QualityIssue(
                    issue_id=f"{record_id}_status_format",
                    issue_type=QualityIssueType.INCONSISTENT_FORMAT,
                    severity=Severity.MEDIUM,
                    field_name='employment_status',
                    record_id=record_id,
                    current_value=status,
                    expected_value=standard_status,
                    description=f"Employment status format inconsistent: '{status}'",
                    recommendation=f"Standardize to: {standard_status}",
                    auto_fixable=True
                ))
                records_with_issues.add(record_id)
        
        # Name capitalization check
        first_name = record.get('first_name', '')
        last_name = record.get('last_name', '')
        
        if first_name and not first_name[0].isupper():
            self.issues.append(QualityIssue(
                issue_id=f"{record_id}_firstname_case",
                issue_type=QualityIssueType.INCONSISTENT_FORMAT,
                severity=Severity.LOW,
                field_name='first_name',
                record_id=record_id,
                current_value=first_name,
                expected_value=first_name.title(),
                description=f"First name not properly capitalized: '{first_name}'",
                recommendation=f"Capitalize properly: {first_name.title()}",
                auto_fixable=True
            ))
            records_with_issues.add(record_id)
        
        if last_name and not last_name[0].isupper():
            self.issues.append(QualityIssue(
                issue_id=f"{record_id}_lastname_case",
                issue_type=QualityIssueType.INCONSISTENT_FORMAT,
                severity=Severity.LOW,
                field_name='last_name',
                record_id=record_id,
                current_value=last_name,
                expected_value=last_name.title(),
                description=f"Last name not properly capitalized: '{last_name}'",
                recommendation=f"Capitalize properly: {last_name.title()}",
                auto_fixable=True
            ))
            records_with_issues.add(record_id)
    
    def _check_data_validity(
        self,
        record: Dict[str, Any],
        record_id: str,
        records_with_issues: set
    ):
        """Check for invalid data values."""
        
        # Check employee_id format
        emp_id = record.get('employee_id', '')
        if emp_id:
            # Should be in format EMP### with at least 3 digits
            if not re.match(r'^EMP\d{3,}$', emp_id):
                self.issues.append(QualityIssue(
                    issue_id=f"{record_id}_empid_invalid",
                    issue_type=QualityIssueType.INVALID_DATA,
                    severity=Severity.CRITICAL,
                    field_name='employee_id',
                    record_id=record_id,
                    current_value=emp_id,
                    expected_value="EMP### format",
                    description=f"Invalid employee_id format: '{emp_id}'",
                    recommendation="Generate valid employee_id in format EMP### with proper sequence number",
                    auto_fixable=False
                ))
                records_with_issues.add(record_id)
        
        # Check salary validity
        salary = record.get('salary')
        if salary is not None:
            if not isinstance(salary, (int, float)) or salary < 0:
                self.issues.append(QualityIssue(
                    issue_id=f"{record_id}_salary_invalid",
                    issue_type=QualityIssueType.INVALID_DATA,
                    severity=Severity.HIGH,
                    field_name='salary',
                    record_id=record_id,
                    current_value=salary,
                    expected_value="Positive number",
                    description=f"Invalid salary value: {salary}",
                    recommendation="Verify and update salary from payroll records",
                    auto_fixable=False
                ))
                records_with_issues.add(record_id)
            elif salary > 1000000:  # Anomaly detection
                self.issues.append(QualityIssue(
                    issue_id=f"{record_id}_salary_anomaly",
                    issue_type=QualityIssueType.ANOMALY,
                    severity=Severity.MEDIUM,
                    field_name='salary',
                    record_id=record_id,
                    current_value=salary,
                    expected_value="< $1,000,000",
                    description=f"Unusually high salary: ${salary:,}",
                    recommendation="Verify salary is correct for executive/C-level position",
                    auto_fixable=False
                ))
                records_with_issues.add(record_id)
        
        # Check performance rating validity
        rating = record.get('performance_rating')
        if rating is not None:
            if not isinstance(rating, (int, float)) or rating < 0 or rating > 5:
                self.issues.append(QualityIssue(
                    issue_id=f"{record_id}_rating_invalid",
                    issue_type=QualityIssueType.INVALID_DATA,
                    severity=Severity.MEDIUM,
                    field_name='performance_rating',
                    record_id=record_id,
                    current_value=rating,
                    expected_value="0.0 - 5.0",
                    description=f"Invalid performance rating: {rating}",
                    recommendation="Update rating to be within 0-5 scale",
                    auto_fixable=False
                ))
                records_with_issues.add(record_id)
    
    def _check_business_rules(
        self,
        record: Dict[str, Any],
        record_id: str,
        records_with_issues: set
    ):
        """Check for business rule violations."""
        
        # Rule: Terminated employees shouldn't have active managers or salaries
        status = record.get('employment_status', '').lower()
        if 'terminated' in status or 'inactive' in status:
            if record.get('manager_id'):
                self.issues.append(QualityIssue(
                    issue_id=f"{record_id}_terminated_has_manager",
                    issue_type=QualityIssueType.BUSINESS_RULE_VIOLATION,
                    severity=Severity.HIGH,
                    field_name='manager_id',
                    record_id=record_id,
                    current_value=record.get('manager_id'),
                    expected_value=None,
                    description="Terminated employee still has active manager assignment",
                    recommendation="Remove manager_id for terminated employees",
                    auto_fixable=True
                ))
                records_with_issues.add(record_id)
        
        # Rule: All employees except new hires should have performance review
        hire_date = record.get('hire_date', '')
        last_review = record.get('last_review_date')
        rating = record.get('performance_rating')
        
        if hire_date:
            # Check if employee has been with company > 6 months
            try:
                hire_datetime = datetime.strptime(hire_date, '%Y-%m-%d')
                months_employed = (datetime.now() - hire_datetime).days / 30
                
                if months_employed > 6 and (not last_review or rating is None):
                    self.issues.append(QualityIssue(
                        issue_id=f"{record_id}_missing_review",
                        issue_type=QualityIssueType.BUSINESS_RULE_VIOLATION,
                        severity=Severity.MEDIUM,
                        field_name='last_review_date',
                        record_id=record_id,
                        current_value=last_review,
                        expected_value="Recent review date",
                        description=f"Employee hired {hire_date} missing performance review",
                        recommendation="Schedule and complete performance review",
                        auto_fixable=False
                    ))
                    records_with_issues.add(record_id)
            except ValueError:
                pass  # Invalid date format will be caught elsewhere
    
    def _check_duplicates(self, data: List[Dict[str, Any]], records_with_issues: set):
        """Check for duplicate records."""
        
        # Check for duplicate employee IDs
        emp_ids = [r.get('employee_id') for r in data if r.get('employee_id')]
        emp_id_counts = Counter(emp_ids)
        
        for emp_id, count in emp_id_counts.items():
            if count > 1:
                self.issues.append(QualityIssue(
                    issue_id=f"{emp_id}_duplicate",
                    issue_type=QualityIssueType.DUPLICATE_DATA,
                    severity=Severity.CRITICAL,
                    field_name='employee_id',
                    record_id=emp_id,
                    current_value=f"{count} records",
                    expected_value="1 record",
                    description=f"Duplicate employee_id '{emp_id}' found in {count} records",
                    recommendation="Investigate duplicates and merge or remove incorrect records",
                    auto_fixable=False
                ))
                records_with_issues.add(emp_id)
        
        # Check for duplicate emails
        emails = [r.get('email') for r in data if r.get('email')]
        email_counts = Counter(emails)
        
        for email, count in email_counts.items():
            if count > 1:
                emp_ids_with_email = [r.get('employee_id') for r in data if r.get('email') == email]
                self.issues.append(QualityIssue(
                    issue_id=f"email_duplicate_{email}",
                    issue_type=QualityIssueType.DUPLICATE_DATA,
                    severity=Severity.HIGH,
                    field_name='email',
                    record_id=', '.join(emp_ids_with_email),
                    current_value=f"{count} records with '{email}'",
                    expected_value="Unique email per employee",
                    description=f"Email '{email}' used by {count} employees",
                    recommendation="Assign unique email addresses to each employee",
                    auto_fixable=False
                ))
                for emp_id in emp_ids_with_email:
                    records_with_issues.add(emp_id)
    
    def _check_referential_integrity(
        self,
        data: List[Dict[str, Any]],
        records_with_issues: set
    ):
        """Check referential integrity (e.g., manager_id references)."""
        
        # Get all valid employee IDs
        valid_emp_ids = {r.get('employee_id') for r in data if r.get('employee_id')}
        
        # Check manager_id references
        for record in data:
            record_id = record.get('employee_id', 'Unknown')
            manager_id = record.get('manager_id')
            
            if manager_id and manager_id not in valid_emp_ids:
                self.issues.append(QualityIssue(
                    issue_id=f"{record_id}_invalid_manager",
                    issue_type=QualityIssueType.REFERENTIAL_INTEGRITY,
                    severity=Severity.HIGH,
                    field_name='manager_id',
                    record_id=record_id,
                    current_value=manager_id,
                    expected_value="Valid employee_id",
                    description=f"Manager ID '{manager_id}' does not exist in employee records",
                    recommendation="Update to valid manager_id or leave null for top-level employees",
                    auto_fixable=False
                ))
                records_with_issues.add(record_id)
    
    def _get_most_common_domain(self, data: List[Dict[str, Any]]) -> Optional[str]:
        """Get most common email domain."""
        domains = []
        for record in data:
            email = record.get('email', '')
            if '@' in email:
                domains.append(email.split('@')[1])
        
        if domains:
            return Counter(domains).most_common(1)[0][0]
        return None
    
    def _get_most_common_phone_format(self, data: List[Dict[str, Any]]) -> Optional[str]:
        """Determine most common phone format."""
        formats = []
        for record in data:
            phone = record.get('phone', '')
            if phone:
                # Detect format pattern
                if re.match(r'^\+1-\d{3}-\d{4}$', phone):
                    formats.append('+1-555-0000')
                elif re.match(r'^\+1 \(\d{3}\) \d{4}$', phone):
                    formats.append('+1 (555) 0000')
                elif re.match(r'^\d{3}-\d{4}$', phone):
                    formats.append('555-0000')
        
        if formats:
            return Counter(formats).most_common(1)[0][0]
        return None
    
    def _matches_phone_format(self, phone: str, standard_format: Optional[str]) -> bool:
        """Check if phone matches standard format."""
        if not standard_format:
            return True
        
        if standard_format == '+1-555-0000':
            return bool(re.match(r'^\+1-\d{3}-\d{4}$', phone))
        elif standard_format == '+1 (555) 0000':
            return bool(re.match(r'^\+1 \(\d{3}\) \d{4}$', phone))
        elif standard_format == '555-0000':
            return bool(re.match(r'^\d{3}-\d{4}$', phone))
        
        return True
    
    def _get_standard_department_name(
        self,
        department: str,
        data: List[Dict[str, Any]]
    ) -> Optional[str]:
        """Get standardized department name."""
        # Collect all department names
        departments = [r.get('department', '') for r in data if r.get('department')]
        
        # Group by lowercase version
        dept_groups = defaultdict(list)
        for dept in departments:
            dept_groups[dept.lower()].append(dept)
        
        # Find most common capitalization for this department
        dept_lower = department.lower()
        if dept_lower in dept_groups:
            variants = dept_groups[dept_lower]
            if len(variants) > 1:
                # Return most common variant
                return Counter(variants).most_common(1)[0][0]
        
        return None
    
    def _get_standard_status(
        self,
        status: str,
        data: List[Dict[str, Any]]
    ) -> Optional[str]:
        """Get standardized employment status."""
        statuses = [r.get('employment_status', '') for r in data if r.get('employment_status')]
        
        # Group by lowercase version
        status_groups = defaultdict(list)
        for s in statuses:
            status_groups[s.lower()].append(s)
        
        # Find most common capitalization
        status_lower = status.lower()
        if status_lower in status_groups:
            variants = status_groups[status_lower]
            if len(variants) > 1:
                return Counter(variants).most_common(1)[0][0]
        
        return None
    
    def _generate_report(
        self,
        data: List[Dict[str, Any]],
        records_with_issues: set
    ) -> QualityReport:
        """Generate comprehensive quality report."""
        
        # Count issues by type and severity
        issues_by_type = defaultdict(int)
        issues_by_severity = defaultdict(int)
        
        for issue in self.issues:
            issues_by_type[issue.issue_type.value] += 1
            issues_by_severity[issue.severity.value] += 1
        
        # Calculate quality score (0-100)
        total_records = len(data)
        total_issues = len(self.issues)
        records_affected = len(records_with_issues)
        
        # Quality score formula: penalize both number of issues and records affected
        if total_records > 0:
            issue_penalty = (total_issues / (total_records * 10)) * 50  # Max 50 points penalty
            record_penalty = (records_affected / total_records) * 50  # Max 50 points penalty
            quality_score = max(0, 100 - issue_penalty - record_penalty)
        else:
            quality_score = 100
        
        # Generate summary with LLM
        summary = self._generate_summary_with_llm(
            total_records, records_affected, total_issues,
            issues_by_type, issues_by_severity, quality_score
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(issues_by_type, issues_by_severity)
        
        # Convert issues to dict with proper Enum serialization
        serialized_issues = []
        for issue in self.issues:
            issue_dict = asdict(issue)
            issue_dict['issue_type'] = issue.issue_type.value
            issue_dict['severity'] = issue.severity.value
            serialized_issues.append(issue_dict)
        
        report = QualityReport(
            report_id=f"QR_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now().isoformat(),
            total_records=total_records,
            records_with_issues=records_affected,
            total_issues=total_issues,
            issues_by_type=dict(issues_by_type),
            issues_by_severity=dict(issues_by_severity),
            quality_score=round(quality_score, 2),
            issues=serialized_issues,
            summary=summary,
            recommendations=recommendations
        )
        
        return report
    
    def _generate_summary_with_llm(
        self,
        total_records: int,
        records_affected: int,
        total_issues: int,
        issues_by_type: Dict,
        issues_by_severity: Dict,
        quality_score: float
    ) -> str:
        """Generate natural language summary using LLM."""
        
        prompt = f"""
You are a data quality analyst. Generate a concise summary (3-4 sentences) of this HRIS data quality report:

Total Records: {total_records}
Records with Issues: {records_affected} ({records_affected/total_records*100:.1f}%)
Total Issues Found: {total_issues}
Quality Score: {quality_score:.1f}/100

Issues by Type:
{json.dumps(issues_by_type, indent=2)}

Issues by Severity:
{json.dumps(issues_by_severity, indent=2)}

Focus on the most critical findings and overall data health.
"""
        
        try:
            response = self.llm_client.generate(
                prompt=prompt,
                temperature=0.3,
                max_tokens=200
            )
            return response.strip()
        except Exception as e:
            logger.warning(f"Failed to generate LLM summary: {e}")
            # Fallback summary
            return f"Analyzed {total_records} employee records. Found {total_issues} quality issues affecting {records_affected} records ({records_affected/total_records*100:.1f}%). Overall quality score: {quality_score:.1f}/100."
    
    def _generate_recommendations(
        self,
        issues_by_type: Dict,
        issues_by_severity: Dict
    ) -> List[str]:
        """Generate actionable recommendations."""
        
        recommendations = []
        
        # Priority recommendations based on severity
        if issues_by_severity.get('critical', 0) > 0:
            recommendations.append(
                f"🚨 CRITICAL: Address {issues_by_severity['critical']} critical issues immediately "
                "(duplicate IDs, invalid formats, system-breaking errors)"
            )
        
        if issues_by_severity.get('high', 0) > 0:
            recommendations.append(
                f"⚠️  HIGH PRIORITY: Resolve {issues_by_severity['high']} high-priority issues "
                "affecting data integrity and operations"
            )
        
        # Specific recommendations by issue type
        if issues_by_type.get('missing_data', 0) > 0:
            recommendations.append(
                f"📋 Fill in {issues_by_type['missing_data']} missing data fields from source HR systems"
            )
        
        if issues_by_type.get('inconsistent_format', 0) > 0:
            recommendations.append(
                f"✏️  Standardize {issues_by_type['inconsistent_format']} formatting inconsistencies "
                "to improve data quality"
            )
        
        if issues_by_type.get('referential_integrity', 0) > 0:
            recommendations.append(
                f"🔗 Fix {issues_by_type['referential_integrity']} referential integrity issues "
                "(invalid manager IDs, broken relationships)"
            )
        
        if issues_by_type.get('business_rule_violation', 0) > 0:
            recommendations.append(
                f"📊 Resolve {issues_by_type['business_rule_violation']} business rule violations "
                "(terminated employees with active data, missing reviews)"
            )
        
        # General recommendations
        recommendations.append(
            "🔄 Implement automated data validation rules at data entry points"
        )
        recommendations.append(
            "📈 Schedule regular data quality audits (monthly recommended)"
        )
        
        return recommendations
    
    def generate_cleansing_script(self, report: QualityReport) -> str:
        """
        Generate automated data cleansing script for auto-fixable issues.
        
        Args:
            report: Quality report with identified issues
            
        Returns:
            Python script to fix auto-fixable issues
        """
        
        auto_fixable = [
            issue for issue in report.issues
            if isinstance(issue, dict) and issue.get('auto_fixable', False)
        ]
        
        if not auto_fixable:
            return "# No auto-fixable issues found"
        
        script = """#!/usr/bin/env python3
\"\"\"
Auto-generated data cleansing script
Generated by HRIS Data Quality Agent
\"\"\"

import json
import re
from typing import Dict, List, Any

def clean_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    \"\"\"Apply automated data fixes.\"\"\"
    
    cleaned_data = []
    
    for record in data:
        record = record.copy()  # Don't modify original
        record_id = record.get('employee_id', 'Unknown')
        
"""
        
        # Group fixes by record
        fixes_by_record = defaultdict(list)
        for issue in auto_fixable:
            record_id = issue.get('record_id', '')
            fixes_by_record[record_id].append(issue)
        
        # Generate fix code
        script += "        # Apply fixes\n"
        
        for record_id, issues in fixes_by_record.items():
            script += f"        if record_id == '{record_id}':\n"
            
            for issue in issues:
                field = issue.get('field_name', '')
                expected = issue.get('expected_value', '')
                
                if 'email' in field and 'lowercase' in issue.get('description', '').lower():
                    script += f"            record['{field}'] = record.get('{field}', '').lower()\n"
                elif 'case' in issue.get('description', '').lower():
                    script += f"            record['{field}'] = record.get('{field}', '').title()\n"
                elif expected:
                    script += f"            record['{field}'] = '{expected}'\n"
        
        script += """
        cleaned_data.append(record)
    
    return cleaned_data

if __name__ == '__main__':
    # Load data
    with open('employee_data.json', 'r') as f:
        data = json.load(f)
    
    # Clean data
    cleaned = clean_data(data)
    
    # Save cleaned data
    with open('employee_data_cleaned.json', 'w') as f:
        json.dump(cleaned, f, indent=2)
    
    print(f"Cleaned {len(cleaned)} records")
"""
        
        return script
    
    def export_report(self, report: QualityReport, output_dir: Path):
        """
        Export quality report to various formats.
        
        Args:
            report: Quality report to export
            output_dir: Directory to save reports
        """
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 1. JSON report (detailed)
        json_path = output_dir / f"quality_report_{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(asdict(report), f, indent=2)
        logger.info(f"Saved JSON report: {json_path}")
        
        # 2. Summary text report
        summary_path = output_dir / f"quality_summary_{timestamp}.txt"
        with open(summary_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("HRIS DATA QUALITY REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Report ID: {report.report_id}\n")
            f.write(f"Generated: {report.timestamp}\n\n")
            f.write(f"Total Records: {report.total_records}\n")
            f.write(f"Records with Issues: {report.records_with_issues} "
                   f"({report.records_with_issues/report.total_records*100:.1f}%)\n")
            f.write(f"Total Issues: {report.total_issues}\n")
            f.write(f"Quality Score: {report.quality_score}/100\n\n")
            f.write("-" * 80 + "\n")
            f.write("SUMMARY\n")
            f.write("-" * 80 + "\n")
            f.write(f"{report.summary}\n\n")
            f.write("-" * 80 + "\n")
            f.write("ISSUES BY TYPE\n")
            f.write("-" * 80 + "\n")
            for issue_type, count in sorted(report.issues_by_type.items(), 
                                           key=lambda x: x[1], reverse=True):
                f.write(f"  {issue_type}: {count}\n")
            f.write("\n")
            f.write("-" * 80 + "\n")
            f.write("ISSUES BY SEVERITY\n")
            f.write("-" * 80 + "\n")
            for severity, count in sorted(report.issues_by_severity.items(),
                                         key=lambda x: ['critical', 'high', 'medium', 'low'].index(x[0])):
                f.write(f"  {severity.upper()}: {count}\n")
            f.write("\n")
            f.write("-" * 80 + "\n")
            f.write("RECOMMENDATIONS\n")
            f.write("-" * 80 + "\n")
            for i, rec in enumerate(report.recommendations, 1):
                f.write(f"{i}. {rec}\n")
        logger.info(f"Saved summary report: {summary_path}")
        
        # 3. CSV of issues (for analysis)
        csv_path = output_dir / f"quality_issues_{timestamp}.csv"
        with open(csv_path, 'w') as f:
            f.write("Issue ID,Type,Severity,Field,Record ID,Current Value,Expected Value,Description,Auto-Fixable\n")
            for issue in report.issues:
                if isinstance(issue, dict):
                    f.write(f"{issue.get('issue_id','')},")
                    f.write(f"{issue.get('issue_type','')},")
                    f.write(f"{issue.get('severity','')},")
                    f.write(f"{issue.get('field_name','')},")
                    f.write(f"{issue.get('record_id','')},")
                    f.write(f"\"{issue.get('current_value','')}\",")
                    f.write(f"\"{issue.get('expected_value','')}\",")
                    f.write(f"\"{issue.get('description','')}\",")
                    f.write(f"{issue.get('auto_fixable',False)}\n")
        logger.info(f"Saved issues CSV: {csv_path}")
        
        return {
            'json': json_path,
            'summary': summary_path,
            'csv': csv_path
        }


def main():
    """Main function for standalone execution."""
    
    # Configuration
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
    
    # Load sample data
    data_path = Path(__file__).parent.parent.parent / 'datasets' / 'hris_samples' / 'employee_data_with_quality_issues.json'
    
    try:
        with open(data_path, 'r') as f:
            employee_data = json.load(f)
        
        logger.info(f"Loaded {len(employee_data)} employee records")
        
        # Run quality analysis
        report = agent.analyze_dataset(employee_data)
        
        # Export reports
        output_dir = Path(__file__).parent.parent.parent / 'results' / 'hris_data_quality'
        agent.export_report(report, output_dir)
        
        # Generate cleansing script
        cleansing_script = agent.generate_cleansing_script(report)
        script_path = output_dir / f"cleansing_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        with open(script_path, 'w') as f:
            f.write(cleansing_script)
        logger.info(f"Generated cleansing script: {script_path}")
        
        # Print summary
        print("\n" + "=" * 80)
        print("HRIS DATA QUALITY ANALYSIS COMPLETE")
        print("=" * 80)
        print(f"\nQuality Score: {report.quality_score}/100")
        print(f"Total Issues: {report.total_issues}")
        print(f"Records Affected: {report.records_with_issues}/{report.total_records}")
        print(f"\nReports saved to: {output_dir}")
        
    except Exception as e:
        logger.error(f"Error running analysis: {e}")
        raise


if __name__ == '__main__':
    main()
