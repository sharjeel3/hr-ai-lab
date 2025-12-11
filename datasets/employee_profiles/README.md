# Employee Profiles Dataset

This directory contains synthetic employee profiles used for testing the Career Pathway Recommender (Experiment D) and other HR AI experiments.

## Files

- **`sample_employees.json`**: 10 diverse employee profiles across various roles, departments, and career stages

## Profile Schema

Each employee profile includes:

### Core Identifiers
- `employee_id`: Unique employee identifier
- `name`: Employee name (synthetic)
- `current_title`: Current job title
- `department`: Department/team

### Experience & Tenure
- `years_experience`: Total years of professional experience
- `years_at_company`: Years at current organization

### Skills & Qualifications
- `skills`: Array of technical and soft skills
- `education_level`: Highest degree obtained
- `certifications`: Professional certifications and credentials

### Career Development
- `career_interests`: Areas of interest for future growth
- `strengths`: Key strengths and competencies
- `career_goals`: Self-stated career aspirations (free text)
- `performance_rating`: Most recent performance review rating

## Sample Profiles Overview

| ID | Name | Current Role | Experience | Department |
|----|------|--------------|------------|------------|
| EMP001 | Alex Johnson | Software Engineer | 4 years | Engineering |
| EMP002 | Maria Rodriguez | Senior Software Engineer | 7 years | Engineering |
| EMP003 | David Chen | Junior Data Analyst | 1.5 years | Data & Analytics |
| EMP004 | Sarah Kim | Product Manager | 5 years | Product |
| EMP005 | James Patterson | DevOps Engineer | 6 years | Engineering |
| EMP006 | Jennifer Wu | Data Scientist | 3.5 years | Data & Analytics |
| EMP007 | Michael Torres | HR Business Partner | 8 years | People & Culture |
| EMP008 | Priya Sharma | Solutions Architect | 9 years | Customer Success |
| EMP009 | Lisa Anderson | Marketing Manager | 6 years | Marketing |
| EMP010 | Robert Jackson | Software Engineer | 2 years | Engineering |

## Career Stage Diversity

- **Early Career** (0-3 years): EMP003, EMP010
- **Mid-Career** (3-7 years): EMP001, EMP004, EMP005, EMP006, EMP009
- **Senior** (7+ years): EMP002, EMP007, EMP008

## Department Coverage

- **Engineering**: 5 profiles (various specializations)
- **Data & Analytics**: 2 profiles
- **Product**: 1 profile
- **People & Culture**: 1 profile
- **Customer Success**: 1 profile
- **Marketing**: 1 profile

## Usage Examples

### Load All Profiles
```python
import json
from pathlib import Path

with open('datasets/employee_profiles/sample_employees.json', 'r') as f:
    employees = json.load(f)

print(f"Loaded {len(employees)} employee profiles")
```

### Filter by Department
```python
engineering_employees = [
    emp for emp in employees 
    if emp['department'] == 'Engineering'
]
```

### Filter by Experience Level
```python
senior_employees = [
    emp for emp in employees 
    if emp['years_experience'] >= 7
]
```

### Use with Career Pathway Recommender
```bash
cd experiments/career_pathway_recommender
python run_career_pathway.py --employees ../../datasets/employee_profiles/sample_employees.json
```

## Data Quality Notes

✅ **Realistic Skill Combinations**: Skills are matched to realistic role requirements

✅ **Career Progression Alignment**: Experience levels match typical career trajectories

✅ **Diverse Backgrounds**: Variety in education, certifications, and interests

✅ **Privacy-Safe**: All data is synthetic - no real employee information

## Extending the Dataset

To add more profiles:

1. Follow the JSON schema structure
2. Ensure realistic skill-role combinations
3. Vary career stages and departments
4. Include career_goals for rich recommendations
5. Validate JSON syntax

Example template:
```json
{
  "employee_id": "EMP011",
  "name": "...",
  "current_title": "...",
  "department": "...",
  "years_experience": 0,
  "years_at_company": 0,
  "skills": [],
  "education_level": "...",
  "certifications": [],
  "career_interests": [],
  "strengths": [],
  "career_goals": "...",
  "performance_rating": "..."
}
```

## Related Experiments

- **Experiment D**: Career Pathway Recommender (primary use)
- **Experiment C**: Performance Review Drafter (profile context)
- **Experiment F**: Bias Testing (fairness validation)

## License

Synthetic data for research and development purposes only.
