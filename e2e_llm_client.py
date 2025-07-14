"""
E2E Networks LLM API Client
Handles API communication with E2E Networks LLM endpoints
"""

import requests
import json
import os
from typing import Dict, Any, Optional
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class E2ELLMClient:
    """Client for E2E Networks LLM API"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize E2E LLM Client
        
        Args:
            api_key: E2E Networks API key (can be set via environment variable E2E_API_KEY)
            base_url: E2E Networks API base URL (can be set via environment variable E2E_BASE_URL)
        """
        self.api_key = api_key or os.getenv("E2E_API_KEY")
        # Clean up base URL to avoid double slashes
        base_url_raw = base_url or os.getenv("E2E_BASE_URL", "https://infer.e2enetworks.net/project/p-5861/endpoint/is-5691/v1")
        self.base_url = base_url_raw.rstrip('/')
        
        # Load additional configuration from environment
        self.default_model = os.getenv("E2E_MODEL_NAME", "meta-llama/Llama-2-7b-chat-hf")
        self.default_max_tokens = int(os.getenv("E2E_MAX_TOKENS", "500"))
        self.default_temperature = float(os.getenv("E2E_TEMPERATURE", "0.7"))
        
        if not self.api_key:
            raise ValueError("E2E API key is required. Set E2E_API_KEY environment variable or pass api_key parameter.")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Timeout configuration
        self.timeout = 30
        
    def call_llm(self, 
                 prompt: str, 
                 model: Optional[str] = None,
                 max_tokens: Optional[int] = None,
                 temperature: Optional[float] = None,
                 system_message: Optional[str] = None) -> str:
        """
        Call E2E Networks LLM API
        
        Args:
            prompt: User prompt/question
            model: Model name (uses default if not specified)
            max_tokens: Maximum tokens in response
            temperature: Response creativity (0.0-1.0)
            system_message: System message for context
            
        Returns:
            LLM response text
        """
        try:
            # Prepare messages
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            # API payload for E2E Networks format
            payload = {
                "model": model or self.default_model,
                "messages": messages,
                "max_tokens": max_tokens or self.default_max_tokens,
                "temperature": temperature or self.default_temperature,
                "stream": False
            }
            
            # Try different endpoint formats for E2E Networks
            endpoints_to_try = [
                f"{self.base_url}/chat/completions",
                f"{self.base_url}/completions", 
                f"{self.base_url}/generate",
                f"{self.base_url}/v1/chat/completions",
                f"{self.base_url}/inference",
                f"{self.base_url}"
            ]
            
            response = None
            for endpoint in endpoints_to_try:
                try:
                    print(f"Debug: Trying endpoint: {endpoint}")
                    response = requests.post(
                        endpoint,
                        headers=self.headers,
                        json=payload,
                        timeout=self.timeout
                    )
                    print(f"Debug: Response status: {response.status_code}")
                    
                    if response.status_code == 200:
                        print(f"✅ Success with endpoint: {endpoint}")
                        break
                    elif response.status_code in [404, 405]:
                        print(f"❌ {response.status_code} - trying next endpoint")
                        continue
                    else:
                        print(f"Debug: Response text: {response.text}")
                        break
                        
                except Exception as e:
                    print(f"Debug: Error with {endpoint}: {str(e)}")
                    continue
            
            if not response:
                return "Error: Unable to connect to any E2E endpoint"
            
            # Handle response
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    print(f"Debug: Response data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                    
                    # Try different response formats
                    if "choices" in data and len(data["choices"]) > 0:
                        return data["choices"][0]["message"]["content"]
                    elif "response" in data:
                        return data["response"]
                    elif "text" in data:
                        return data["text"]
                    elif "output" in data:
                        return data["output"]
                    elif isinstance(data, str):
                        return data
                    else:
                        print(f"⚠️ Unexpected response format: {data}")
                        return f"Error: Unexpected response format from E2E API. Keys: {list(data.keys()) if isinstance(data, dict) else 'N/A'}"
                except json.JSONDecodeError:
                    return f"Error: Invalid JSON response: {response.text}"
            else:
                error_msg = f"E2E API Error {response.status_code if response else 'No response'}: {response.text if response else 'Connection failed'}"
                print(f"⚠️ {error_msg}")
                return f"Error calling E2E LLM API: {response.status_code if response else 'Connection failed'}"
                
        except requests.RequestException as e:
            error_msg = f"Network error calling E2E API: {str(e)}"
            print(f"⚠️ {error_msg}")
            return "Error: Unable to connect to E2E Networks API"
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"⚠️ {error_msg}")
            return "Error: Unexpected issue with E2E API call"
    
    def call_with_retry(self, prompt: str, max_retries: int = 3, **kwargs) -> str:
        """
        Call LLM with retry logic
        
        Args:
            prompt: User prompt
            max_retries: Maximum number of retry attempts
            **kwargs: Additional arguments for call_llm
            
        Returns:
            LLM response or error message
        """
        for attempt in range(max_retries):
            try:
                result = self.call_llm(prompt, **kwargs)
                if not result.startswith("Error"):
                    return result
                
                if attempt < max_retries - 1:
                    time.sleep(1 * (attempt + 1))  # Exponential backoff
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(1 * (attempt + 1))
                else:
                    return f"Error after {max_retries} attempts: {str(e)}"
        
        return "Error: Max retries exceeded"
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the E2E API connection
        
        Returns:
            Dictionary with connection status and details
        """
        try:
            test_prompt = "Hello, this is a test message. Please respond with 'Connection successful.'"
            print(f"Testing connection to: {self.base_url}")
            print(f"Using model: {self.default_model}")
            response = self.call_llm(test_prompt, max_tokens=50)
            
            return {
                "status": "success" if not response.startswith("Error") else "error",
                "response": response,
                "api_key_configured": bool(self.api_key),
                "base_url": self.base_url,
                "model": self.default_model
            }
        except Exception as e:
            print(f"Exception during test: {str(e)}")
            return {
                "status": "error",
                "response": str(e),
                "api_key_configured": bool(self.api_key),
                "base_url": self.base_url,
                "model": self.default_model
            }

# Global client instance (will be initialized when API key is provided)
_global_client = None

def get_e2e_client() -> Optional[E2ELLMClient]:
    """Get the global E2E client instance"""
    return _global_client

def initialize_e2e_client(api_key: str, base_url: Optional[str] = None) -> E2ELLMClient:
    """Initialize the global E2E client"""
    global _global_client
    _global_client = E2ELLMClient(api_key=api_key, base_url=base_url)
    return _global_client

def call_e2e_llm(prompt: str, **kwargs) -> str:
    """
    Convenience function to call E2E LLM
    
    Args:
        prompt: User prompt
        **kwargs: Additional arguments
        
    Returns:
        LLM response or fallback message
    """
    client = get_e2e_client()
    if not client:
        return "⚠️ E2E Networks API not configured. Please set your API key."
    
    return client.call_with_retry(prompt, **kwargs)