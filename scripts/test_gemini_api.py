#!/usr/bin/env python3
"""Test Google Gemini API directly to verify model and API key."""

import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

try:
    import google.generativeai as genai
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in .env file")
        exit(1)
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Configure
    genai.configure(api_key=api_key)
    
    # List available models
    print("\n📋 Available Gemini models:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"  - {model.name}")
    
    # Test with different model names
    test_models = [
        "gemini-2.5-flash-lite",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-pro"
    ]
    
    print("\n🧪 Testing models:")
    for model_name in test_models:
        try:
            print(f"\nTesting: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'Hello, I am working!' in JSON format: {\"message\": \"your message\"}")
            print(f"  ✅ Works! Response: {response.text[:100]}")
            break
        except Exception as e:
            print(f"  ❌ Failed: {str(e)[:100]}")
    
except ImportError:
    print("❌ google-generativeai not installed")
    print("Run: pip install google-generativeai")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
