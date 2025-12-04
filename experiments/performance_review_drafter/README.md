# Performance Review Auto-Draft (Experiment C)

## Overview

An AI-powered performance review drafting system that consolidates performance notes, analyzes employee achievements and growth areas, and generates balanced, professional performance reviews according to organizational templates.

## Features

- **Intelligent Note Analysis**: Extracts themes, patterns, and key achievements from scattered performance notes
- **Balanced Reviews**: Generates fair reviews highlighting strengths while constructively addressing development areas
- **Goal Tracking**: Analyzes progress on stated goals with quality assessments
- **Multiple Formats**: Produces both structured JSON and formatted text documents
- **Customizable Templates**: Supports custom review templates and rating scales
- **Actionable Recommendations**: Provides specific next steps and development plans

## Usage

### Basic Usage

```python
from experiments.performance_review_drafter.review_drafter import run_performance_review_experiment

# Run the experiment
results = run_performance_review_experiment(
    config_path='config.json',
    output_dir='results/performance_reviews'
)
```

### Command Line

```bash
# Activate virtual environment
source .venv/bin/activate

# Run with default settings
python experiments/performance_review_drafter/review_drafter.py

# Run with custom configuration
python experiments/performance_review_drafter/review_drafter.py \
    --config custom_config.json \
    --output results/custom_reviews
```

### Draft Single Review

```python
from experiments.performance_review_drafter.review_drafter import PerformanceReviewDrafter
import json

# Initialize drafter
config = {
    'llm_provider': 'openai',
    'llm_model': 'gpt-4',
    'temperature': 0.5
}
drafter = PerformanceReviewDrafter(config)

# Load performance notes
with open('datasets/performance_notes/perf_note_001.json') as f:
    performance_data = json.load(f)

# Draft review
review = drafter.draft_performance_review(performance_data)

# Get formatted document
print(review['formatted_document'])
```

## Configuration

Configure in `config.json`:

```json
{
  "experiments": {
    "performance_review": {
      "dataset": "performance_notes",
      "llm_model": "gpt-4",
      "temperature": 0.5,
      "max_tokens": 3000,
      "review_template": {
        "sections": [
          "Executive Summary",
          "Key Achievements",
          "Technical/Functional Skills",
          "Leadership & Collaboration",
          "Areas for Development",
          "Goal Achievement",
          "Overall Rating",
          "Recommended Actions"
        ],
        "rating_scale": {
          "5": "Outstanding",
          "4": "Exceeds Expectations",
          "3": "Meets Expectations",
          "2": "Needs Improvement",
          "1": "Unsatisfactory"
        }
      }
    }
  }
}
```

## Review Process

The drafter follows a two-step pipeline:

### Step 1: Note Analysis
- Extracts key achievements with impact assessment
- Analyzes technical and soft skill competencies
- Identifies development areas with suggestions
- Reviews goal progress and quality
- Detects patterns and trajectory

### Step 2: Review Drafting
- Generates executive summary
- Writes detailed competency assessments
- Provides constructive development feedback
- Assigns overall rating with justification
- Assesses promotion readiness
- Creates actionable development plan

## Output

The experiment generates:

1. **drafted_reviews_[timestamp].json**: Complete review data for all employees
2. **review_metrics_[timestamp].json**: Aggregate statistics and distributions
3. **review_[employee_id]_[timestamp].txt**: Formatted review documents for each employee

### Sample Review Structure

```json
{
  "employee_id": "EMP1045",
  "employee_name": "Jennifer Martinez",
  "review": {
    "executive_summary": "Jennifer has demonstrated exceptional...",
    "key_achievements": "Led authentication service migration...",
    "technical_skills_assessment": "Strong technical capabilities...",
    "leadership_collaboration": "Excellent mentor who...",
    "development_areas": "Could improve task estimation...",
    "goal_achievement_summary": "Exceeded all stated goals...",
    "overall_rating": 4.5,
    "promotion_readiness": "Ready Now",
    "recommended_next_steps": [
      {
        "action": "Take on architecture ownership for core services",
        "timeline": "Next quarter",
        "support_needed": "Pairing with Principal Engineer"
      }
    ]
  }
}
```

## Rating Scale

Default 5-point scale:

- **5 - Outstanding**: Consistently exceeds expectations, exceptional impact
- **4 - Exceeds Expectations**: Regularly delivers beyond requirements
- **3 - Meets Expectations**: Solid performer meeting all requirements
- **2 - Needs Improvement**: Performance below expectations
- **1 - Unsatisfactory**: Significant performance concerns

## Metrics

Generated metrics include:

- **Total Reviews**: Number of reviews drafted
- **Average Rating**: Mean performance rating
- **Rating Distribution**: Count at each rating level
- **Promotion Readiness**: Distribution across readiness categories

## Performance Note Format

Input data should include:

```json
{
  "performance_note_id": "PN001",
  "employee_id": "EMP1045",
  "employee_name": "Jennifer Martinez",
  "position": "Software Engineer II",
  "manager": "David Chen",
  "review_period": "2024 Q3-Q4",
  "notes": [
    {
      "date": "2024-09-15",
      "category": "Technical Achievement",
      "observation": "Led refactoring of authentication service..."
    }
  ],
  "strengths": ["Strong technical skills", "Excellent mentor"],
  "areas_for_development": ["Task estimation"],
  "goals_progress": {
    "goal_1": {
      "goal": "Migrate authentication system",
      "status": "Completed ahead of schedule"
    }
  }
}
```

## Best Practices

### For Managers
1. **Document Throughout Period**: Add notes regularly, not just before reviews
2. **Be Specific**: Include concrete examples and impact
3. **Balance Feedback**: Document both achievements and areas for growth
4. **Review & Personalize**: Edit AI drafts to match your voice and add personal touches
5. **Discuss with Employee**: Use draft as discussion starting point, not final document

### For Organizations
1. **Standardize Templates**: Use consistent review templates across teams
2. **Calibrate Ratings**: Review rating distributions to ensure fairness
3. **Train Managers**: Help managers write better performance notes
4. **Run Bias Tests**: Use Experiment F to check for bias in reviews
5. **Combine with 1:1s**: Reviews should summarize ongoing conversations, not surprise employees

## Use Cases

1. **Annual Reviews**: Consolidate year's worth of notes into comprehensive review
2. **Mid-Year Check-ins**: Generate progress summaries
3. **Promotion Packets**: Create supporting documentation for promotions
4. **PIPs (Performance Improvement Plans)**: Draft constructive development plans
5. **Manager Training**: Generate sample reviews for calibration exercises

## Tone & Style

The drafter aims for:

- **Professional**: Appropriate for HR records
- **Balanced**: Recognition with constructive feedback
- **Specific**: Concrete examples over generic statements
- **Supportive**: Growth-oriented, not punitive
- **Authentic**: Personal, not robotic

## Integration

### With Interview Summarization (Experiment B)
Use consistent competency frameworks across hiring and performance

### With Career Pathway Recommender (Experiment D)
Link development areas to career advancement opportunities

### With Bias Testing (Experiment F)
Ensure fairness across demographics, departments, and levels

## Manager Workflow

1. **Collect Notes**: Gather observations throughout review period
2. **Run Drafter**: Generate initial draft
3. **Review & Edit**: Add personal insights, adjust tone
4. **Calibrate**: Discuss with peers and HR
5. **Discuss**: Have conversation with employee
6. **Finalize**: Incorporate employee feedback
7. **Submit**: Complete official review process

## Dependencies

- Python 3.8+
- OpenAI API key (or configured LLM provider)
- Core utilities from `scripts/utils.py`

## Limitations

- Cannot replace manager judgment and relationship context
- Quality depends on input note quality and specificity
- May miss informal feedback and conversations
- Should be edited and personalized before sharing
- Not suitable for sensitive situations requiring legal review
- Cannot assess non-documented behaviors or achievements

## Ethical Considerations

- **Transparency**: Employees should know AI is used in drafting
- **Human Oversight**: Managers must review and own final content
- **Bias Monitoring**: Regular testing for demographic biases
- **Privacy**: Secure handling of performance data
- **Fairness**: Consistent standards across employees

## Future Enhancements

- Multi-source feedback integration (360 reviews)
- Peer comparison and calibration suggestions
- Career development plan generation
- Skills gap analysis with training recommendations
- Sentiment analysis of manager feedback
- Integration with HR systems (Workday, BambooHR, etc.)
- Real-time note quality feedback
