"""
Rate Limiter for API calls

This module provides rate limiting functionality to respect API rate limits
for services like Google Gemini API.
"""

import time
import threading
from typing import Optional
from datetime import datetime, timedelta


class RateLimiter:
    """
    Token bucket rate limiter for API calls.
    
    This implementation uses the token bucket algorithm to enforce rate limits
    based on requests per minute (RPM).
    """
    
    def __init__(self, rpm: int = 15):
        """
        Initialize rate limiter.
        
        Args:
            rpm: Requests per minute allowed
        """
        self.rpm = rpm
        self.tokens = rpm
        self.max_tokens = rpm
        self.last_update = time.time()
        self.lock = threading.Lock()
        
    def _refill_tokens(self):
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_update
        
        # Calculate tokens to add based on elapsed time
        # tokens_to_add = (elapsed / 60) * rpm
        tokens_to_add = (elapsed / 60.0) * self.rpm
        
        self.tokens = min(self.max_tokens, self.tokens + tokens_to_add)
        self.last_update = now
    
    def acquire(self, block: bool = True, timeout: Optional[float] = None) -> bool:
        """
        Acquire a token to make an API call.
        
        Args:
            block: If True, block until a token is available
            timeout: Maximum time to wait in seconds (only used if block=True)
            
        Returns:
            True if token was acquired, False otherwise
        """
        start_time = time.time()
        
        while True:
            with self.lock:
                self._refill_tokens()
                
                if self.tokens >= 1:
                    self.tokens -= 1
                    return True
                
                if not block:
                    return False
                
                # Calculate wait time until next token is available
                wait_time = (1.0 / self.rpm) * 60.0
                
            # Check timeout
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    return False
                wait_time = min(wait_time, timeout - elapsed)
            
            # Sleep before retrying
            time.sleep(wait_time)
    
    def wait(self):
        """
        Wait until a token is available (blocking).
        Convenience method that always blocks.
        """
        self.acquire(block=True)
    
    def get_available_tokens(self) -> float:
        """
        Get the current number of available tokens.
        
        Returns:
            Number of tokens available
        """
        with self.lock:
            self._refill_tokens()
            return self.tokens
    
    def reset(self):
        """Reset the rate limiter to full capacity."""
        with self.lock:
            self.tokens = self.max_tokens
            self.last_update = time.time()


# Global rate limiter instances for different models
_rate_limiters = {}


def get_rate_limiter(model: str = "gemini-2.5-flash-lite") -> RateLimiter:
    """
    Get or create a rate limiter for a specific model.
    
    Args:
        model: Model name
        
    Returns:
        RateLimiter instance
    """
    # Rate limits for different Gemini models (Free tier)
    model_rpm_limits = {
        "gemini-2.5-pro": 2,
        "gemini-2.5-flash": 10,
        "gemini-2.5-flash-preview": 10,
        "gemini-2.5-flash-lite": 15,
        "gemini-2.5-flash-lite-preview": 15,
        "gemini-2.0-flash": 15,
        "gemini-2.0-flash-lite": 30,
    }
    
    # Normalize model name
    model_key = model.lower()
    
    # Create rate limiter if it doesn't exist
    if model_key not in _rate_limiters:
        rpm = model_rpm_limits.get(model_key, 15)  # Default to 15 RPM
        _rate_limiters[model_key] = RateLimiter(rpm=rpm)
    
    return _rate_limiters[model_key]


if __name__ == "__main__":
    # Test rate limiter
    print("Testing rate limiter...")
    limiter = RateLimiter(rpm=15)
    
    print(f"Available tokens: {limiter.get_available_tokens()}")
    
    # Simulate API calls
    for i in range(5):
        limiter.wait()
        print(f"Call {i+1} - Tokens remaining: {limiter.get_available_tokens():.2f}")
    
    print("Rate limiter test complete!")
