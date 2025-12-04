
# HR AI Lab — Experiments, Benchmarks & Responsible AI Framework

A collection of **practical, reproducible, HR-domain AI experiments** aligned with a vision for transforming People & Culture through AI.  
This repository demonstrates how an AI Engineer can build **scalable, ethical,
human-centric workforce tools** across recruitment, performance, career pathways,
and workflow automation.

**Note:**
- This project used AI for production of the source code and documentation

**🚀 Now powered by Google Gemini 2.5 Flash-Lite (Free Tier)**
- All experiments use Google's latest Gemini models
- Built-in rate limiting for free tier (15 RPM)
- No API costs for experimentation
- See [Gemini Migration Guide](docs/gemini-migration-guide.md) for details

---

## 📁 Repository Structure

```
hr-ai-lab/
│
├── experiments/
│   ├── recruitment_cv_screening/
│   ├── interview_summarisation/
│   ├── performance_review_drafter/
│   ├── career_pathway_recommender/
│   ├── workflow_agent_simulation/
│   ├── ethical_ai_bias_tests/
│   ├── hris_data_quality_agent/
│   ├── culture_transformation_coach/
│   └── request_routing_agent/
│
├── datasets/
│   ├── synthetic_cvs/
│   ├── interview_transcripts/
│   ├── performance_notes/
│   ├── job_families/
│   └── hris_samples/
│
├── scripts/
│   ├── run_experiment.py
│   ├── evaluate.py
│   └── utils.py
│
└── results/
├── leaderboard.csv
└── dashboards/

```

---

# 🌟 Overview of Experiments
Each experiment includes:

- Purpose  
- Inputs & outputs  
- Sample prompts  
- Metrics & evaluation  
- Expected results  
- Ethical considerations  
- Diagram of flow  

---


# A. **CV Screening Benchmark (Recruitment Automation)**

### 🎯 Goal  
Benchmark multiple LLMs for automated CV parsing & ranking while ensuring fairness.

### 📥 Inputs  
- 20–50 anonymised or synthetic CVs  
- Target role descriptions  
- Skills ontology for an organisation (synthetic example provided)

### 📤 Outputs  
- Structured JSON  
- Candidate-job similarity ranking  
- Evidence-backed reasoning

### 🧪 Prompts  
```text
Extract the following fields from this CV:
- Skills (mapped to ontology)
- Years of experience
- Certifications
- Projects with outcomes
Return JSON only.
```

### 📊 Metrics

| Metric              | Definition                                        |
| ------------------- | ------------------------------------------------- |
| Extraction Accuracy | % of fields correctly extracted                   |
| Evidence Alignment  | Output must reference CV text, not hallucinations |
| Fairness Check      | Compare outputs with name/identity removed        |
| Latency             | ms per CV                                         |
| Cost                | tokens per CV                                     |

### 🖼 Diagram

```
PDF/DOCX CV → LLM Parser → Structured JSON → Ranking Engine → Report
```

### ✅ Expected Output

```json
{
  "name": "Candidate A",
  "skills": ["Bridge Design", "Revit"],
  "experience_years": 5,
  "fit_score": 0.83,
  "evidence": [
    "Worked on XYZ bridge reinforcement project in 2022"
  ]
}
```

---

# B. **Interview Summarisation Agent**

### 🎯 Goal

Generate structured hiring summaries from interview transcripts.

### 📥 Inputs

* Transcripts (synthetic 10–20)
* Organisation's competency rubric

### 📤 Outputs

* Behavioural evidence
* STAR-format examples
* Hiring recommendation with justification

### 🧪 Prompt Example

```text
Summarise this interview using the STAR method.
Identify evidence for each competency.
Do not invent information. Cite transcript lines.
```

### 📊 Metrics

* Consistency (same transcript → same output)
* Evidence correctness
* Bias testing (swap candidate names)

### 📈 Expected Output

* 4–6 competency ratings
* 3 STAR examples
* Recommendation with risk flags

---

# C. **Performance Review Auto-Draft Assistant**

### 🎯 Goal

Convert monthly manager notes into ready-to-use Workday performance drafts.

### 📥 Inputs

* Manager notes (free text)
* Goal descriptions
* Competency library

### 📤 Outputs

* Strengths summary
* Improvement opportunities
* Workday form fields

### 🧪 Prompt

```text
Convert these check-in notes into a performance summary.
Use a neutral, professional tone.
Extract behaviour-based examples only.
```

### 📊 Metrics

* Manager satisfaction rating
* Coherence score
* Compliance (no value judgments, no bias)

---

# D. **Career Pathway Recommendation Engine**

### 🎯 Goal

Recommend internal roles based on skills similarity + growth alignment.

### 📥 Inputs

* Employee skill profile
* Internal job families
* Learning modules

### 📤 Outputs

* Top 3 next roles
* Explanation for each recommendation
* 90-day development plan

### 🧪 Algorithm

* Convert profiles + roles into embeddings
* Rank by cosine similarity
* Feed role shortlist into LLM for explanation/growth plan

### 🧪 Prompt

```text
Explain why this employee is a good fit for these internal roles.
Generate personalised learning steps.
```

### 📊 Metrics

* Similarity accuracy
* Diversity of suggestions
* Explanation quality rating

---

# E. **HR Workflow Agent Simulation (Workday → Teams → Copilot)**

### 🎯 Goal

Simulate cross-platform workflow automation.

### Example Scenario

**Event:** “New hire onboarded in Workday.”
**Outputs:**

* Teams message
* Calendar invites
* Onboarding checklist
* Copilot-ready summary

### 🧪 Prompt Example

```text
Generate a welcome message for Teams.
Create a checklist for the hiring manager.
Propose calendar reminders.
Return JSON with UI-ready fields.
```

### 📊 Metrics

* Latency
* Task completeness
* Formatting correctness

---

# F. **Ethical AI Bias Stress Test Suite**

### 🎯 Goal

Test HR prompts for fairness across sensitive attributes.

### 📥 Inputs

* CVs, interview transcripts
* Name-flip variations
* Cultural background variations

### 📤 Outputs

* Bias report
* Suggested mitigations
* Guardrail prompts

### 🧪 Guardrail Prompt

```text
You must not use gender, ethnicity, or unrelated personal traits
to infer job suitability. Base all decisions strictly on evidence
in text. If uncertain, return "insufficient data".
```

### 📊 Metrics

* Output variance across identity-swaps
* Violation rate
* Guardrail effectiveness

### 📈 Expected Output

Bias deltas, e.g.:

```
Fit score (original): 0.78  
Fit score (name swapped): 0.77   → ✔ Acceptable  
```

---

# G. **HRIS Data Quality Agent**

### 🎯 Goal

Detect and fix HRIS inconsistencies.

### 📥 Inputs

* Synthetic HRIS CSV
* Example anomalies

### 📤 Outputs

* Suggested corrections
* Risk implications
* Confidence scores

### 🧪 Example Prompt

```text
Identify errors in this HRIS dataset row.
Suggest corrections and explain potential downstream impacts.
```

### 📊 Metrics

* Error detection rate
* Correction quality
* Human QA agreement score

---

# H. **Culture Transformation Coach (Copilot Etiquette Assistant)**

### 🎯 Goal

Improve communication safety & clarity across Teams / email.

### 📥 Inputs

* Synthetic manager communications
* Psychological safety tone guidelines

### 📤 Outputs

* Improved rewrite
* Justification
* Safety score

### 🧪 Prompt

```text
Rewrite this message to be clear, constructive, and psychologically safe.
```

### 📊 Metrics

* Toxicity score reduction
* Clarity improvement
* Readability improvements (Flesch score)

---

# I. **HR Request Routing Agent (Autonomous HR Assistant)**

### 🎯 Goal

Classify HR requests and take action.

### Example Inputs

* “I need parental leave info”
* “I want to hire a structural engineer”
* “My performance cycle is missing”

### Outputs

* Request category
* Required documents
* Policy link
* Next steps
* Escalation logic

### 🧪 Prompt

```text
Classify this request into one of 12 HR categories.
Provide steps the user should take.
```

### 📊 Metrics

* Classification accuracy
* Completion rate
* Error rate

---

# 🛡 Responsible AI & Governance

### Principles embedded in all experiments:

* No unvalidated hiring recommendations
* No inferences based on sensitive attributes
* Evidence-only reasoning
* Human-in-the-loop for high-impact decisions
* Transparency: show *why* a model recommended something
* Drift monitoring: regular bias checks

---

# 🧩 Example Minimal Script (`scripts/run_experiment.py`)

```python
import json
from utils import call_llm, load_dataset

def run_cv_experiment():
    cvs = load_dataset("datasets/synthetic_cvs/")
    results = []

    for cv in cvs:
        output = call_llm(
            prompt=f"Extract fields:\n{cv['text']}",
            model="gpt-4.1-mini"
        )
        results.append(output)

    with open("results/cv_screening.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_cv_experiment()
```

---

# 📌 Summary

This repository demonstrates:

* Practical AI engineering
* Responsible AI
* HR domain understanding
* Systems thinking
* Integration thinking (Workday / M365 / Copilot)
* Culture transformation vision
* Benchmarking discipline

---

# 🚀 Quick Start

### Automated Setup (Recommended)

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### Manual Setup

1. **Create virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# OR: .venv\Scripts\activate  # Windows
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure Google Gemini API key:**
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY from https://aistudio.google.com/app/apikey
```

4. **Run your first experiment:**
```bash
# CV Screening
python3 experiments/recruitment_cv_screening/cv_screener.py

# Or use the experiment runner
python scripts/run_experiment.py --experiment cv_screening --model gemini-2.5-flash-lite
```

5. **View results:**
```bash
python scripts/evaluate.py
```

### Project Structure

- `experiments/` - Individual experiment modules (9 total)
- `datasets/` - Synthetic datasets for testing
- `scripts/` - Core utilities and runners
- `results/` - Experiment outputs and leaderboards
- `docs/` - Documentation and implementation plans

### Rate Limiting

All experiments automatically respect Google Gemini's free tier rate limits:
- **15 RPM** (requests per minute) for Gemini 2.5 Flash-Lite
- **250,000 TPM** (tokens per minute)
- **1,000 RPD** (requests per day)

Rate limiting is handled transparently by the `LLMClient` class.

See [scripts/README.md](scripts/README.md) for detailed usage instructions.


