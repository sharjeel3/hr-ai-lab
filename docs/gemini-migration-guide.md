# Google Gemini Migration Guide

## Overview

This project has been migrated from OpenAI GPT-4 to **Google Gemini 2.5 Flash-Lite** (free tier) via the Google AI Studio API.

## Changes Made

### 1. Dependencies
- **Replaced**: `openai` and `anthropic` packages
- **Added**: `google-generativeai>=0.8.0`
- Update dependencies: `pip install -r requirements.txt`

### 2. Configuration
All experiments now use:
- **Provider**: `google`
- **Model**: `gemini-2.5-flash-lite`
- **Rate Limit**: 15 RPM (requests per minute)
- **Token Limit**: 250,000 TPM (tokens per minute)
- **Daily Limit**: 1,000 RPD (requests per day)

### 3. Rate Limiting
A new rate limiter has been implemented to respect Google's free tier limits:
- Automatically enforces 15 RPM for Gemini 2.5 Flash-Lite
- Uses token bucket algorithm for smooth rate limiting
- Supports different rate limits for different Gemini models
- Located in `scripts/rate_limiter.py`

### 4. API Key Setup
1. Get your Google API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a `.env` file based on `.env.example`
3. Set your API key:
   ```bash
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Supported Gemini Models (Free Tier)

The project supports all free tier Gemini models with automatic rate limiting:

| Model | RPM | TPM | RPD |
|-------|-----|-----|-----|
| Gemini 2.5 Pro | 2 | 125,000 | 50 |
| Gemini 2.5 Flash | 10 | 250,000 | 250 |
| Gemini 2.5 Flash-Lite | **15** | **250,000** | **1,000** |
| Gemini 2.0 Flash | 15 | 1,000,000 | 200 |
| Gemini 2.0 Flash-Lite | 30 | 1,000,000 | 200 |

**Default Model**: `gemini-2.5-flash-lite` (recommended for free tier)

## Usage

### Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

3. **Run experiments**:
   ```bash
   # CV Screening
   python3 experiments/recruitment_cv_screening/cv_screener.py
   
   # Interview Summarization
   python3 experiments/interview_summarisation/interview_summarizer.py
   
   # Performance Review
   python3 experiments/performance_review_drafter/review_drafter.py
   ```

### Using Different Models

To use a different Gemini model, update `config.json`:

```json
{
  "default_experiment_config": {
    "llm_provider": "google",
    "llm_model": "gemini-2.0-flash",  // Change model here
    "temperature": 0.7,
    "max_tokens": 1000
  }
}
```

### Rate Limiting

Rate limiting is automatically applied for all Google Gemini API calls:

```python
from scripts.utils import LLMClient

# Rate limiting is handled automatically
client = LLMClient(provider="google", model="gemini-2.5-flash-lite")
response = client.generate(prompt="Your prompt here")
```

### Manual Rate Limiter Usage

```python
from scripts.rate_limiter import get_rate_limiter

# Get rate limiter for specific model
limiter = get_rate_limiter("gemini-2.5-flash-lite")

# Wait for token availability before making API call
limiter.wait()
# Make your API call here

# Check available tokens
available = limiter.get_available_tokens()
print(f"Available tokens: {available}")
```

## Code Examples

### Basic LLM Call

```python
from scripts.utils import LLMClient

client = LLMClient(
    provider="google",
    model="gemini-2.5-flash-lite"
)

response = client.generate(
    prompt="Analyze this CV...",
    temperature=0.7,
    max_tokens=1000
)
print(response)
```

### Convenience Function

```python
from scripts.utils import call_llm

# Quick one-off call
response = call_llm(
    prompt="Your prompt here",
    model="gemini-2.5-flash-lite",
    provider="google",
    temperature=0.5
)
```

## Migration Benefits

1. **Cost**: Free tier with generous limits (1,000 requests/day)
2. **Performance**: Fast inference with Gemini 2.5 Flash-Lite
3. **Rate Limiting**: Built-in protection against rate limit errors
4. **Scalability**: Easy to upgrade to paid tier or different models
5. **Latest AI**: Access to Google's latest Gemini 2.5 models

## Troubleshooting

### API Key Issues
```bash
# Verify API key is set
echo $GOOGLE_API_KEY

# Or check in Python
python3 -c "import os; print(os.getenv('GOOGLE_API_KEY'))"
```

### Rate Limit Errors
If you hit rate limits:
- The rate limiter should prevent this automatically
- If it occurs, the system will wait and retry
- Consider reducing concurrent experiments
- Or upgrade to a paid tier for higher limits

### Import Errors
```bash
# Ensure package is installed
pip install google-generativeai

# Or reinstall all dependencies
pip install -r requirements.txt --upgrade
```

## Files Modified

1. `requirements.txt` - Updated dependencies
2. `config.json` - Changed default provider and model
3. `.env.example` - Updated API key configuration
4. `scripts/utils.py` - Added Google Gemini support
5. `scripts/rate_limiter.py` - New rate limiting module

## Backward Compatibility

Legacy OpenAI and Anthropic support is still available in the code:
- Set `provider: "openai"` to use OpenAI
- Set `provider: "anthropic"` to use Anthropic
- Add respective API keys to `.env`

However, you'll need to reinstall the legacy packages:
```bash
pip install openai anthropic
```

## Resources

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Rate Limits Documentation](https://ai.google.dev/pricing)
- [Python SDK Reference](https://ai.google.dev/tutorials/python_quickstart)

## Support

For issues or questions:
1. Check the [Google AI Studio](https://aistudio.google.com/) for API status
2. Review rate limits in your Google Cloud Console
3. Verify API key permissions and quota
