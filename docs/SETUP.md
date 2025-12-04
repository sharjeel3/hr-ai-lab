# Setup Instructions for HR AI Lab with Google Gemini

This guide will help you set up the HR AI Lab project to use Google's Gemini API (free tier).

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A Google account (for API key)

## Step-by-Step Setup

### 1. Get Your Google API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key (keep it secure!)

### 2. Clone or Download the Repository

```bash
cd ~/dev
git clone <repository-url> hr-ai-lab
cd hr-ai-lab
```

### 3. Create Python Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

You should see `(.venv)` in your terminal prompt.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `google-generativeai` - Google Gemini API client
- `pandas`, `numpy` - Data processing
- `sentence-transformers` - Embeddings
- `scikit-learn` - Metrics
- And other dependencies

### 5. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Google API key:
   ```bash
   # macOS/Linux
   nano .env
   
   # Or use any text editor
   code .env
   ```

3. Update the file:
   ```env
   GOOGLE_API_KEY=your_actual_api_key_here
   DEFAULT_LLM_PROVIDER=google
   DEFAULT_LLM_MODEL=gemini-2.5-flash-lite
   ```

### 6. Test the Installation

Run the test script to verify everything is working:

```bash
python3 scripts/test_gemini_integration.py
```

You should see all tests pass:
```
✓ Rate Limiter       PASSED
✓ Google Package     PASSED
✓ LLM Client         PASSED
✓ Configuration      PASSED
```

### 7. Run Your First Experiment

Try the CV screening experiment:

```bash
python3 experiments/recruitment_cv_screening/cv_screener.py
```

Or the interview summarization:

```bash
python3 experiments/interview_summarisation/interview_summarizer.py
```

## Verification Checklist

- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip list | grep google-generativeai`)
- [ ] Google API key obtained from AI Studio
- [ ] `.env` file created with `GOOGLE_API_KEY`
- [ ] Test script passes all checks
- [ ] First experiment runs successfully

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'google'"

**Solution:**
```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install google-generativeai
```

### Issue: "GOOGLE_API_KEY not found in environment variables"

**Solution:**
1. Check `.env` file exists in project root
2. Verify the file contains: `GOOGLE_API_KEY=your_key_here`
3. Make sure no extra spaces around the `=` sign
4. Restart your terminal or reload environment

### Issue: Rate limit errors (429 status code)

**Solution:**
- The project has built-in rate limiting (15 RPM)
- If you still hit limits, reduce concurrent experiments
- Wait a minute and try again
- Check your quota at [Google AI Studio](https://aistudio.google.com/)

### Issue: "Import Error" when running experiments

**Solution:**
```bash
# Make sure you're in the project root directory
cd /path/to/hr-ai-lab

# Verify directory structure
ls -la scripts/

# Run from project root
python3 experiments/recruitment_cv_screening/cv_screener.py
```

### Issue: Permission denied on setup.sh

**Solution:**
```bash
chmod +x setup.sh
./setup.sh
```

## Free Tier Limits

Remember the Google Gemini free tier limits:

| Metric | Gemini 2.5 Flash-Lite | Description |
|--------|----------------------|-------------|
| **RPM** | 15 | Requests per minute |
| **TPM** | 250,000 | Tokens per minute |
| **RPD** | 1,000 | Requests per day |

The project automatically respects these limits through built-in rate limiting.

## Next Steps

1. **Explore Experiments**: Check out the 9 different HR AI experiments in the `experiments/` folder
2. **Read Documentation**: See `docs/` for detailed guides and implementation plans
3. **Review Datasets**: Explore `datasets/` for sample data
4. **Check Results**: Run experiments and view outputs in `results/`

## Getting Help

- **Migration Guide**: See [docs/gemini-migration-guide.md](gemini-migration-guide.md)
- **Main README**: See [README.MD](../README.MD)
- **Google Gemini Docs**: https://ai.google.dev/docs
- **API Issues**: Check [Google AI Studio](https://aistudio.google.com/)

## Upgrading to Paid Tier

If you need higher limits:

1. Visit [Google AI Studio Pricing](https://ai.google.dev/pricing)
2. Enable billing in your Google Cloud project
3. Upgrade your API key
4. Update `config.json` to use faster models if desired:
   - `gemini-2.0-flash` (15 RPM → higher with paid tier)
   - `gemini-2.5-flash` (10 RPM → higher with paid tier)

The code will automatically adjust rate limits based on the model you choose.

---

**Ready to go?** Run your first experiment:
```bash
python3 experiments/recruitment_cv_screening/cv_screener.py
```
