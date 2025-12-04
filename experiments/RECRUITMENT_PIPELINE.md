# Recruitment Pipeline (Phase 2: Experiments A-C)

## Overview

The Recruitment Pipeline consists of three integrated AI-powered experiments that cover the complete hiring lifecycle from initial CV screening through interviews to performance reviews. These experiments demonstrate practical applications of LLMs in HR workflows.

## Experiments

### A. CV Screening Benchmark
**Location**: `experiments/recruitment_cv_screening/`

Automates candidate screening by parsing CVs, extracting qualifications, and matching against job requirements.

**Key Features**:
- Intelligent qualification extraction
- Smart matching with scoring
- Batch candidate processing
- Interview recommendations

[📖 Full Documentation](recruitment_cv_screening/README.md)

### B. Interview Summarization Agent
**Location**: `experiments/interview_summarisation/`

Processes interview transcripts to generate structured summaries with competency assessments and hiring recommendations.

**Key Features**:
- Competency extraction and rating
- Evidence-based assessment
- Candidate ranking
- Next-step recommendations

[📖 Full Documentation](interview_summarisation/README.md)

### C. Performance Review Auto-Draft
**Location**: `experiments/performance_review_drafter/`

Consolidates performance notes to generate balanced, professional performance reviews.

**Key Features**:
- Theme and pattern analysis
- Balanced strength/development feedback
- Goal tracking
- Promotion readiness assessment

[📖 Full Documentation](performance_review_drafter/README.md)

## Complete Workflow

### 1. Initial Screening (Experiment A)
```bash
# Screen all CVs for a position
python experiments/recruitment_cv_screening/cv_screener.py \
    --job-requirements jobs/senior_engineer.json \
    --output results/cv_screening
```

**Output**: Ranked candidates with scores, strengths, gaps, and interview questions

### 2. Interview Processing (Experiment B)
```bash
# Summarize interviews for shortlisted candidates
python experiments/interview_summarisation/interview_summarizer.py \
    --output results/interview_summarization
```

**Output**: Structured summaries with competency ratings and hiring recommendations

### 3. Post-Hire Review (Experiment C)
```bash
# Draft performance reviews after employee onboards
python experiments/performance_review_drafter/review_drafter.py \
    --output results/performance_reviews
```

**Output**: Comprehensive performance reviews with ratings and development plans

## Integrated Pipeline Example

```python
from experiments.recruitment_cv_screening.cv_screener import CVScreener
from experiments.interview_summarisation.interview_summarizer import InterviewSummarizer
from experiments.performance_review_drafter.review_drafter import PerformanceReviewDrafter

# 1. Screen CVs
screener = CVScreener(config)
screening_results = screener.screen_multiple(cv_list)
top_candidates = [r for r in screening_results if r['matching']['overall_score'] > 75]

# 2. Process interviews for top candidates
summarizer = InterviewSummarizer(config)
interview_summaries = summarizer.summarize_multiple(interview_list)
hired_candidates = [s for s in interview_summaries 
                    if s['summary']['recommendation'] in ['Strong Hire', 'Hire']]

# 3. After 6 months, draft performance reviews
drafter = PerformanceReviewDrafter(config)
performance_reviews = drafter.draft_multiple_reviews(performance_notes)
```

## Quick Start

### 1. Setup Environment

```bash
# Activate virtual environment
source .venv/bin/activate

# Verify Python packages
pip list | grep openai
```

### 2. Configure API Keys

```bash
# Set OpenAI API key (or your LLM provider)
export OPENAI_API_KEY='your-api-key-here'
```

### 3. Run All Experiments

```bash
# Run the complete recruitment pipeline
python scripts/run_experiment.py --experiment all --phase 2
```

## Configuration

All experiments share configuration from `config.json`:

```json
{
  "experiments": {
    "cv_screening": {
      "llm_model": "gpt-4",
      "temperature": 0.3,
      "dataset": "synthetic_cvs"
    },
    "interview_summarisation": {
      "llm_model": "gpt-4",
      "temperature": 0.5,
      "dataset": "interview_transcripts"
    },
    "performance_review": {
      "llm_model": "gpt-4",
      "temperature": 0.5,
      "dataset": "performance_notes"
    }
  }
}
```

## Datasets

All experiments use synthetic datasets from `datasets/`:

- **CVs**: `datasets/synthetic_cvs/` (10 diverse candidate profiles)
- **Interview Transcripts**: `datasets/interview_transcripts/` (4 interview examples)
- **Performance Notes**: `datasets/performance_notes/` (4 employee performance records)

## Results Structure

```
results/
├── cv_screening/
│   ├── screening_results_[timestamp].json
│   └── screening_metrics_[timestamp].json
├── interview_summarization/
│   ├── interview_summaries_[timestamp].json
│   ├── candidate_rankings_[timestamp].json
│   └── summarization_metrics_[timestamp].json
└── performance_reviews/
    ├── drafted_reviews_[timestamp].json
    ├── review_metrics_[timestamp].json
    └── review_[employee_id]_[timestamp].txt
```

## Evaluation Metrics

### CV Screening
- Average matching score (0-100)
- Recommendation distribution
- Interview recommendation rate
- Processing time per CV

### Interview Summarization
- Average competency ratings (1-5)
- Hiring recommendation distribution
- Summary quality scores
- Processing time per interview

### Performance Reviews
- Average rating distribution (1-5)
- Promotion readiness breakdown
- Review completeness scores
- Processing time per review

## Best Practices

### Data Quality
- Use structured, complete data for best results
- Include specific examples and details in inputs
- Maintain consistent data formats

### Human Oversight
- Always review AI outputs before using in decisions
- Use as decision support, not replacement for judgment
- Calibrate ratings across evaluators

### Bias Mitigation
- Run Experiment F (Bias Testing) on all outputs
- Monitor for demographic disparities
- Regular audits of recommendations

### Continuous Improvement
- Collect feedback on AI suggestions
- Track accuracy vs human decisions
- Adjust prompts and configurations based on results

## Integration with Other Experiments

### Experiment F: Ethical AI Bias Testing
Test all recruitment pipeline outputs for bias:
```python
from experiments.ethical_ai_bias_tests.bias_tester import BiasTestSuite

# Test CV screening for bias
bias_results = BiasTestSuite.test_cv_screening(screening_results)
```

### Experiment D: Career Pathway Recommender
Link performance reviews to career development:
```python
# Recommend career paths based on review
career_paths = pathway_recommender.recommend(
    employee_profile=review['analysis'],
    development_areas=review['review']['development_areas']
)
```

### Experiment I: HR Request Routing
Route follow-up questions from experiments:
```python
# Route candidate questions to appropriate HR team
routing_agent.route_request(
    request="Question about interview feedback",
    context=interview_summary
)
```

## Testing

Run tests for all recruitment pipeline experiments:

```bash
# Run unit tests
pytest tests/test_recruitment_pipeline.py

# Run integration tests
pytest tests/test_recruitment_integration.py

# Run with coverage
pytest tests/ --cov=experiments --cov-report=html
```

## Performance Benchmarks

Typical processing times (using GPT-4):

| Experiment | Per Item | Batch (10 items) |
|-----------|----------|------------------|
| CV Screening | 15-20s | 2-3 min |
| Interview Summarization | 20-30s | 3-5 min |
| Performance Review | 25-35s | 4-6 min |

*Times vary based on content length and LLM API response times*

## Cost Estimation

Approximate costs using GPT-4 (as of Dec 2024):

| Experiment | Cost per Item | Cost for 100 Items |
|-----------|---------------|---------------------|
| CV Screening | $0.15-0.25 | $15-25 |
| Interview Summarization | $0.20-0.35 | $20-35 |
| Performance Review | $0.25-0.40 | $25-40 |

*Use GPT-3.5-turbo for ~10x cost reduction with some quality tradeoff*

## Troubleshooting

### Common Issues

**API Rate Limits**
```python
# Add retry logic in config
"api_config": {
    "max_retries": 3,
    "retry_delay": 2
}
```

**Poor Quality Outputs**
- Increase temperature for more creative responses
- Add more context to prompts
- Use higher-quality models (GPT-4 vs GPT-3.5)

**Missing Dependencies**
```bash
pip install -r requirements.txt
```

### Debug Mode

```bash
# Run with debug logging
export LOG_LEVEL=DEBUG
python experiments/recruitment_cv_screening/cv_screener.py
```

## Dependencies

Core requirements:
- Python 3.8+
- OpenAI API access (or alternative LLM provider)
- `scripts/utils.py` utilities
- JSON datasets

See `requirements.txt` for complete list.

## Contributing

When adding features to recruitment pipeline experiments:

1. Maintain consistent interfaces across experiments
2. Add tests for new functionality
3. Update relevant README files
4. Run bias testing on new features
5. Document configuration options

## Future Enhancements

### Short Term
- [ ] Real-time processing APIs
- [ ] Web UI for each experiment
- [ ] Batch processing optimizations
- [ ] Additional LLM provider support

### Long Term
- [ ] Multi-language support
- [ ] Video interview analysis
- [ ] Integration with ATS systems
- [ ] Candidate feedback loop
- [ ] Predictive performance modeling

## License

See main project LICENSE file.

## Support

For issues or questions:
1. Check individual experiment README files
2. Review `docs/implementation-plan.md`
3. Check GitHub issues
4. Contact maintainers

---

**Status**: ✅ Phase 2 (A-C) Complete

**Next Phase**: D-E (Employee Development) or F (Bias Testing Framework)
