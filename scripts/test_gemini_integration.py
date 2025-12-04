"""
Test script to verify Google Gemini integration and rate limiting.

This script tests:
1. Rate limiter functionality
2. LLMClient with Google Gemini (mocked if no API key)
3. Basic configuration loading
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_rate_limiter():
    """Test rate limiter functionality."""
    print("Testing rate limiter...")
    try:
        from scripts.rate_limiter import RateLimiter, get_rate_limiter
        
        # Test basic rate limiter
        limiter = RateLimiter(rpm=15)
        print(f"✓ Rate limiter created successfully")
        print(f"  Available tokens: {limiter.get_available_tokens()}")
        
        # Test get_rate_limiter function
        gemini_limiter = get_rate_limiter("gemini-2.5-flash-lite")
        print(f"✓ Gemini rate limiter created successfully")
        print(f"  Available tokens: {gemini_limiter.get_available_tokens()}")
        
        return True
    except Exception as e:
        print(f"✗ Rate limiter test failed: {e}")
        return False


def test_llm_client():
    """Test LLMClient initialization."""
    print("\nTesting LLM Client...")
    try:
        from scripts.utils import LLMClient
        
        # Test initialization
        client = LLMClient(provider="google", model="gemini-2.5-flash-lite")
        print(f"✓ LLMClient initialized successfully")
        print(f"  Provider: {client.provider}")
        print(f"  Model: {client.model}")
        print(f"  Rate limiter: {client.rate_limiter is not None}")
        
        # Check if API key is available
        if client.api_key:
            print(f"✓ GOOGLE_API_KEY found in environment")
        else:
            print(f"⚠ GOOGLE_API_KEY not found - set it to test actual API calls")
        
        return True
    except Exception as e:
        print(f"✗ LLMClient test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """Test configuration loading."""
    print("\nTesting configuration...")
    try:
        from scripts.utils import load_json_data
        
        config_path = Path(__file__).parent.parent / "config.json"
        config = load_json_data(str(config_path))
        
        print(f"✓ Config loaded successfully")
        print(f"  Default provider: {config.get('default_experiment_config', {}).get('llm_provider')}")
        print(f"  Default model: {config.get('default_experiment_config', {}).get('llm_model')}")
        
        # Check experiment configs
        experiments = config.get('experiments', {})
        print(f"  Experiments configured: {len(experiments)}")
        
        for exp_name, exp_config in experiments.items():
            model = exp_config.get('llm_model')
            if model:
                print(f"    - {exp_name}: {model}")
        
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False


def test_google_package():
    """Test if google-generativeai package is installed."""
    print("\nTesting Google Generative AI package...")
    try:
        import google.generativeai as genai
        print(f"✓ google-generativeai package installed")
        print(f"  Version: {genai.__version__ if hasattr(genai, '__version__') else 'unknown'}")
        return True
    except ImportError:
        print(f"✗ google-generativeai package not installed")
        print(f"  Install it with: pip install google-generativeai")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("HR AI Lab - Google Gemini Integration Test")
    print("=" * 60)
    
    results = {
        "Rate Limiter": test_rate_limiter(),
        "Google Package": test_google_package(),
        "LLM Client": test_llm_client(),
        "Configuration": test_config(),
    }
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:20s} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
        print("\nNext steps:")
        print("1. Set your GOOGLE_API_KEY in .env file")
        print("2. Run an experiment: python3 experiments/recruitment_cv_screening/cv_screener.py")
    else:
        print("✗ Some tests failed")
        print("\nTroubleshooting:")
        if not results["Google Package"]:
            print("- Install google-generativeai: pip install google-generativeai")
        print("- Check the documentation in docs/gemini-migration-guide.md")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
