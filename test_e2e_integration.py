"""
Test script for E2E Networks LLM integration
Use this to test the API connection and agent functionality
"""

import os
from e2e_llm_client import E2ELLMClient, initialize_e2e_client
from agents import SimpleAgent, ResearchAgent, WritingAgent
from multi_agent_workflow import MultiAgentSystem

def test_e2e_connection():
    """Test basic E2E API connection"""
    print("🧪 Testing E2E Networks LLM Connection...")
    print("-" * 50)
    
    # Get API credentials (you need to set these)
    api_key = os.getenv("E2E_API_KEY") or input("Enter your E2E API key: ")
    base_url = os.getenv("E2E_BASE_URL", "https://api.e2enetworks.com/v1")
    
    if not api_key:
        print("❌ No API key provided")
        return False
    
    try:
        # Initialize client
        client = E2ELLMClient(api_key=api_key, base_url=base_url)
        
        # Test connection
        result = client.test_connection()
        
        print(f"Status: {result['status']}")
        print(f"Response: {result['response']}")
        print(f"API Key Configured: {result['api_key_configured']}")
        print(f"Base URL: {result['base_url']}")
        
        return result['status'] == 'success'
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def test_simple_agent():
    """Test Simple Agent with E2E integration"""
    print("\n🤖 Testing Simple Agent...")
    print("-" * 50)
    
    agent = SimpleAgent()
    
    test_queries = [
        "Hello, how are you?",
        "What is 10 + 5?",
        "Tell me a joke",
        "What is artificial intelligence?"
    ]
    
    for query in test_queries:
        print(f"\n👤 Query: {query}")
        result = agent.process_query(query)
        print(f"🤖 Response: {result['result']}")

def test_research_agent():
    """Test Research Agent with E2E integration"""
    print("\n🔍 Testing Research Agent...")
    print("-" * 50)
    
    agent = ResearchAgent()
    
    test_queries = [
        "machine learning",
        "climate change",
        "quantum computing"
    ]
    
    for query in test_queries:
        print(f"\n👤 Research Query: {query}")
        state = {"user_query": query, "agent_results": {}}
        result = agent.gather_information(state)
        print(f"🔍 Research Result: {result['agent_results']['research']}")

def test_writing_agent():
    """Test Writing Agent with E2E integration"""
    print("\n✍️ Testing Writing Agent...")
    print("-" * 50)
    
    agent = WritingAgent()
    
    test_queries = [
        ("artificial intelligence", "summary"),
        ("python programming", "technical"),
        ("space exploration", "creative")
    ]
    
    for query, style in test_queries:
        print(f"\n👤 Writing Query: {query} (style: {style})")
        state = {
            "user_query": f"write a {style} piece about {query}",
            "agent_results": {}
        }
        result = agent.create_content(state)
        print(f"✍️ Writing Result: {result['agent_results']['writing']}")

def test_multi_agent_system():
    """Test complete Multi-Agent System with E2E integration"""
    print("\n🤖🤖🤖 Testing Multi-Agent System...")
    print("-" * 50)
    
    system = MultiAgentSystem()
    
    test_queries = [
        "What is machine learning and calculate 10 + 5?",
        "Research climate change and write a summary",
        "Calculate the average of 1,2,3,4,5 and create a report"
    ]
    
    for query in test_queries:
        print(f"\n👤 Multi-Agent Query: {query}")
        print("🔄 Processing...")
        
        result = system.process_query(query)
        
        print(f"📋 Task Plan: {[task['agent'] for task in result['task_plan']]}")
        print(f"🤖 Agents Used: {result['metadata']['agents_used']}")
        print(f"✨ Final Result:\n{result['final_result']}")
        print("-" * 30)

def main():
    """Main test function"""
    print("🚀 E2E Networks LLM Integration Test Suite")
    print("=" * 60)
    
    # Test 1: Basic connection
    if not test_e2e_connection():
        print("\n❌ E2E connection failed. Tests will use fallback responses.")
        print("Please check your API key and base URL.")
    else:
        print("\n✅ E2E connection successful!")
    
    # Initialize global client for agents
    api_key = os.getenv("E2E_API_KEY")
    if api_key:
        initialize_e2e_client(api_key)
    
    # Test 2: Individual agents
    test_simple_agent()
    test_research_agent() 
    test_writing_agent()
    
    # Test 3: Multi-agent system
    test_multi_agent_system()
    
    print("\n🎉 Test suite completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()