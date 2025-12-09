# Experiment F: Ethical AI Bias Testing Suite

## 🎯 Implementation Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                  BIAS TESTING AGENT (Experiment F)              │
│                 Foundational Framework for All                   │
│                                                                  │
│  Agent Capabilities:                                             │
│  • Autonomous test case generation                               │
│  • Counterfactual analysis                                       │
│  • Statistical bias detection                                    │
│  • Comprehensive reporting                                       │
│  • Mitigation recommendations                                    │
└─────────────────────────────────────────────────────────────────┘
                               │
                               │ Tests All Experiments
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
    ┌─────────────────┐ ┌─────────────┐ ┌──────────────┐
    │  Experiment A   │ │Experiment B │ │ Experiment C │
    │  CV Screening   │ │ Interview   │ │ Performance  │
    │                 │ │Summarization│ │   Reviews    │
    └─────────────────┘ └─────────────┘ └──────────────┘
              │                │                │
              └────────────────┼────────────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
          ┌────────────────┐    ┌─────────────────┐
          │  Experiment D  │    │ Experiments E-I │
          │Career Pathways │    │  Workflow, HR   │
          └────────────────┘    └─────────────────┘
```

## 📊 Bias Types Tested

| # | Bias Type | Test Method | Impact |
|---|-----------|-------------|--------|
| 1 | **Gender** | Name swaps, pronoun changes | HIGH |
| 2 | **Ethnicity** | Ethnically-identifiable names | HIGH |
| 3 | **Age** | Experience years, graduation dates | MEDIUM |
| 4 | **Name** | Combined gender/ethnicity testing | HIGH |
| 5 | **Education** | Prestigious vs standard universities | MEDIUM |
| 6 | **Geography** | Urban vs rural locations | LOW |
| 7 | **Employment Gap** | Career gap scenarios | MEDIUM |
| 8 | **Career Trajectory** | Non-linear path variations | LOW |

## 🔬 Testing Methodology

### Counterfactual Testing Approach

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Generate Paired Test Cases                         │
│                                                              │
│  Original:  Name: "Alex Johnson"                            │
│             University: "Harvard"                            │
│             Location: "San Francisco, CA"                    │
│                                                              │
│  Modified:  Name: "Lakisha Johnson"                         │
│             University: "Harvard"                            │
│             Location: "San Francisco, CA"                    │
│                                                              │
│  → Only ONE attribute changes (name = ethnicity signal)     │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: Run Experiment on Both Versions                     │
│                                                              │
│  Original Score:  0.85                                       │
│  Modified Score:  0.67                                       │
│                                                              │
│  → Difference: 0.18 (18%)                                   │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: Detect Bias                                         │
│                                                              │
│  Threshold: 0.05 (5%)                                        │
│  Difference: 0.18 (18%)                                      │
│                                                              │
│  ⚠️ BIAS DETECTED - Severity: MODERATE                      │
└─────────────────────────────────────────────────────────────┘
```

## 📁 File Structure

```
experiments/ethical_ai_bias_tests/
│
├── bias_testing_agent.py          # 🤖 Main agent (1,100+ lines)
│   ├── Class: BiasTestingAgent
│   ├── Enum: BiasType
│   ├── DataClass: BiasTestCase
│   ├── DataClass: BiasTestResult
│   └── Function: run_bias_analysis_on_experiment()
│
├── example_bias_test.py            # 📚 Usage examples (400+ lines)
│   ├── Example 1: Basic test generation
│   ├── Example 2: Full analysis
│   ├── Example 3: Custom scenarios
│   └── Example 4: Mitigation strategies
│
├── test_bias_agent.py              # ✅ Unit tests (350+ lines)
│   ├── Test: Agent initialization
│   ├── Test: Gender test cases
│   ├── Test: Ethnicity test cases
│   ├── Test: Education test cases
│   ├── Test: Age test cases
│   ├── Test: Severity calculation
│   └── Test: Report generation
│
├── __init__.py                     # 📦 Package interface
├── README.md                       # 📖 Full documentation (500+ lines)
└── QUICK_START.md                  # 🚀 Quick start guide

datasets/bias_test_samples/
│
├── sample_cv_for_bias_testing.json              # Neutral CV template
├── sample_interview_for_bias_testing.json       # Neutral interview
└── README.md                                     # Data documentation
```

**Total: 8 files, ~2,500 lines of code + documentation**

## ⚙️ Configuration

### Default Settings
```json
{
  "bias_testing": {
    "llm_provider": "google",
    "llm_model": "gemini-2.5-flash-lite",
    "bias_threshold": 0.05,
    "temperature": 0.3,
    "modifications": [
      "name_swap",
      "gender_swap", 
      "ethnicity_swap",
      "age_swap",
      "education_swap",
      "geography_swap",
      "employment_gap"
    ]
  }
}
```

### Configurable Parameters
- **bias_threshold**: Score difference to flag as bias (0.05 = 5%)
- **temperature**: LLM temperature for consistency (0.1-0.5)
- **modifications**: Which bias types to test
- **severity_levels**: Thresholds for none/low/moderate/high/critical

## 📊 Report Structure

```json
{
  "summary": {
    "total_tests": 120,
    "biased_tests": 18,
    "bias_rate": 0.15,
    "overall_assessment": "NEEDS IMPROVEMENT"
  },
  
  "by_bias_type": {
    "gender": {
      "total": 40,
      "biased": 6,
      "bias_rate": 0.15,
      "avg_difference": 0.072,
      "max_difference": 0.12,
      "severities": {
        "none": 34,
        "low": 4,
        "moderate": 2,
        "high": 0,
        "critical": 0
      }
    },
    "ethnicity": {...},
    "age": {...}
  },
  
  "critical_cases": [
    {
      "test_id": "ethnicity_Lakisha_Johnson",
      "bias_type": "ethnicity",
      "modification": "Name change: Emily Wilson -> Lakisha Johnson",
      "score_difference": 0.18,
      "severity": "moderate",
      "explanation": "..."
    }
  ],
  
  "recommendations": [
    "⚠️ High ethnicity bias detected (20.0% of tests)",
    "✓ Implement blind screening where possible",
    "✓ Use structured evaluation rubrics",
    ...
  ]
}
```

## 🎯 Usage Patterns

### Pattern 1: Quick Test Generation
```python
agent = BiasTestingAgent(config)
test_cases = agent.generate_test_cases(
    sample_cv,
    [BiasType.GENDER, BiasType.ETHNICITY]
)
# Returns: List of paired test cases ready to run
```

### Pattern 2: Complete Analysis
```python
report = run_bias_analysis_on_experiment(
    experiment_name="cv_screening",
    experiment_function=screener.screen_candidate,
    score_extractor=lambda r: r['score'],
    test_data=[cv1, cv2, cv3],
    bias_types=[BiasType.GENDER, BiasType.ETHNICITY, BiasType.AGE]
)
# Returns: Comprehensive bias report
```

### Pattern 3: Custom Testing
```python
agent = BiasTestingAgent(config)
test_cases = agent.generate_test_cases(cv, [BiasType.EMPLOYMENT_GAP])
results = agent.run_batch_tests(test_cases, my_function, score_extractor)
report = agent.generate_bias_report(results)
# Returns: Focused analysis of specific bias
```

## 🔐 Bias Detection Thresholds

| Score Difference | Severity | Action Required |
|-----------------|----------|-----------------|
| < 0.05 (5%) | **None** | ✅ Pass - Continue |
| 0.05 - 0.10 | **Low** | ⚠️ Monitor - Document |
| 0.10 - 0.20 | **Moderate** | 🔶 Investigate - Consider fixes |
| 0.20 - 0.30 | **High** | 🚨 Fix Required - Block deployment |
| > 0.30 (30%) | **Critical** | 🔴 Urgent - Do not deploy |

## 🛡️ Mitigation Strategies

### 1. Blind Screening
```python
# Remove protected attributes before processing
def blind_cv(cv):
    return {
        'skills': cv['skills'],
        'experience': cv['experience'],
        'achievements': cv['achievements']
        # NO name, gender, age, location
    }
```

### 2. Explicit Fairness Instructions
```python
prompt = """
Evaluate based SOLELY on qualifications.
Do NOT consider: gender, race, age, university prestige.
Focus ONLY on: skills, experience, achievements.
"""
```

### 3. Structured Rubrics
```python
rubric = {
    'technical_skills': {'weight': 0.4, 'score': 0-10},
    'experience': {'weight': 0.3, 'score': 0-10},
    'achievements': {'weight': 0.2, 'score': 0-10},
    'cultural_fit': {'weight': 0.1, 'score': 0-10}
}
# Reduces subjective bias
```

### 4. Regular Audits
```bash
# Run weekly
python test_all_experiments_for_bias.py --threshold 0.05
```

## 🏆 Success Criteria

| Metric | Target | Status |
|--------|--------|--------|
| Bias types covered | ≥ 6 | ✅ 8 types |
| Code quality | Production-ready | ✅ Error handling, logging |
| Documentation | Comprehensive | ✅ 500+ lines |
| Test coverage | Core functions | ✅ 7 unit tests |
| Integration | All experiments | ✅ Experiment-agnostic |
| Automation | Full | ✅ Single function call |
| Reporting | Multi-level | ✅ Summary + detailed |

## 🎓 Key Innovations

1. **Agent-Based Architecture**: Autonomous, self-directed bias testing
2. **Counterfactual Methodology**: Paired test cases for rigorous comparison
3. **Comprehensive Coverage**: 8 bias types across all experiments
4. **Statistical Rigor**: Thresholds, severity levels, confidence metrics
5. **Actionable Insights**: Specific recommendations for mitigation
6. **Production-Ready**: Enterprise-grade code quality and documentation

## 📈 Impact

### Risk Mitigation
- ✅ Prevents biased AI from reaching production
- ✅ Provides audit trail for compliance
- ✅ Reduces legal and reputational risk

### Ethical AI
- ✅ Systematic fairness validation
- ✅ Transparent bias measurement
- ✅ Continuous monitoring capability

### Best Practices
- ✅ Follows industry standards (Google, Microsoft)
- ✅ Reproducible methodology
- ✅ Scalable across experiments

## 🚀 Getting Started

```bash
# 1. Verify installation
python experiments/ethical_ai_bias_tests/test_bias_agent.py

# 2. Run examples
python experiments/ethical_ai_bias_tests/example_bias_test.py

# 3. Test your experiment
python -c "
from experiments.ethical_ai_bias_tests import *
agent = BiasTestingAgent(config)
# ... your test code
"
```

## 📚 Documentation

- **Quick Start**: `QUICK_START.md` (5-minute guide)
- **Full Documentation**: `README.md` (comprehensive reference)
- **Examples**: `example_bias_test.py` (4 detailed examples)
- **Tests**: `test_bias_agent.py` (verification)
- **Summary**: `docs/experiment-f-bias-testing-complete.md`

---

## ✅ Status: COMPLETE & PRODUCTION-READY

**Experiment F is fully implemented, tested, and documented.**

This bias testing framework is now the **foundational quality assurance tool** for all HR AI experiments in the lab. It ensures fairness, ethical compliance, and responsible AI development.

**Next Step**: Apply bias testing to Experiments A-I

---

*Implementation Date: December 9, 2024*  
*Version: 1.0.0*  
*Status: Production-Ready ✅*
