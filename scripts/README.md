# Scripts Directory

This directory contains core utilities, dataset generators, and experiment runners for the HR AI Lab.

## Files

### `generate_datasets.py`
Generates synthetic HR datasets including CVs, interview transcripts, and performance notes.

**Usage:**
```bash
# Generate all default datasets
python generate_datasets.py --all

# Generate specific numbers of each type
python generate_datasets.py --cvs 20 --interviews 10 --performance 15

# Use custom random seed for reproducibility
python generate_datasets.py --all --seed 123
```

**Arguments:**
- `--all`: Generate all dataset types with default counts
- `--cvs N`: Generate N CVs (default: 10)
- `--interviews N`: Generate N interview transcripts (default: 5)
- `--performance N`: Generate N performance notes (default: 5)
- `--seed N`: Random seed for reproducible generation (default: 42)

### `utils.py`
Core utility functions including:
- **LLMClient**: Wrapper for LLM API calls (OpenAI, Anthropic, Azure)
- **Data Loading**: Functions to load datasets from JSON, CSV, and text files
- **Results Saving**: Save experiment outputs in various formats
- **Metrics**: Basic metric calculations
- **Path Helpers**: Functions to get project paths

### `run_experiment.py`
Main experiment runner script. Usage:
```bash
python run_experiment.py --experiment cv_screening --model gpt-4 --provider openai
```

Arguments:
- `--experiment`: Name of experiment to run
- `--config`: Path to config file (optional)
- `--model`: LLM model to use (default: gpt-4)
- `--provider`: LLM provider (openai, anthropic, azure)

### `evaluate.py`
Evaluation and benchmarking framework. Usage:
```bash
# Evaluate specific results
python evaluate.py results/cv_screening_20250604_120000.json

# Generate leaderboard
python evaluate.py
```

Features:
- Per-experiment evaluators
- Bias testing framework
- Model comparison
- Leaderboard generation

## Getting Started

1. Create and activate virtual environment:
```bash
# Create virtual environment
python3 -m venv ../.venv

# Activate virtual environment
source ../.venv/bin/activate  # On macOS/Linux
# OR
../.venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r ../requirements.txt
```

3. Set up environment variables:
```bash
cp ../.env.example ../.env
# Edit .env with your API keys
```

4. Run a test:
```bash
python utils.py  # Test utilities
```
