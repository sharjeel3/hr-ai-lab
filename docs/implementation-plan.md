# Implementation Strategy

Always work in the virtual environment .venv folder.


## Phase 1: Foundation (Tasks 1-3)

Set up complete directory structure matching the README
Build core utilities for LLM integration, data loading, and metrics
Generate synthetic datasets for testing without privacy concerns

## Phase 2: Core Experiments (Tasks 4-12)

Each of the 9 experiments should be implemented as standalone modules:

A-C: Recruitment pipeline (screening, interviews, reviews)
D-E: Employee development and workflow automation
F: Critical bias testing framework (foundational for all experiments)
G-I: Operational improvements (data quality, communication, routing)


## Phase 3: Evaluation & Visualization (Tasks 13-14)

Unified evaluation framework comparing LLM performance
Interactive dashboards for metrics and leaderboards

## Phase 4: Documentation & Deployment (Tasks 15-16)

Configuration management
Detailed per-experiment documentation

Key Technical Considerations
LLM Selection: Need to decide on models (OpenAI GPT-4, Claude, open-source alternatives?)
Embeddings: Career pathway recommender needs vector DB (Pinecone, ChromaDB, FAISS?)
Synthetic Data Quality: Critical for meaningful benchmarks
Evaluation Framework: Metrics need to be consistently measurable
Bias Testing: Should be applied across ALL experiments, not just Experiment F


## Complete TODO List:

1. Setup project structure and directories
2. Create synthetic datasets
3. Build core utility scripts
4. Implement CV Screening Benchmark (Experiment A)
5. Implement Interview Summarisation Agent (Experiment B)
6. Implement Performance Review Auto-Draft (Experiment C)
7. Implement Career Pathway Recommender (Experiment D)
8. Implement Workflow Agent Simulation (Experiment E)
9. Implement Ethical AI Bias Testing Suite (Experiment F)
10. Implement HRIS Data Quality Agent (Experiment G)
11. Implement Culture Transformation Coach (Experiment H)
12. Implement HR Request Routing Agent (Experiment I)
13. Create evaluation and benchmarking framework
14. Setup results dashboards and visualisation
15. Add configuration and environment setup
16. Document each experiment with detailed READMEs
