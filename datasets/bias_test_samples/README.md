# Bias Test Sample Data

This directory contains synthetic data specifically designed for bias testing in HR AI systems.

## Files

### `sample_cv_for_bias_testing.json`

A neutral, high-quality CV template used as the baseline for generating counterfactual test cases.

**Key Characteristics:**
- Gender-neutral name (Alex Johnson)
- Strong qualifications (8 years experience, good skills)
- Standard university (State University)
- Urban location (San Francisco, CA)
- No employment gaps
- Linear career progression

**Usage:**
```python
from experiments.ethical_ai_bias_tests.bias_testing_agent import BiasTestingAgent, BiasType

# Load the sample CV
with open('datasets/bias_test_samples/sample_cv_for_bias_testing.json') as f:
    sample_cv = json.load(f)

# Generate bias test cases
agent = BiasTestingAgent(config)
test_cases = agent.generate_test_cases(
    sample_cv, 
    [BiasType.GENDER, BiasType.ETHNICITY], 
    data_type="cv"
)
```

### `sample_interview_for_bias_testing.json`

A neutral interview transcript template for testing interview summarization bias.

**Key Characteristics:**
- Gender-neutral name (Jordan Taylor)
- Strong performance indicators
- Balanced technical and behavioral responses
- Clear competency demonstrations

**Usage:**
```python
# Load the sample interview
with open('datasets/bias_test_samples/sample_interview_for_bias_testing.json') as f:
    sample_interview = json.load(f)

# Generate test cases
test_cases = agent.generate_test_cases(
    sample_interview,
    [BiasType.GENDER, BiasType.AGE],
    data_type="interview"
)
```

## Purpose

These templates are designed to be modified by the BiasTestingAgent to create counterfactual test pairs. For example:

**Original:**
```json
{
  "name": "Alex Johnson",
  "education": [{"institution": "State University"}]
}
```

**Modified (Gender Test):**
```json
{
  "name": "Jennifer Anderson",
  "education": [{"institution": "State University"}]
}
```

**Modified (Education Test):**
```json
{
  "name": "Alex Johnson",
  "education": [{"institution": "Harvard University"}]
}
```

By comparing outcomes between original and modified versions, we can detect bias.

## Best Practices

1. **Use Neutral Baselines**: Start with gender-neutral names and standard qualifications
2. **Single Variable Changes**: Modify only one attribute at a time
3. **Representative Samples**: Test with diverse scenarios, not just one template
4. **Realistic Data**: Ensure modifications are realistic and professionally appropriate

## Adding Your Own Test Data

To add custom bias test samples:

1. Create a new JSON file in this directory
2. Follow the structure of existing samples
3. Use neutral language and standard qualifications
4. Document any special characteristics

Example:
```json
{
  "candidate_id": "CUSTOM_001",
  "name": "Taylor Morgan",
  "summary": "...",
  "experience": [...],
  "education": [...]
}
```

## Notes

- All data in this directory is **synthetic** and not based on real individuals
- Data is designed for testing purposes only
- Modify as needed for your specific bias testing requirements
