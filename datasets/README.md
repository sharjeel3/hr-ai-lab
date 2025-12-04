# HR AI Lab - Synthetic Datasets

This directory contains realistic synthetic datasets for testing and evaluating HR AI experiments. All data is artificially generated and does not represent real individuals.

## 📂 Directory Structure

```
datasets/
├── synthetic_cvs/              # CVs/Resumes for recruitment screening
├── interview_transcripts/      # Interview conversations for summarization
├── performance_notes/          # Manager notes for performance reviews
├── job_families/               # Career pathway and job progression data
└── hris_samples/              # Employee records with data quality issues
```

## 📊 Dataset Details

### 1. Synthetic CVs (`synthetic_cvs/`)

**Purpose:** Testing CV screening and candidate evaluation AI agents

**Contents:**
- 10 diverse candidate profiles
- Multiple experience levels (junior, mid-level, senior)
- Various roles (Software Engineer, Product Manager, Data Scientist, UX Designer, HR, DevOps, etc.)
- Different backgrounds (career changers, recent grads, experienced professionals, career gaps)

**Data Fields:**
- Personal information (name, email, phone, location)
- Professional summary
- Work experience with dates and responsibilities
- Education history
- Technical and soft skills
- Certifications and languages

**Use Cases:**
- CV screening and ranking
- Candidate-job matching
- Skills extraction and analysis
- Bias detection in hiring

### 2. Interview Transcripts (`interview_transcripts/`)

**Purpose:** Testing interview summarization and candidate assessment AI

**Contents:**
- 4 complete interview transcripts
- Mix of strong and weak candidates
- Technical and behavioral questions
- Interviewer notes and ratings

**Data Fields:**
- Candidate and interviewer information
- Timestamped conversation transcript
- Performance notes by category
- Rating scores
- Hiring recommendations

**Use Cases:**
- Interview summarization
- Candidate evaluation
- Key points extraction
- Sentiment analysis

### 3. Performance Notes (`performance_notes/`)

**Purpose:** Testing performance review drafting AI agents

**Contents:**
- 4 performance review documents
- Different performance levels (exceptional, high, needs improvement, average)
- Manager observations over time
- Goal tracking

**Data Fields:**
- Employee information
- Dated observations by category
- Strengths and development areas
- Goals progress tracking
- Overall performance ratings
- Promotion readiness assessments

**Use Cases:**
- Performance review generation
- Employee evaluation summarization
- Goal tracking and analysis
- Talent identification

### 4. Job Families (`job_families/`)

**Purpose:** Testing career pathway recommendation systems

**Contents:**
- 3 complete job family definitions
- Career progression ladders
- Skills required at each level

**Job Families Included:**
- Software Engineering (5 levels)
- Product Management (5 levels)
- Data Science & Analytics (5 levels)

**Data Fields:**
- Career levels with salary ranges
- Required and nice-to-have skills
- Key responsibilities
- Promotion criteria
- Adjacent role transitions
- Skill development paths

**Use Cases:**
- Career pathway recommendations
- Skills gap analysis
- Career planning and development
- Succession planning

### 5. HRIS Samples (`hris_samples/`)

**Purpose:** Testing data quality agents and data cleaning systems

**Contents:**
- 20 employee records
- **Intentionally contains data quality issues** (see README in directory)

**Known Issues:**
- Missing data (null fields, empty strings)
- Inconsistent formatting (phone numbers, emails, names)
- Invalid data (malformed IDs, wrong domains)
- Outdated records
- Business rule violations

**Data Fields:**
- Employee ID and personal info
- Department and job title
- Manager relationships
- Employment status and dates
- Salary and performance ratings

**Use Cases:**
- Data quality detection
- Data cleaning and standardization
- Data validation rule creation
- Data quality reporting

## 🔄 Generating New Data

Use the dataset generation script to create additional synthetic data:

```bash
# Generate default datasets
python scripts/generate_datasets.py --all

# Generate custom amounts
python scripts/generate_datasets.py --cvs 50 --interviews 20 --performance 30

# Use specific random seed for reproducibility
python scripts/generate_datasets.py --all --seed 12345
```

## 📋 Data Format

All datasets use JSON format for easy parsing and manipulation. Each file is standalone and can be used independently.

**Example CV structure:**
```json
{
  "candidate_id": "CV001",
  "name": "Sarah Chen",
  "email": "sarah.chen@email.com",
  "experience": [...],
  "education": [...],
  "skills": {...}
}
```

## 🔒 Privacy & Ethics

- **All data is synthetic** - No real personal information is used
- Generated using realistic but fictional names, companies, and details
- Designed to minimize bias while testing for bias detection
- Should not be used to train production models without review

## 🎯 Best Practices

1. **Test with diverse data**: Use the full range of profiles to ensure AI systems work for all candidates
2. **Bias testing**: Use these datasets to test for unfair bias in AI systems
3. **Validation**: Cross-reference AI outputs with expected results
4. **Regeneration**: Regularly regenerate data to avoid overfitting to specific test cases
5. **Expansion**: Add more diverse profiles as needed for comprehensive testing

## 📝 Citation

If using these datasets in research or publications, please cite:

```
HR AI Lab Synthetic Datasets
https://github.com/sharjeel3/hr-ai-lab
Generated: 2024
```

## 🤝 Contributing

To add new dataset types or improve existing ones:
1. Update the generation scripts in `scripts/generate_datasets.py`
2. Add appropriate documentation
3. Ensure data is realistic and diverse
4. Test with relevant experiments

## 📖 Related Documentation

- [Implementation Plan](../docs/implementation-plan.md)
- [Phase 1 Completion](../docs/phase1-completion.md)
- [Scripts README](../scripts/README.md)
