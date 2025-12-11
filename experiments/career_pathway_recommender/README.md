# Career Pathway Recommendation Engine (Experiment D)

## 🎯 Overview

The Career Pathway Recommendation Engine is an AI-powered system that helps employees discover their next career moves within the organization. It uses advanced NLP embeddings and large language models to match employee profiles with internal job roles, providing personalized recommendations with detailed explanations and actionable development plans.

**Key Features:**
- 🔍 **Smart Matching**: Uses sentence-transformers embeddings and FAISS for efficient semantic similarity search
- 🤖 **AI Explanations**: Leverages Google Gemini to generate personalized career advice
- 📈 **Development Plans**: Creates tailored 90-day learning roadmaps for each recommendation
- 📊 **Scalable**: Batch processing for organization-wide career planning
- ✅ **Evidence-Based**: Matches based on skills, experience, and career interests

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Employee Profile Input                        │
│  (Skills, Experience, Education, Interests, Certifications)      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              Embedding Generation (sentence-transformers)        │
│                    all-MiniLM-L6-v2 Model                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│          FAISS Vector Similarity Search (Cosine Distance)        │
│                Indexed Job Family Roles (All Levels)             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              Filter & Rank Candidate Roles                       │
│  - Similarity threshold (default: 0.7)                          │
│  - Career progression validation (experience level check)        │
│  - Top-K selection (default: 3)                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│        LLM Enhancement (Google Gemini 2.5 Flash-Lite)            │
│  - Generate personalized explanations                           │
│  - Create 90-day development plans                              │
│  - Identify skill gaps and learning resources                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Structured Recommendations                      │
│  - Top 3 roles with match scores                                │
│  - Detailed explanations                                        │
│  - Personalized development roadmaps                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📥 Input Format

### Employee Profile Schema

```json
{
  "employee_id": "EMP001",
  "name": "Alex Johnson",
  "current_title": "Software Engineer",
  "years_experience": 4,
  "skills": [
    "Python",
    "JavaScript",
    "React",
    "System Design",
    "Docker"
  ],
  "education_level": "Bachelor of Science in Computer Science",
  "certifications": [
    "AWS Certified Developer"
  ],
  "career_interests": [
    "Technical Leadership",
    "System Architecture",
    "Team Mentoring"
  ],
  "strengths": [
    "Problem Solving",
    "Technical Communication"
  ]
}
```

### Job Family Schema

Job families are loaded from `datasets/job_families/`:
- `job_family_software_engineering.json`
- `job_family_data_science.json`
- `job_family_product_management.json`

Each job family contains multiple career levels with:
- Title and level
- Years of experience required
- Required skills and nice-to-have skills
- Key responsibilities
- Promotion criteria
- Salary ranges

---

## 📤 Output Format

### Recommendation Result

```json
{
  "employee_id": "EMP001",
  "employee_name": "Alex Johnson",
  "current_title": "Software Engineer",
  "recommendations": [
    {
      "role": {
        "title": "Senior Software Engineer",
        "job_family": "Software Engineering",
        "level": 3,
        "years_experience": "5-8",
        "salary_range": "$130,000-$175,000",
        "required_skills": [...],
        "responsibilities": [...]
      },
      "similarity_score": 0.87,
      "explanation": "Your 4 years of experience and strong foundation in Python, JavaScript, and system design position you well for a Senior Software Engineer role...",
      "development_plan": {
        "month_1": {
          "focus": "Advanced system design and leadership fundamentals",
          "objectives": [
            "Master distributed systems patterns",
            "Begin technical leadership training"
          ],
          "activities": [...],
          "resources": [...],
          "success_metrics": [...]
        },
        "month_2": {...},
        "month_3": {...},
        "total_estimated_hours": 120
      }
    }
  ],
  "metadata": {
    "timestamp": "2025-12-12T10:30:00",
    "total_candidates_found": 5,
    "similarity_threshold": 0.7
  }
}
```

---

## 🚀 Quick Start

### Prerequisites

```bash
# Install required packages
pip install sentence-transformers faiss-cpu google-generativeai python-dotenv

# Or use requirements.txt
pip install -r requirements.txt
```

### Setup Environment

Create a `.env` file with your API key:

```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

Get a free API key from: https://ai.google.dev/

### Run the Experiment

**Option 1: Run with sample data**
```bash
cd experiments/career_pathway_recommender
python run_career_pathway.py
```

**Option 2: Run with custom employee data**
```bash
python run_career_pathway.py --employees ../../datasets/employee_profiles.json --top-k 5
```

**Option 3: Run as a module**
```bash
python career_recommender.py
```

### Using the Universal Runner

```bash
cd scripts
python run_experiment.py career_pathway_recommender
```

---

## 📊 Evaluation Metrics

The system tracks the following metrics:

| Metric | Description | Target |
|--------|-------------|--------|
| **Success Rate** | % of employees receiving recommendations | > 95% |
| **Average Similarity Score** | Mean cosine similarity of recommendations | > 0.75 |
| **Role Diversity** | Number of unique roles recommended | High variety |
| **Recommendations per Employee** | Average number of valid pathways | 2-3 |
| **Explanation Quality** | Human rating of explanation relevance | > 4/5 |
| **Plan Completeness** | % of plans with all 3 months populated | 100% |

### Sample Metrics Output

```json
{
  "total_employees": 4,
  "successful_recommendations": 4,
  "success_rate": 1.0,
  "average_similarity_score": 0.82,
  "unique_roles_recommended": 8,
  "recommendations_per_employee": 3.0
}
```

---

## 🔧 Configuration

Edit `config.json` to customize behavior:

```json
{
  "experiments": {
    "career_pathway": {
      "dataset": "job_families",
      "llm_model": "gemini-2.5-flash-lite",
      "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
      "vector_store": "faiss",
      "similarity_threshold": 0.7,
      "temperature": 0.7
    }
  }
}
```

**Key Parameters:**
- `similarity_threshold`: Minimum cosine similarity for recommendations (0.0-1.0)
- `embedding_model`: Sentence-transformers model name
- `temperature`: LLM creativity (0.0 = deterministic, 1.0 = creative)
- `vector_store`: Vector database type (faiss, pinecone, chromadb)

---

## 🧪 Algorithm Details

### 1. Text Embedding Generation

Employee profiles and job roles are converted to dense vector representations using sentence-transformers:

```python
# Employee profile → text representation
"Current Role: Software Engineer | Skills: Python, JavaScript, React | 
 Experience: 4 years | Interests: Technical Leadership, System Architecture"

# Encoded to 384-dimensional vector
embedding = model.encode(text)  # → [0.234, -0.567, 0.891, ...]
```

### 2. Vector Similarity Search

FAISS (Facebook AI Similarity Search) enables efficient k-nearest neighbor search:

```python
# Normalize vectors for cosine similarity
faiss.normalize_L2(embeddings)

# Build index with inner product
index = faiss.IndexFlatIP(dimension)
index.add(role_embeddings)

# Search for top-k similar roles
similarities, indices = index.search(employee_embedding, k=5)
```

### 3. Career Progression Validation

Not all similar roles are appropriate next steps:

```python
def is_valid_next_step(current_experience, role_requirement):
    # Allow stretch assignments (up to +2 years)
    # Prevent over-qualification gaps
    min_years, max_years = parse_requirement(role_requirement)
    return (current_experience >= min_years - 2) and 
           (current_experience <= max_years + 2)
```

### 4. LLM-Enhanced Explanations

Google Gemini generates contextual explanations:

```python
prompt = f"""
You are an expert career advisor. Explain why {employee_name} 
is a good fit for {role_title}.

Employee: {employee_profile}
Target Role: {role_details}

Provide:
1. Transferable skills analysis
2. Career interest alignment
3. Skill gaps and bridging strategies
"""
```

---

## 📈 Use Cases

### 1. **Annual Career Conversations**
Managers use recommendations to guide career development discussions with team members.

### 2. **Internal Mobility Programs**
HR teams identify cross-functional movement opportunities to retain talent.

### 3. **Succession Planning**
Leadership pipeline development by mapping high-potential employees to critical roles.

### 4. **Skills Gap Analysis**
Organization-wide identification of training needs based on recommended pathways.

### 5. **Retention Strategy**
Proactive career planning to reduce turnover by showing growth opportunities.

---

## 🛡️ Ethical Considerations

### Bias Mitigation
- **Skill-Based Matching**: Focuses on competencies, not demographics
- **Transparent Scoring**: Similarity scores visible to employees
- **Multiple Pathways**: Diverse recommendations prevent pigeonholing
- **Human Override**: Final decisions remain with employees and managers

### Privacy & Consent
- **Opt-In Model**: Employees control profile visibility
- **Data Minimization**: Only essential career-relevant data used
- **Anonymization**: Aggregated insights don't expose individual profiles

### Fairness Testing
Apply bias testing (Experiment F) to career recommendations:
```bash
python ../ethical_ai_bias_tests/test_bias.py --experiment career_pathway
```

Monitor for:
- Gender-based role steering
- Age discrimination in advancement recommendations
- Educational credential over-weighting

---

## 🔍 Example Output

```
================================================================================
CAREER PATHWAY RECOMMENDATIONS
================================================================================

Employee: Alex Johnson (EMP001)
Current Role: Software Engineer

Top 3 Recommended Career Paths:

1. Senior Software Engineer - Software Engineering
   Match Score: 87%
   Experience Required: 5-8 years
   Salary Range: $130,000-$175,000
   
   Explanation:
   Your 4 years of experience building scalable web applications with Python and
   JavaScript, combined with your demonstrated interest in system architecture,
   make you a strong candidate for a Senior Software Engineer role. Your AWS
   certification shows cloud infrastructure understanding, a key requirement...
   
   90-Day Development Plan:
   
   Month 1: Advanced system design and leadership fundamentals
   Objectives:
     • Master distributed systems patterns (CAP theorem, consistency models)
     • Begin technical leadership training through internal L&D program
   Activities:
     • Complete "Designing Data-Intensive Applications" coursework
     • Shadow senior engineers in architecture review meetings
   
   Month 2: Hands-on architecture and mentoring practice
   ...

2. Staff Software Engineer - Software Engineering
   Match Score: 78%
   ...

3. Engineering Manager - Software Engineering
   Match Score: 72%
   ...
```

---

## 🧩 Integration with Other Experiments

- **Experiment A (CV Screening)**: Use career pathways to assess external candidate fit
- **Experiment C (Performance Reviews)**: Link review outcomes to development plans
- **Experiment F (Bias Testing)**: Validate fairness of recommendations
- **Experiment H (Culture Coach)**: Align career paths with cultural values

---

## 🐛 Troubleshooting

### Common Issues

**1. FAISS Import Error**
```bash
# Install FAISS CPU version
pip install faiss-cpu

# For GPU support (optional)
pip install faiss-gpu
```

**2. Sentence-Transformers Model Download Fails**
```python
# Pre-download model
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
```

**3. Low Similarity Scores**
- Lower `similarity_threshold` in config.json (e.g., 0.6)
- Enrich employee profiles with more skills/details
- Use larger embedding model (e.g., all-mpnet-base-v2)

**4. Gemini API Quota Exceeded**
```
⚠️  Rate limit hit: 15 RPM exceeded
Solutions:
  1. Wait for quota reset (1 minute)
  2. Add delays between batch processing
  3. Upgrade to paid tier at https://ai.google.dev/
```

---

## 📚 References

- **Sentence-Transformers**: https://www.sbert.net/
- **FAISS Documentation**: https://github.com/facebookresearch/faiss
- **Google Gemini API**: https://ai.google.dev/docs
- **Career Development Theory**: Schein's Career Anchors, Holland Codes

---

## 🤝 Contributing

To extend this experiment:

1. **Add New Job Families**: Create JSON files in `datasets/job_families/`
2. **Custom Embedding Models**: Swap `embedding_model` in config.json
3. **Alternative Vector Stores**: Implement Pinecone or ChromaDB adapters
4. **Enhanced Filtering**: Add location, remote preferences, etc.

---

## 📄 License

See main repository LICENSE file.

---

## 🆘 Support

For issues or questions:
1. Check the [main repository README](../../README.MD)
2. Review [implementation plan](../../docs/implementation-plan.md)
3. Open an issue on GitHub

---

**Last Updated**: December 2025  
**Status**: ✅ Complete - Phase 2 (Experiment D)
