# HRIS Data Quality Issues Documentation

This dataset intentionally contains various data quality issues for testing the HRIS Data Quality Agent.

## Data Quality Issues Present:

### 1. **Missing Data**
- EMP003: Missing last_name
- EMP003: Missing phone number (null)
- EMP003: Missing performance_rating (null)
- EMP011: Missing performance_rating (null) - acceptable for new hire
- EMP011: Missing last_review_date (null) - acceptable for new hire
- EMP012: Missing phone number (null)
- EMP012: Missing manager_id (empty string)

### 2. **Inconsistent Formatting**
- **Phone Numbers**: Multiple formats
  - "+1-555-0101" (EMP001)
  - "555-0102" (EMP002) - missing country code
  - "+1 (555) 0104" (EMP004) - different format
  - "555.0106" (EMP006) - dots instead of hyphens
  - "5550114" (EMP014) - no separators
  
- **Email Addresses**:
  - "amanda.foster@company" (EMP007) - missing .com
  - "lisa.park@oldcompany.com" (EMP009) - wrong domain
  - "ROBERT.TAYLOR@COMPANY.COM" (EMP004) - all caps
  
- **Department Names**:
  - "Engineering" (EMP001) - capitalized
  - "engineering" (EMP002) - lowercase
  - "Data" vs "Data Science" - inconsistent naming
  
- **Location**:
  - "San Francisco, CA" (EMP001) - full format
  - "San Francisco" (EMP002) - missing state
  - "Remote" - mixed with city names
  
- **Employment Status**:
  - "Active" (most) - capitalized
  - "active" (EMP004) - lowercase
  - "Terminated" (EMP010) - different value

- **Name Capitalization**:
  - EMP008: "carlos" and "rodriguez" - all lowercase

### 3. **Invalid or Suspicious Data**
- EMP019 (EMP053): Invalid employee_id format - missing digits (shows as "EMP")
- EMP010: Still has active salary and manager despite "Terminated" status
- Orphaned manager_id references (if some managers don't exist in dataset)

### 4. **Outdated Data**
- EMP010: Terminated employee with last_review_date in 2023
- EMP003: Last review date in January 2024 (>6 months ago)

### 5. **Potential Duplicates**
- Could have duplicate entries with slight variations (not included but could be added)

### 6. **Business Rule Violations**
- New employees (EMP011) with hire_date in 2024 should have null performance ratings
- Terminated employees should not have active employment status indicators

## Expected Agent Behavior:

The HRIS Data Quality Agent should:
1. Detect missing critical fields
2. Identify formatting inconsistencies
3. Flag invalid data formats
4. Suggest data standardization rules
5. Highlight business rule violations
6. Recommend data cleaning procedures
7. Generate a data quality report with severity levels

## Usage:

This dataset should be used to test:
- Data validation rules
- Data quality scoring
- Automated data cleaning suggestions
- Data quality dashboards
- Alert systems for data quality issues
