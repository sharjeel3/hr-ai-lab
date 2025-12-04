# CV Screening Benchmark (Experiment A)

## Overview

An AI-powered CV screening system that automates candidate evaluation by parsing CVs, extracting key qualifications, matching against job requirements, and generating detailed screening reports with scores and recommendations.

## Features

- **Intelligent Qualification Extraction**: Uses LLM to extract technical skills, soft skills, experience, education, certifications, and achievements
- **Smart Matching**: Matches candidate qualifications against job requirements with detailed scoring
- **Batch Processing**: Screen multiple candidates efficiently and generate ranked results
- **Detailed Reports**: Provides comprehensive screening reports with strengths, gaps, and interview recommendations

## Usage

### Basic Usage

```python
from experiments.recruitment_cv_screening.cv_screener import run_cv_screening_experiment

# Run the experiment
results = run_cv_screening_experiment(
    config_path='config.json',
    output_dir='results/cv_screening'
)
```

### Command Line

```bash
# Activate virtual environment
source .venv/bin/activate

# Run with default settings
python experiments/recruitment_cv_screening/cv_screener.py

# Run with custom job requirements
python experiments/recruitment_cv_screening/cv_screener.py \
    --job-requirements path/to/job_requirements.json \
    --output results/custom_screening
```

### Custom Job Requirements

Create a JSON file with job requirements:

```json
{
    "title": "Senior Software Engineer",
    "min_years_experience": 5,
    "required_skills": [
        "Python", "JavaScript", "React", "REST APIs",
        "SQL", "Git", "Microservices"
    ],
    "preferred_skills": [
        "AWS", "Docker", "Kubernetes", "CI/CD"
    ],
    "education": "Bachelor's degree in Computer Science or related field",
    "leadership": "Experience leading small teams or projects"
}
```

## Configuration

Configure in `config.json`:

```json
{
  "experiments": {
    "cv_screening": {
      "dataset": "synthetic_cvs",
      "llm_model": "gpt-4",
      "temperature": 0.3,
      "max_tokens": 1000,
      "required_fields": [
        "skills",
        "experience_years",
        "certifications"
      ]
    }
  }
}
```

## Output

The experiment generates:

1. **screening_results_[timestamp].json**: Complete screening results for all candidates
2. **screening_metrics_[timestamp].json**: Aggregate metrics and statistics

### Sample Output Structure

```json
{
  "candidate_id": "CV001",
  "candidate_name": "Sarah Chen",
  "qualifications": {
    "total_years_experience": 8,
    "technical_skills": ["Python", "JavaScript", "React", "AWS"],
    "key_achievements": [...]
  },
  "matching": {
    "overall_score": 85,
    "recommendation": "Strong Match",
    "strengths": ["Strong technical background", "Leadership experience"],
    "gaps": ["No Kubernetes experience"],
    "interview_recommendation": true,
    "key_questions": [...]
  }
}
```

## Metrics

- **Total Candidates**: Number of CVs screened
- **Average Score**: Mean matching score (0-100)
- **Recommendations**: Distribution of Strong Match, Good Match, Possible Match, Weak Match
- **Interview Recommendations**: Number of candidates recommended for interviews

## Evaluation Criteria

The screener evaluates candidates on:

1. **Experience**: Years and relevance of professional experience
2. **Technical Skills**: Match with required and preferred skills
3. **Education**: Qualification level and relevance
4. **Achievements**: Impact and quality of accomplishments
5. **Leadership**: Management and mentoring experience
6. **Cultural Indicators**: Communication, initiative, problem-solving

## Best Practices

- Keep job requirements specific but not overly restrictive
- Review screening results as a starting point, not final decisions
- Use "key_questions" to guide interviews
- Combine with human judgment for final hiring decisions
- Monitor for bias using the Ethical AI Bias Testing Suite (Experiment F)

## Dependencies

- Python 3.8+
- OpenAI API key (or configured LLM provider)
- Core utilities from `scripts/utils.py`

## Next Steps

After screening:
1. Review top candidates' full profiles
2. Use generated interview questions
3. Proceed to Interview Summarization (Experiment B)
4. Run bias testing to ensure fairness

## Limitations

- Dependent on LLM quality and API availability
- May miss nuanced qualifications not explicitly stated
- Should be used as a support tool, not replacement for human judgment
- Requires well-structured CV data for best results
