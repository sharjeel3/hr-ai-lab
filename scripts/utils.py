"""                                                                                                                       Core utilities for HR AI Lab experiments.

This module provides:
- LLM integration functions
- Data loading utilities
- Common metrics calculations
- Logging and error handling
"""

import os
import json
import csv
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, will use system environment variables only
    pass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import rate limiter
try:
    from .rate_limiter import get_rate_limiter
except ImportError:
    # Fallback for when running as script
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from rate_limiter import get_rate_limiter


class LLMClient:
    """
    Wrapper for LLM API calls with support for multiple providers.
    """
    
    def __init__(self, provider: str = "google", model: str = "gemini-2.5-flash-lite"):
        """
        Initialize LLM client.
        
        Args:
            provider: LLM provider (google, openai, anthropic, azure)
            model: Model name
        """
        self.provider = provider
        self.model = model
        self.api_key = self._get_api_key()
        self.rate_limiter = get_rate_limiter(model) if provider == "google" else None
        
    def _get_api_key(self) -> str:
        """Get API key from environment variables."""
        key_map = {
            "google": "GOOGLE_API_KEY",
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "azure": "AZURE_OPENAI_KEY"
        }
        key_name = key_map.get(self.provider)
        api_key = os.getenv(key_name)
        if not api_key:
            logger.warning(f"{key_name} not found in environment variables")
        return api_key
    
    def call(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """
        Make a call to the LLM API.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            
        Returns:
            Dict containing response and metadata
        """
        try:
            if self.provider == "google":
                return self._call_google(prompt, system_prompt, temperature, max_tokens)
            elif self.provider == "openai":
                return self._call_openai(prompt, system_prompt, temperature, max_tokens)
            elif self.provider == "anthropic":
                return self._call_anthropic(prompt, system_prompt, temperature, max_tokens)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            return {
                "response": None,
                "error": str(e),
                "metadata": {
                    "model": self.model,
                    "provider": self.provider
                }
            }
    
    def _call_google(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """Call Google Gemini API."""
        try:
            import google.generativeai as genai
            
            # Apply rate limiting
            if self.rate_limiter:
                self.rate_limiter.wait()
            
            genai.configure(api_key=self.api_key)
            
            # Create model instance
            model = genai.GenerativeModel(self.model)
            
            # Combine system prompt and user prompt
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            # Generate response
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
            )
            
            # Check if response was blocked
            if not response.candidates:
                error_msg = "Response blocked - no candidates returned"
                logger.error(f"Gemini API: {error_msg}")
                logger.error(f"Prompt feedback: {response.prompt_feedback if hasattr(response, 'prompt_feedback') else 'N/A'}")
                return {
                    "response": None,
                    "error": error_msg,
                    "metadata": {
                        "model": self.model,
                        "provider": self.provider
                    }
                }
            
            # Check if content was blocked
            candidate = response.candidates[0]
            if not hasattr(candidate.content, 'parts') or not candidate.content.parts:
                error_msg = f"Content blocked - finish_reason: {candidate.finish_reason.name}"
                logger.error(f"Gemini API: {error_msg}")
                return {
                    "response": None,
                    "error": error_msg,
                    "metadata": {
                        "model": self.model,
                        "provider": self.provider,
                        "finish_reason": candidate.finish_reason.name
                    }
                }
            
            return {
                "response": response.text,
                "metadata": {
                    "model": self.model,
                    "provider": self.provider,
                    "finish_reason": candidate.finish_reason.name
                }
            }
        except ImportError:
            logger.error("Google Generative AI package not installed. Run: pip install google-generativeai")
            raise
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower() or "ResourceExhausted" in str(type(e).__name__):
                logger.error("⚠️  Google API Quota Exceeded!")
                logger.error("You've hit the rate limit for Gemini API.")
                logger.error("Solutions:")
                logger.error("  1. Wait for the quota to reset (check error message for retry time)")
                logger.error("  2. Upgrade to a paid tier at https://ai.google.dev/")
                logger.error("  3. Switch to a different model with higher limits")
                logger.error(f"Error details: {error_msg[:500]}")
            else:
                logger.error(f"Google Gemini API call failed: {error_msg}")
                logger.error(f"Error type: {type(e).__name__}")
            import traceback
            logger.debug(f"Traceback: {traceback.format_exc()}")
            raise
    
    def _clean_json_response(self, text: str) -> str:
        """Clean JSON response by removing markdown code blocks."""
        if not text:
            return text
        
        # Remove ```json and ``` markers
        import re
        # Pattern to match ```json ... ``` or ``` ... ```
        pattern = r'```(?:json)?\s*\n?(.*?)\n?```'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()
    
    def _call_openai(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """Call OpenAI API."""
        try:
            import openai
            openai.api_key = self.api_key
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return {
                "response": response.choices[0].message.content,
                "metadata": {
                    "model": self.model,
                    "provider": self.provider,
                    "tokens_used": response.usage.total_tokens,
                    "finish_reason": response.choices[0].finish_reason
                }
            }
        except ImportError:
            logger.error("OpenAI package not installed. Run: pip install openai")
            raise
    
    def _call_anthropic(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """Call Anthropic API."""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            
            response = client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt or "",
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                "response": response.content[0].text,
                "metadata": {
                    "model": self.model,
                    "provider": self.provider,
                    "tokens_used": response.usage.input_tokens + response.usage.output_tokens
                }
            }
        except ImportError:
            logger.error("Anthropic package not installed. Run: pip install anthropic")
            raise


    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Generate text from LLM (simplified interface).
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated text response (cleaned of markdown code blocks)
        """
        result = self.call(prompt, system_prompt, temperature, max_tokens)
        response_text = result.get("response", "")
        
        # Check for errors in result
        if result.get("error"):
            logger.error(f"LLM generate error: {result.get('error')}")
            return ""
        
        # Clean JSON responses (remove markdown code blocks)
        if response_text and self.provider == "google":
            response_text = self._clean_json_response(response_text)
        
        return response_text if response_text else ""


def call_llm(
    prompt: str,
    model: str = "gemini-2.5-flash-lite",
    provider: str = "google",
    **kwargs
) -> str:
    """
    Convenience function for quick LLM calls.
    
    Args:
        prompt: User prompt
        model: Model name
        provider: LLM provider
        **kwargs: Additional parameters
        
    Returns:
        LLM response text
    """
    client = LLMClient(provider=provider, model=model)
    result = client.call(prompt, **kwargs)
    return result.get("response", "")


def load_json_data(path: str) -> Dict[str, Any]:
    """
    Load JSON data from a file.
    
    Args:
        path: Path to JSON file
        
    Returns:
        Dictionary with loaded data
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load JSON from {path}: {str(e)}")
        return {}


def load_dataset(path: str, file_type: str = "auto") -> List[Dict[str, Any]]:
    """
    Load dataset from various file formats.
    
    Args:
        path: Path to dataset file or directory
        file_type: File type (json, csv, txt, auto)
        
    Returns:
        List of data items
    """
    path_obj = Path(path)
    
    if not path_obj.exists():
        logger.error(f"Path does not exist: {path}")
        return []
    
    # Handle directory
    if path_obj.is_dir():
        data = []
        for file in path_obj.iterdir():
            if file.is_file():
                data.extend(load_dataset(str(file), file_type))
        return data
    
    # Detect file type
    if file_type == "auto":
        file_type = path_obj.suffix.lower().lstrip('.')
    
    try:
        if file_type == "json":
            return _load_json(path_obj)
        elif file_type == "csv":
            return _load_csv(path_obj)
        elif file_type in ["txt", "text"]:
            return _load_text(path_obj)
        else:
            logger.warning(f"Unsupported file type: {file_type}, trying as text")
            return _load_text(path_obj)
    except Exception as e:
        logger.error(f"Failed to load {path}: {str(e)}")
        return []


def _load_json(path: Path) -> List[Dict[str, Any]]:
    """Load JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Handle both single objects and lists
        return data if isinstance(data, list) else [data]


def _load_csv(path: Path) -> List[Dict[str, Any]]:
    """Load CSV file."""
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def _load_text(path: Path) -> List[Dict[str, Any]]:
    """Load text file."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        return [{
            "filename": path.name,
            "text": content,
            "path": str(path)
        }]


def save_results(
    data: Any,
    output_path: str,
    format: str = "json"
) -> bool:
    """
    Save results to file.
    
    Args:
        data: Data to save
        output_path: Output file path
        format: Output format (json, csv)
        
    Returns:
        True if successful
    """
    try:
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        if format == "json":
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        elif format == "csv":
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                if isinstance(data, list) and len(data) > 0:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        logger.info(f"Results saved to {output_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save results: {str(e)}")
        return False


def calculate_accuracy(predictions: List[Any], ground_truth: List[Any]) -> float:
    """
    Calculate accuracy metric.
    
    Args:
        predictions: List of predictions
        ground_truth: List of ground truth values
        
    Returns:
        Accuracy score (0-1)
    """
    if len(predictions) != len(ground_truth):
        logger.warning("Predictions and ground truth have different lengths")
        return 0.0
    
    if len(predictions) == 0:
        return 0.0
    
    correct = sum(1 for p, g in zip(predictions, ground_truth) if p == g)
    return correct / len(predictions)


def calculate_metrics(data: List[Dict[str, Any]], metric_type: str = "basic") -> Dict[str, Any]:
    """
    Calculate various metrics from data.
    
    Args:
        data: List of data items
        metric_type: Type of metrics to calculate
        
    Returns:
        Dictionary with calculated metrics
    """
    if not data:
        return {"count": 0}
    
    metrics = {
        "count": len(data),
        "timestamp": timestamp()
    }
    
    return metrics


def timestamp() -> str:
    """Get current timestamp string."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def get_project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parent.parent


def get_experiment_path(experiment_name: str) -> Path:
    """Get path to experiment directory."""
    return get_project_root() / "experiments" / experiment_name


def get_dataset_path(dataset_name: str) -> Path:
    """Get path to dataset directory."""
    return get_project_root() / "datasets" / dataset_name


def get_results_path() -> Path:
    """Get path to results directory."""
    return get_project_root() / "results"


if __name__ == "__main__":
    # Test utilities
    print("Testing HR AI Lab utilities...")
    print(f"Project root: {get_project_root()}")
    print(f"Experiments path: {get_experiment_path('recruitment_cv_screening')}")
    print(f"Datasets path: {get_dataset_path('synthetic_cvs')}")
    print(f"Results path: {get_results_path()}")
