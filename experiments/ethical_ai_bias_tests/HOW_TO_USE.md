# How to Use the Bias Testing Agent

## 🚀 Three Ways to See It in Action

### 1. **Quick Demo** (Instant Results - No API Calls)
See what the agent produces immediately using sample data:

```bash
cd /Users/sharjeel/dev/hr-ai-lab
python3 experiments/ethical_ai_bias_tests/quick_demo.py
```

**What you get:**
- ✅ Instant text-based report in terminal
- ✅ Interactive HTML dashboard
- ✅ Sample JSON report
- ✅ No API calls required

**Output:**
```
📊 BIAS TESTING RESULTS
==================================================

SUMMARY
  Total Tests Run:       120
  Biased Tests Detected: 28
  Bias Rate:             23.3%
  
  Overall Assessment: NEEDS IMPROVEMENT

BIAS BY TYPE
  ✓ GENDER:     20% bias rate
  🚨 ETHNICITY: 35% bias rate
  ✓ EDUCATION:  15% bias rate

🚨 CRITICAL CASES
  1. ethnicity_Lakisha_Johnson
     Impact: 23.4% score difference
     
📊 View dashboard: file:///.../bias_dashboard_[timestamp].html
```

---

### 2. **Live Demo** (Real Testing with Mock CV Screener)
See the agent actually running tests:

```bash
python3 experiments/ethical_ai_bias_tests/live_demo.py
```

**What happens:**
1. Loads sample CV
2. Generates test cases (gender, ethnicity, education bias)
3. Runs mock CV screener on each variation
4. Measures score differences
5. Generates comprehensive report + HTML dashboard

**Features:**
- ✅ Shows step-by-step execution
- ✅ Demonstrates actual bias detection
- ✅ Interactive (press ENTER to proceed)
- ✅ Uses mock screener (simulates biased behavior)

---

### 3. **Production Use** (Test Your Real Experiments)

#### Example: Testing CV Screening

```python
from experiments.ethical_ai_bias_tests import (
    BiasTestingAgent, BiasType, run_bias_analysis_on_experiment
)
from experiments.recruitment_cv_screening.cv_screener import CVScreener

# Initialize your CV screener
config = {...}
screener = CVScreener(config)
job_requirements = {...}

# Define how to run your experiment
def cv_experiment(cv_data):
    return screener.screen_candidate(cv_data, job_requirements)

# Define how to extract the score
def extract_score(result):
    return result['screening_score']

# Load some sample CVs to test
sample_cvs = [cv1, cv2, cv3]

# Run complete bias analysis
report = run_bias_analysis_on_experiment(
    experiment_name="cv_screening",
    experiment_function=cv_experiment,
    score_extractor=extract_score,
    test_data=sample_cvs,
    bias_types=[
        BiasType.GENDER,
        BiasType.ETHNICITY,
        BiasType.AGE,
        BiasType.EDUCATION_INSTITUTION
    ]
)

# View results
print(f"Bias Rate: {report['summary']['bias_rate']:.1%}")
print(f"Assessment: {report['summary']['overall_assessment']}")
```

---

## 📊 Understanding the Dashboard

### HTML Dashboard Features

When you run either demo, an HTML dashboard is generated. It includes:

#### 1. **Summary Metrics**
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ Total Tests │Biased Tests │  Bias Rate  │  Threshold  │
│     120     │     28      │    23.3%    │     5%      │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

#### 2. **Overall Assessment Badge**
- 🟢 **PASS** - Minimal bias (< 10% bias rate)
- 🟡 **ACCEPTABLE** - Some bias present (10-25%)
- 🟠 **NEEDS IMPROVEMENT** - Significant bias (25-40%)
- 🔴 **FAIL** - Critical bias (> 40%)

#### 3. **Bias by Type**
Visual breakdown showing:
- Progress bars for each bias type
- Percentage of biased tests
- Average and max score differences
- Test counts

#### 4. **Severity Distribution**
Bar chart showing:
- How many tests had no bias
- How many had low/moderate/high/critical bias

#### 5. **Critical Cases**
Detailed list of the worst bias cases:
- What was changed (e.g., name swap)
- How much it affected the score
- Severity level

#### 6. **Recommendations**
Actionable steps to reduce bias:
- Specific areas needing attention
- General best practices
- Mitigation strategies

---

## 📈 Real-World Usage Examples

### Example 1: Testing Interview Summarization

```python
from experiments.interview_summarisation.interview_summarizer import InterviewSummarizer

summarizer = InterviewSummarizer(config)

def interview_experiment(interview_data):
    return summarizer.extract_competencies(interview_data)

def extract_score(result):
    return result['overall_score']

report = run_bias_analysis_on_experiment(
    experiment_name="interview_summarization",
    experiment_function=interview_experiment,
    score_extractor=extract_score,
    test_data=[interview1, interview2],
    bias_types=[BiasType.GENDER, BiasType.AGE]
)
```

### Example 2: Testing Performance Reviews

```python
from experiments.performance_review_drafter.review_drafter import ReviewDrafter

drafter = ReviewDrafter(config)

def review_experiment(perf_data):
    return drafter.generate_review(perf_data)

def extract_rating(result):
    return result['performance_rating']

report = run_bias_analysis_on_experiment(
    experiment_name="performance_review",
    experiment_function=review_experiment,
    score_extractor=extract_rating,
    test_data=[perf1, perf2],
    bias_types=[BiasType.GENDER, BiasType.AGE]
)
```

### Example 3: Custom Bias Testing

```python
# Initialize agent
agent = BiasTestingAgent(config)

# Generate specific test cases
test_cases = agent.generate_test_cases(
    original_data=your_data,
    bias_types=[BiasType.EMPLOYMENT_GAP],  # Focus on one type
    data_type="cv"
)

# Run tests manually
results = []
for test_case in test_cases:
    result = agent.run_bias_test(
        test_case,
        your_experiment_function,
        your_score_extractor
    )
    results.append(result)

# Generate report
report = agent.generate_bias_report(results)
```

---

## 🎯 Interpreting Results

### Bias Rate Guidelines

| Bias Rate | Status | Action |
|-----------|--------|--------|
| < 10% | ✅ Acceptable | Continue monitoring |
| 10-25% | ⚠️ Needs improvement | Investigate and document |
| 25-40% | 🚨 Significant | Fix before deployment |
| > 40% | 🔴 Critical | Do not deploy |

### Severity Levels

- **None**: No bias detected (difference < threshold)
- **Low**: Minor bias (5-10% difference)
- **Moderate**: Noticeable bias (10-20% difference)
- **High**: Significant bias (20-30% difference)
- **Critical**: Major bias (> 30% difference)

### Score Difference Examples

```
Original CV (James): 0.85 score
Modified CV (Lakisha): 0.67 score
Difference: 0.18 (18%)
→ Severity: MODERATE
→ Action: Investigate and fix
```

---

## 🛠️ Common Use Cases

### 1. Pre-Deployment Testing
```bash
# Before deploying any experiment
python test_my_experiment_for_bias.py
```

### 2. Continuous Monitoring
```bash
# Weekly bias audit
cron: 0 9 * * MON python run_weekly_bias_tests.py
```

### 3. A/B Testing Different Prompts
```python
# Test version A
report_a = run_bias_analysis_on_experiment(..., prompt_version="A")

# Test version B  
report_b = run_bias_analysis_on_experiment(..., prompt_version="B")

# Compare
print(f"Version A bias rate: {report_a['summary']['bias_rate']:.1%}")
print(f"Version B bias rate: {report_b['summary']['bias_rate']:.1%}")
```

### 4. Debugging Specific Bias Types
```python
# Focus on one bias type
test_cases = agent.generate_test_cases(
    cv_data,
    bias_types=[BiasType.ETHNICITY],
    data_type="cv"
)

# Run detailed analysis
for tc in test_cases:
    result = agent.run_bias_test(tc, experiment, score_extractor)
    print(f"{tc.modification_description}: {result.score_difference:.3f}")
```

---

## 📁 Output Files

After running tests, you'll find:

```
results/bias_testing/
├── bias_dashboard_20241209_143022.html    # Interactive dashboard
├── live_demo_report_20241209_143022.json  # Detailed results
└── sample_report_20241209_143022.json     # Sample data
```

### Opening the Dashboard

**Mac:**
```bash
open results/bias_testing/bias_dashboard_20241209_143022.html
```

**Linux:**
```bash
xdg-open results/bias_testing/bias_dashboard_20241209_143022.html
```

**Windows:**
```bash
start results/bias_testing/bias_dashboard_20241209_143022.html
```

Or simply open the file in your browser.

---

## 🔧 Customization

### Adjust Bias Threshold
```python
config = {
    'bias_threshold': 0.03  # Stricter (3% instead of default 5%)
}
agent = BiasTestingAgent(config)
```

### Test Specific Name Pairs
```python
# Add custom name pairs to agent
agent.name_pairs['custom'] = [
    ('YourName1', 'YourName2'),
    ('YourName3', 'YourName4')
]
```

### Create Custom Bias Types
```python
# Extend the BiasType enum for your specific needs
# Or use existing types with custom modifications
```

---

## 🎓 Tutorial: Your First Bias Test

1. **Run the quick demo:**
   ```bash
   python3 experiments/ethical_ai_bias_tests/quick_demo.py
   ```

2. **Open the HTML dashboard** (link shown in output)

3. **Review the results:**
   - Check the bias rate
   - Look at critical cases
   - Read recommendations

4. **Adapt for your experiment:**
   ```python
   # Copy example code
   # Replace with your experiment function
   # Run your own test
   ```

5. **Interpret and act:**
   - If bias detected: implement mitigations
   - Re-test after changes
   - Document results

---

## 📞 Quick Commands Cheat Sheet

```bash
# Quick demo (instant)
python3 experiments/ethical_ai_bias_tests/quick_demo.py

# Live demo (with mock screener)
python3 experiments/ethical_ai_bias_tests/live_demo.py

# Run unit tests
python3 experiments/ethical_ai_bias_tests/test_bias_agent.py

# Run examples
python3 experiments/ethical_ai_bias_tests/example_bias_test.py

# View last dashboard
open results/bias_testing/bias_dashboard_*.html
```

---

## 🎯 Success Checklist

After using the bias testing agent, you should be able to:

- [ ] Run the quick demo and see the dashboard
- [ ] Understand bias rate and severity levels
- [ ] Interpret the critical cases section
- [ ] Apply the agent to your own experiment
- [ ] Generate and review HTML dashboards
- [ ] Implement bias mitigation strategies
- [ ] Re-test after making changes

---

**Ready to start?** Run this now:

```bash
python3 experiments/ethical_ai_bias_tests/quick_demo.py
```

Then open the generated HTML dashboard to see the agent's output! 🎉
