#!/usr/bin/env python3
"""
Dedicated script to test E2E Networks API endpoints and find the correct format
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_e2e_endpoints():
    """Test various E2E endpoint formats to find the working one"""
    
    api_key = os.getenv("E2E_API_KEY")
    base_url = os.getenv("E2E_BASE_URL", "").rstrip('/')
    
    if not api_key:
        print("❌ No API key found. Set E2E_API_KEY in .env file")
        return
    
    print(f"🧪 Testing E2E Networks API Endpoints")
    print(f"📡 Base URL: {base_url}")
    print(f"🔑 API Key: {api_key[:20]}...")
    print("-" * 60)
    
    # Different headers to try
    headers_variants = [
        {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        {
            "Authorization": f"Token {api_key}",
            "Content-Type": "application/json"
        },
        {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        },
        {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
    ]
    
    # Different endpoint paths to try
    endpoints = [
        f"{base_url}/chat/completions",
        f"{base_url}/completions",
        f"{base_url}/generate", 
        f"{base_url}/inference",
        f"{base_url}/predict",
        f"{base_url}/api/generate",
        f"{base_url}/api/chat",
        f"{base_url}/v1/completions",
        f"{base_url}/v1/chat/completions",
        f"{base_url}",
        f"{base_url}/",
    ]
    
    # Different payload formats to try
    payloads = [
        # OpenAI-style format
        {
            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
            "messages": [{"role": "user", "content": "Hello, respond with 'API working'"}],
            "max_tokens": 50,
            "temperature": 0.7
        },
        # Simple completion format
        {
            "prompt": "Hello, respond with 'API working'",
            "max_tokens": 50,
            "temperature": 0.7
        },
        # Hugging Face style
        {
            "inputs": "Hello, respond with 'API working'",
            "parameters": {
                "max_new_tokens": 50,
                "temperature": 0.7
            }
        },
        # Direct text format
        {
            "text": "Hello, respond with 'API working'",
            "max_length": 50
        }
    ]
    
    success_found = False
    
    for endpoint in endpoints:
        print(f"\n🔗 Testing endpoint: {endpoint}")
        
        for i, headers in enumerate(headers_variants):
            for j, payload in enumerate(payloads):
                try:
                    response = requests.post(
                        endpoint,
                        headers=headers,
                        json=payload,
                        timeout=10
                    )
                    
                    print(f"  📤 Headers variant {i+1}, Payload variant {j+1}: {response.status_code}")
                    
                    if response.status_code == 200:
                        print(f"  ✅ SUCCESS!")
                        print(f"  📨 Response: {response.text[:200]}...")
                        print(f"  🎯 Working config:")
                        print(f"     Endpoint: {endpoint}")
                        print(f"     Headers: {headers}")
                        print(f"     Payload: {json.dumps(payload, indent=2)}")
                        success_found = True
                        return endpoint, headers, payload
                        
                    elif response.status_code in [400, 422]:
                        print(f"  ⚠️  Bad request - payload might be wrong")
                        print(f"     Response: {response.text[:100]}")
                        
                    elif response.status_code == 401:
                        print(f"  🔐 Unauthorized - auth header might be wrong")
                        
                    elif response.status_code == 404:
                        print(f"  🔍 Not found - endpoint doesn't exist")
                        
                    elif response.status_code == 405:
                        print(f"  🚫 Method not allowed - wrong HTTP method")
                        
                    else:
                        print(f"  ❓ Status {response.status_code}: {response.text[:100]}")
                        
                except requests.exceptions.Timeout:
                    print(f"  ⏰ Timeout")
                except requests.exceptions.RequestException as e:
                    print(f"  💥 Request error: {str(e)}")
                except Exception as e:
                    print(f"  🐛 Unexpected error: {str(e)}")
    
    if not success_found:
        print(f"\n❌ No working configuration found!")
        print(f"\n💡 Suggestions:")
        print(f"  1. Check if your API key is valid")
        print(f"  2. Verify the base URL from E2E Networks dashboard")
        print(f"  3. Contact E2E Networks support for correct API format")
        print(f"  4. Check E2E Networks documentation")
    
    return None

if __name__ == "__main__":
    test_e2e_endpoints()