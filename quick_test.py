#!/usr/bin/env python3
"""
Quick test script to debug E2E API and calculator issues
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Test 1: Check E2E API with current configuration
print("🔧 Testing E2E API Configuration...")
print("-" * 50)

# Check environment variables
api_key = os.getenv("E2E_API_KEY")
base_url = os.getenv("E2E_BASE_URL")

print(f"API Key set: {'Yes' if api_key else 'No'}")
print(f"Base URL: {base_url}")
print(f"API Key (first 10 chars): {api_key[:10] + '...' if api_key else 'None'}")

# Test 2: Test calculator function
print("\n🧮 Testing Calculator Function...")
print("-" * 50)

from agents import advanced_calculator

test_expressions = [
    "10 + 5",
    "15 * 25", 
    "100 / 4",
    "average of 1,2,3,4,5",
    "sum of 10,20,30"
]

for expr in test_expressions:
    result = advanced_calculator.invoke({"expression": expr})
    print(f"'{expr}' → {result}")

# Test 3: Test E2E client directly
print("\n🌐 Testing E2E Client Directly...")
print("-" * 50)

try:
    from e2e_llm_client import E2ELLMClient
    
    if api_key:
        client = E2ELLMClient(api_key=api_key, base_url=base_url)
        
        # Test with minimal payload
        print("Testing basic connection...")
        test_result = client.test_connection()
        print(f"Result: {test_result}")
        
    else:
        print("❌ No API key available for testing")
        
except Exception as e:
    print(f"❌ Error testing E2E client: {str(e)}")

# Test 4: Alternative E2E API call format
print("\n🔄 Testing Alternative API Format...")
print("-" * 50)

if api_key and base_url:
    import requests
    import json
    
    # Try different endpoint formats
    endpoints_to_try = [
        f"{base_url}/chat/completions",
        f"{base_url}/completions", 
        f"{base_url}/generate",
        f"{base_url.rstrip('/v1')}/completions",
        f"{base_url.rstrip('/v1')}/chat/completions"
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Simple test payload
    payload = {
        "model": "meta-llama/Llama-2-7b-chat-hf",
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 50
    }
    
    for endpoint in endpoints_to_try:
        try:
            print(f"Trying: {endpoint}")
            response = requests.post(endpoint, headers=headers, json=payload, timeout=10)
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                print(f"  ✅ SUCCESS! Response: {response.json()}")
                break
            else:
                print(f"  Response: {response.text[:200]}")
        except Exception as e:
            print(f"  Error: {str(e)}")

print("\n✅ Quick test completed!")