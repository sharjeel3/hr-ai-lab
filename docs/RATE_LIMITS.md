# Google Gemini API - Rate Limits Quick Reference

## Free Tier Rate Limits

### Gemini 2.5 Flash-Lite (DEFAULT - Recommended)
```
RPM (Requests Per Minute):  15
TPM (Tokens Per Minute):    250,000
RPD (Requests Per Day):     1,000
```
**Best for**: Most experiments, high daily usage

### Gemini 2.5 Flash
```
RPM:  10
TPM:  250,000
RPD:  250
```
**Best for**: Higher quality outputs, lower daily needs

### Gemini 2.5 Pro
```
RPM:  2
TPM:  125,000
RPD:  50
```
**Best for**: Complex reasoning tasks, premium quality

### Gemini 2.0 Flash
```
RPM:  15
TPM:  1,000,000
RPD:  200
```
**Best for**: High token throughput, moderate daily usage

### Gemini 2.0 Flash-Lite
```
RPM:  30
TPM:  1,000,000
RPD:  200
```
**Best for**: Highest request frequency, moderate daily usage

## How Rate Limiting Works in This Project

### Automatic Rate Limiting
All API calls are automatically rate-limited based on the model you choose:

```python
from scripts.utils import LLMClient

# Rate limiting happens automatically
client = LLMClient(provider="google", model="gemini-2.5-flash-lite")
response = client.generate(prompt="Your prompt")
```

### Token Bucket Algorithm
- Tokens refill at a constant rate (based on RPM)
- Each API call consumes one token
- If no tokens available, the system waits
- Smooth distribution of requests over time

### Thread-Safe
- Safe to use in multi-threaded applications
- Shared rate limiter per model
- Prevents race conditions

## Estimating Usage

### Example: CV Screening with 50 CVs
```
Model: gemini-2.5-flash-lite
RPM: 15 requests/minute

If each CV requires 1 API call:
- 50 CVs = 50 API calls
- Time needed: 50 / 15 = ~3.4 minutes
- Daily capacity: 1,000 / 50 = 20 batches
```

### Example: Interview Summarization with 20 Interviews
```
Model: gemini-2.5-flash-lite
RPM: 15 requests/minute

If each interview requires 2 API calls (analysis + summary):
- 20 interviews = 40 API calls
- Time needed: 40 / 15 = ~2.7 minutes
- Daily capacity: 1,000 / 40 = 25 batches
```

## Switching Models

### In config.json
```json
{
  "default_experiment_config": {
    "llm_provider": "google",
    "llm_model": "gemini-2.0-flash",  // Change here
    "temperature": 0.7,
    "max_tokens": 1000
  }
}
```

### In Code
```python
# Use a different model
client = LLMClient(
    provider="google",
    model="gemini-2.5-flash"  // Specify model
)
```

The rate limiter automatically adjusts based on the model!

## Handling Rate Limits

### Built-in Waiting
The system automatically waits when rate limits are hit:
```python
# This will automatically wait if needed
client.generate(prompt="Your prompt")
```

### Check Available Tokens
```python
from scripts.rate_limiter import get_rate_limiter

limiter = get_rate_limiter("gemini-2.5-flash-lite")
available = limiter.get_available_tokens()
print(f"Can make {int(available)} requests now")
```

### Manual Control
```python
from scripts.rate_limiter import get_rate_limiter

limiter = get_rate_limiter("gemini-2.5-flash-lite")

# Try to acquire without blocking
if limiter.acquire(block=False):
    # Make API call
    response = client.generate(prompt)
else:
    print("Rate limit reached, try again later")

# Or acquire with timeout
if limiter.acquire(block=True, timeout=10):
    # Make API call within 10 seconds
    response = client.generate(prompt)
```

## Tips for Staying Within Limits

1. **Use Flash-Lite for experiments** - 15 RPM and 1,000 RPD
2. **Batch processing** - Process multiple items in sequence
3. **Cache results** - Save outputs to avoid re-processing
4. **Monitor usage** - Check your quota at https://aistudio.google.com/
5. **Use appropriate temperature** - Lower temperature = more consistent tokens
6. **Set max_tokens wisely** - Don't request more than needed

## Upgrading to Paid Tier

If you need higher limits:

1. Visit: https://ai.google.dev/pricing
2. Enable billing in Google Cloud Console
3. Rate limits increase significantly
4. Pay only for what you use

### Paid Tier Example Limits (Approximate)
```
Model: gemini-2.5-flash-lite
RPM: 1,000+ (vs 15 free)
TPM: 4,000,000+ (vs 250,000 free)
RPD: Unlimited (vs 1,000 free)
```

## Error Messages

### Rate Limit Exceeded (429)
```
"Rate limit exceeded. Please try again later."
```
**Solution**: Built-in rate limiter prevents this, but if you see it:
- Wait 60 seconds and retry
- Check if multiple processes are running
- Verify rate limiter is working

### Quota Exceeded (429)
```
"Daily quota exceeded."
```
**Solution**:
- Wait until next day (resets at midnight PT)
- Upgrade to paid tier
- Optimize to use fewer requests

### Invalid API Key (401)
```
"Invalid API key."
```
**Solution**:
- Check `.env` file has `GOOGLE_API_KEY`
- Verify key from https://aistudio.google.com/app/apikey
- No extra spaces or quotes in `.env`

## Monitoring Usage

### Google AI Studio Dashboard
Visit: https://aistudio.google.com/

See:
- Current usage
- Remaining quota
- Request history
- Error logs

### In Your Code
```python
import logging
logging.basicConfig(level=logging.INFO)

# Rate limiter logs when waiting
# Look for messages like:
# "Rate limit reached, waiting..."
```

## Quick Reference Table

| Need | Recommended Model | RPM | Daily Quota |
|------|-------------------|-----|-------------|
| High volume testing | gemini-2.5-flash-lite | 15 | 1,000 |
| Quality outputs | gemini-2.5-flash | 10 | 250 |
| Premium quality | gemini-2.5-pro | 2 | 50 |
| Max throughput | gemini-2.0-flash-lite | 30 | 200 |
| Balanced | gemini-2.0-flash | 15 | 200 |

---

**Current Default**: `gemini-2.5-flash-lite` (15 RPM, 1,000 RPD)

**Recommended for most use cases**: Provides good balance of speed, quality, and daily quota.
