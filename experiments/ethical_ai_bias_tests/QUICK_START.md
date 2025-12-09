# Bias Testing Quick Start Guide

Get started with bias testing in 5 minutes.

## 1. Install Dependencies

```bash
# Already installed if you've set up hr-ai-lab
pip install -r requirements.txt
```

## 2. Verify Installation

```bash
cd /Users/sharjeel/dev/hr-ai-lab
python experiments/ethical_ai_bias_tests/test_bias_agent.py
```

Expected output:
```
✅ ALL TESTS PASSED
The Bias Testing Agent is working correctly!
```

## 3. Run Examples

```bash
python experiments/ethical_ai_bias_tests/example_bias_test.py
```

This demonstrates:
- Basic test case generation
- Custom bias scenarios  
- Mitigation strategies

## 4. Test Your First Experiment

### Option A: Test CV Screening (Quick)

```python
from experiments.ethical_ai_bias_tests import BiasTestingAgent, BiasType

# Initialize
config = {
    'llm_provider': 'google',
    'llm_model': 'gemini-2.5-flash-lite',
    'bias_threshold': 0.05
}
agent = BiasTestingAgent(config)

# Load a sample CV
sample_cv = {
    'name': 'Alex Johnson',
    'experience': [...],
    'education': [...],
    'skills': [...]
}

# Generate test cases
test_cases = agent.generate_test_cases(
    sample_cv,
    bias_types=[BiasType.GENDER, BiasType.ETHNICITY],
    data_type="cv"
)

print(f"Generated {len(test_cases)} bias test cases")
```

### Option B: Full Bias Analysis (Complete)

```python
from experiments.ethical_ai_bias_tests import run_bias_analysis_on_experiment
from experiments.recruitment_cv_screening.cv_screener import CVScreener

# Setup your experiment
screener = CVScreener(config)
job_requirements = {...}

# Define experiment function
def cv_experiment(cv_data):
    return screener.screen_candidate(cv_data, job_requirements)

# Run full bias analysis
report = run_bias_analysis_on_experiment(
    experiment_name="cv_screening",
    experiment_function=cv_experiment,
    score_extractor=lambda r: r['screening_score'],
    test_data=[sample_cv1, sample_cv2],
    bias_types=[BiasType.GENDER, BiasType.ETHNICITY, BiasType.AGE]
)

# Review results
print(f"Bias Rate: {report['summary']['bias_rate']:.1%}")
print(f"Assessment: {report['summary']['overall_assessment']}")
```

## 5. Interpret Results

### Understanding Bias Rate
- **< 10%**: ✅ Acceptable - minimal bias
- **10-25%**: ⚠️ Needs improvement - some bias present
- **25-40%**: 🚨 Significant bias - action required
- **> 40%**: 🔴 Critical - do not deploy

### Understanding Severity
- **None**: No bias detected
- **Low**: Minor difference (5-10%)
- **Moderate**: Noticeable difference (10-20%)
- **High**: Significant difference (20-30%)
- **Critical**: Major difference (>30%)

## 6. Take Action

### If Bias Detected:

1. **Review Critical Cases**
   ```python
   for case in report['critical_cases']:
       print(f"Issue: {case['modification']}")
       print(f"Difference: {case['score_difference']:.3f}")
   ```

2. **Implement Mitigations**
   - Remove names from data (blind screening)
   - Add fairness instructions to prompts
   - Use structured rubrics
   - Retrain/adjust model

3. **Re-test**
   ```python
   # After implementing fixes
   report_v2 = run_bias_analysis_on_experiment(...)
   
   # Compare
   print(f"Before: {report['summary']['bias_rate']:.1%}")
   print(f"After: {report_v2['summary']['bias_rate']:.1%}")
   ```

## 7. Integrate into Pipeline

### Option A: Manual Testing
```bash
# Before deploying any experiment
python test_experiment_for_bias.py --experiment cv_screening
```

### Option B: Automated CI/CD
```yaml
# In your CI/CD pipeline
- name: Run Bias Tests
  run: |
    python experiments/ethical_ai_bias_tests/test_all_experiments.py
    if [ $? -ne 0 ]; then
      echo "Bias detected - blocking deployment"
      exit 1
    fi
```

## Common Issues

### Issue: No test cases generated
**Solution**: Ensure your data has the required fields (name, education, etc.)

### Issue: All tests show bias
**Solution**: Check your bias_threshold - it might be too strict (default: 0.05)

### Issue: Tests run slowly
**Solution**: Use smaller test_data samples initially, then scale up

## Next Steps

1. ✅ Read full documentation: `experiments/ethical_ai_bias_tests/README.md`
2. ✅ Test all your experiments (A-I) for bias
3. ✅ Set up continuous bias monitoring
4. ✅ Document your bias testing process

## Getting Help

- Check examples: `experiments/ethical_ai_bias_tests/example_bias_test.py`
- Review test cases: `experiments/ethical_ai_bias_tests/test_bias_agent.py`
- Read full docs: `experiments/ethical_ai_bias_tests/README.md`

---

**You're ready to build fair and ethical HR AI!** 🎉
