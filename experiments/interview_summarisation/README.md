# Interview Summarization Agent (Experiment B)

## Overview

An AI-powered interview summarization system that processes interview transcripts, identifies key competencies, extracts technical and behavioral insights, and generates structured summaries with hiring recommendations.

## Features

- **Competency Extraction**: Automatically identifies and rates technical, behavioral, and cultural fit competencies
- **Structured Summaries**: Generates comprehensive interview summaries following best practices
- **Evidence-Based Assessment**: Links ratings to specific examples from the transcript
- **Candidate Ranking**: Ranks candidates based on overall performance scores
- **Next-Step Recommendations**: Suggests follow-up actions and questions for subsequent rounds

## Usage

### Basic Usage

```python
from experiments.interview_summarisation.interview_summarizer import run_interview_summarization_experiment

# Run the experiment
results = run_interview_summarization_experiment(
    config_path='config.json',
    output_dir='results/interview_summarization'
)
```

### Command Line

```bash
# Activate virtual environment
source .venv/bin/activate

# Run with default settings
python experiments/interview_summarisation/interview_summarizer.py

# Run with custom configuration
python experiments/interview_summarisation/interview_summarizer.py \
    --config custom_config.json \
    --output results/custom_interviews
```

### Programmatic Usage

```python
from experiments.interview_summarisation.interview_summarizer import InterviewSummarizer
import json

# Initialize summarizer
config = {
    'llm_provider': 'openai',
    'llm_model': 'gpt-4',
    'temperature': 0.5
}
summarizer = InterviewSummarizer(config)

# Load interview data
with open('datasets/interview_transcripts/interview_001.json') as f:
    interview_data = json.load(f)

# Generate summary
summary = summarizer.summarize_interview(interview_data)
```

## Configuration

Configure in `config.json`:

```json
{
  "experiments": {
    "interview_summarisation": {
      "dataset": "interview_transcripts",
      "llm_model": "gpt-4",
      "temperature": 0.5,
      "max_tokens": 2000,
      "competency_rubric_path": "datasets/job_families/competency_rubric.json"
    }
  }
}
```

## Competency Rubric

Default competencies evaluated:

### Technical Skills
- Problem solving ability
- System design knowledge
- Code quality awareness
- Technical depth
- Best practices understanding

### Behavioral Skills
- Communication skills
- Leadership and mentoring
- Collaboration
- Adaptability
- Initiative and ownership

### Cultural Fit
- Values alignment
- Team orientation
- Growth mindset
- Work style preferences

## Output

The experiment generates:

1. **interview_summaries_[timestamp].json**: Complete summaries for all interviews
2. **candidate_rankings_[timestamp].json**: Ranked list of candidates by score
3. **summarization_metrics_[timestamp].json**: Aggregate statistics

### Sample Output Structure

```json
{
  "interview_metadata": {
    "interview_id": "INT001",
    "candidate_name": "Sarah Chen",
    "position": "Senior Software Engineer"
  },
  "competency_analysis": {
    "technical_competencies": [
      {
        "skill_name": "Problem Solving",
        "rating": 5,
        "evidence": "Systematically debugged payment processing issue...",
        "notes": "Excellent methodical approach"
      }
    ]
  },
  "summary": {
    "executive_summary": "Strong technical candidate with excellent...",
    "recommendation": "Strong Hire",
    "overall_score": 88,
    "next_steps": "Move to final round with focus on system design"
  }
}
```

## Metrics

- **Total Interviews**: Number of interviews processed
- **Average Score**: Mean overall score (0-100)
- **Recommendation Distribution**: Strong Hire, Hire, Maybe, No Hire counts
- **Average Duration**: Mean interview length

## Evaluation Process

The summarizer follows a two-step process:

### Step 1: Competency Extraction
- Analyzes transcript for evidence of each competency
- Rates each competency on 1-5 scale
- Links ratings to specific quotes and examples

### Step 2: Summary Generation
- Creates executive summary
- Highlights key strengths and concerns
- Provides hiring recommendation with reasoning
- Suggests questions for next rounds

## Use Cases

1. **Post-Interview Debriefs**: Generate structured notes immediately after interviews
2. **Hiring Committee Prep**: Provide consistent summaries for decision-making
3. **Interview Quality Assurance**: Ensure comprehensive competency coverage
4. **Candidate Comparison**: Standardize evaluation across interviewers
5. **Interview Training**: Use summaries to train new interviewers

## Best Practices

- Review raw transcript alongside summary for context
- Use summaries as input to hiring discussions, not replacements
- Calibrate ratings across interviewers to ensure consistency
- Follow up on "areas of concern" in subsequent interviews
- Document decision rationale beyond the AI summary

## Interview Data Format

Transcripts should follow this structure:

```json
{
  "interview_id": "INT001",
  "candidate_name": "John Doe",
  "position": "Software Engineer",
  "interviewer": "Jane Smith",
  "date": "2024-11-15",
  "duration_minutes": 45,
  "interview_type": "Technical + Behavioral",
  "transcript": [
    {
      "speaker": "Interviewer",
      "timestamp": "00:00",
      "text": "Question text..."
    },
    {
      "speaker": "Candidate",
      "timestamp": "00:15",
      "text": "Response text..."
    }
  ]
}
```

## Integration

### With CV Screening (Experiment A)
Use CV screening results to prepare targeted interview questions

### With Performance Reviews (Experiment C)
Apply similar competency frameworks for consistency

### With Bias Testing (Experiment F)
Run bias tests on summaries to ensure fair evaluation

## Dependencies

- Python 3.8+
- OpenAI API key (or configured LLM provider)
- Core utilities from `scripts/utils.py`

## Limitations

- Quality depends on transcript clarity and completeness
- May miss non-verbal cues (tone, body language)
- Best for structured interviews with clear questions
- Requires calibration with human judgment
- Should not be sole basis for hiring decisions

## Future Enhancements

- Multi-interviewer synthesis
- Video analysis integration
- Real-time summarization during interviews
- Custom competency frameworks per role
- Sentiment analysis
