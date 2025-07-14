"""
Streamlit Demo App for Multi-Agent System (No dotenv dependency)
Interactive web interface for testing agent capabilities
"""

import streamlit as st
import time
import json
import os
from datetime import datetime

# Import without dotenv dependency
try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    st.warning("⚠️ python-dotenv not installed. Using manual configuration only.")

from agents import SimpleAgent
from multi_agent_workflow import MultiAgentSystem
from e2e_llm_client import initialize_e2e_client, get_e2e_client, E2ELLMClient

# Page configuration
st.set_page_config(
    page_title="Multi-Agent AI System Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'multi_agent_system' not in st.session_state:
    st.session_state.multi_agent_system = MultiAgentSystem()

if 'simple_agent' not in st.session_state:
    st.session_state.simple_agent = SimpleAgent()

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Sidebar configuration
st.sidebar.title("🤖 Agent System Demo")
st.sidebar.markdown("---")

# E2E Networks API Configuration
st.sidebar.subheader("🔧 E2E Networks Configuration")

# Load from environment if available
default_api_key = os.getenv("E2E_API_KEY", "")
default_base_url = os.getenv("E2E_BASE_URL", "https://infer.e2enetworks.net/project/p-5861/endpoint/is-5691/v1")

api_key = st.sidebar.text_input(
    "E2E API Key",
    value=default_api_key,
    type="password",
    help="Enter your E2E Networks API key (or set E2E_API_KEY environment variable)",
    placeholder="eyJhbGciOi..."
)

base_url = st.sidebar.text_input(
    "E2E Base URL",
    value=default_base_url,
    help="E2E Networks API base URL (or set E2E_BASE_URL environment variable)"
)

# Show if values are loaded from environment
if default_api_key:
    st.sidebar.info("🔧 API key loaded from environment")
if DOTENV_AVAILABLE:
    st.sidebar.success("✅ dotenv loaded")
else:
    st.sidebar.warning("⚠️ Using environment variables only")

# Initialize E2E client when API key is provided
if api_key:
    try:
        initialize_e2e_client(api_key, base_url)
        client = get_e2e_client()
        
        # Test connection button
        if st.sidebar.button("🧪 Test E2E Connection"):
            with st.sidebar:
                with st.spinner("Testing connection..."):
                    test_result = client.test_connection()
                    
                    if test_result["status"] == "success":
                        st.success("✅ E2E API Connected!")
                    else:
                        st.error(f"❌ Connection failed: {test_result['response']}")
        
        # Show connection status
        st.sidebar.success("🟢 E2E API Configured")
        
    except Exception as e:
        st.sidebar.error(f"❌ E2E API Error: {str(e)}")
else:
    st.sidebar.warning("⚠️ E2E API key required for enhanced features")
    st.sidebar.markdown("""
    **📝 Setup Instructions:**
    1. Get your API key from E2E Networks dashboard
    2. Enter it in the field above
    3. Or set E2E_API_KEY environment variable
    """)

st.sidebar.markdown("---")

# Agent selection
agent_mode = st.sidebar.selectbox(
    "Select Agent System",
    ["🤖 Multi-Agent System", "⚡ Simple Agent"],
    help="Choose between single agent or multi-agent system"
)

st.sidebar.markdown("---")

# Example queries
st.sidebar.subheader("📝 Example Queries")

example_queries = {
    "🔍 Research + Analysis": [
        "What is machine learning and calculate 10 + 5?",
        "Research artificial intelligence and find average of 1,2,3,4,5",
        "Tell me about climate change and calculate 100 / 4"
    ],
    "📊 Analysis + Writing": [
        "Calculate 15 * 25 and write a technical summary",
        "What is 50 / 2 and create a report about it?",
        "Find sum of 10,20,30 and generate creative content"
    ],
    "✍️ Research + Writing": [
        "Research Python programming and write a summary",
        "What is blockchain and create an informative guide?",
        "Tell me about quantum computing and generate documentation"
    ],
    "🧮 Simple Math": [
        "What is 5 + 3?",
        "Calculate 100 * 2",
        "How are you?"
    ]
}

for category, queries in example_queries.items():
    with st.sidebar.expander(category):
        for query in queries:
            if st.button(query, key=f"example_{query[:20]}"):
                st.session_state.user_query = query

# Clear history button
if st.sidebar.button("🗑️ Clear History"):
    st.session_state.conversation_history = []
    st.session_state.multi_agent_system.clear_history()
    st.rerun()

# Main interface
st.title("🤖 Multi-Agent AI System Demo")
st.markdown("### Experience the power of collaborative AI agents working together!")

# Show configuration status
env_status = "🔧 Environment variables detected" if default_api_key else "📝 Manual configuration mode"
st.info(env_status)

# Show overall system status
client = get_e2e_client()
if client:
    st.success("🟢 **E2E Networks LLM**: Connected and ready for enhanced AI capabilities!")
    st.info(f"📡 **Endpoint**: {client.base_url}")
else:
    st.warning("⚠️ **E2E Networks LLM**: Not connected. Using fallback responses.")
    st.info("💡 **Setup**: Add your E2E API key in the sidebar for full functionality.")

# Create columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    # Query input
    user_query = st.text_area(
        "💬 Ask the agents anything:",
        value=st.session_state.get('user_query', ''),
        height=100,
        placeholder="Try: 'Research AI and calculate 10 + 5' or 'What is machine learning and write a summary?'"
    )
    
    # Process button
    if st.button("🚀 Process Query", type="primary"):
        if user_query.strip():
            with st.spinner("🤖 Agents are working..."):
                start_time = time.time()
                
                if "Multi-Agent" in agent_mode:
                    # Multi-agent processing
                    result = st.session_state.multi_agent_system.process_query(user_query)
                    
                    # Display results
                    st.success("✅ Multi-Agent Processing Complete!")
                    
                    # Show execution plan
                    st.subheader("📋 Execution Plan")
                    plan_cols = st.columns(len(result["task_plan"]))
                    for i, task in enumerate(result["task_plan"]):
                        with plan_cols[i]:
                            st.info(f"**{task['agent'].title()} Agent**\n{task['task']}")
                    
                    # Show agent results
                    st.subheader("🤖 Agent Results")
                    
                    for agent, output in result["agent_results"].items():
                        with st.expander(f"{agent.title()} Agent Output", expanded=True):
                            st.write(output)
                    
                    # Show final result
                    st.subheader("✨ Final Result")
                    st.markdown(result["final_result"])
                    
                    # Show metadata
                    with st.expander("📊 Execution Details"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Agents Used", len(result["metadata"]["agents_used"]))
                        with col2:
                            st.metric("Steps Executed", result["metadata"]["total_steps"])
                        with col3:
                            if "duration_seconds" in result["metadata"]:
                                st.metric("Duration", f"{result['metadata']['duration_seconds']:.2f}s")
                        
                        st.write("**Agents Used:**", ", ".join(result["metadata"]["agents_used"]))
                
                else:
                    # Simple agent processing
                    result = st.session_state.simple_agent.process_query(user_query)
                    
                    st.success("✅ Simple Agent Processing Complete!")
                    st.subheader("🤖 Agent Response")
                    st.write(result["result"])
                
                # Add to conversation history
                end_time = time.time()
                st.session_state.conversation_history.append({
                    "timestamp": datetime.now(),
                    "query": user_query,
                    "agent_mode": agent_mode,
                    "result": result,
                    "duration": end_time - start_time
                })
        else:
            st.error("Please enter a query!")

with col2:
    # System information
    st.subheader("🎯 System Info")
    
    if "Multi-Agent" in agent_mode:
        # Show E2E integration status
        client = get_e2e_client()
        e2e_status = "🟢 E2E LLM Integrated" if client else "🔴 E2E LLM Not Connected"
        
        st.info(f"""
        **🤖 Multi-Agent System**
        
        **Status:** {e2e_status}
        
        **Agents Available:**
        - 🎯 Coordinator: Plans & orchestrates
        - 🔍 Research: E2E-powered information gathering
        - 📊 Analysis: Math & data processing  
        - ✍️ Writing: E2E-powered content generation
        
        **Capabilities:**
        - Complex multi-step tasks
        - Agent collaboration
        - Dynamic task planning
        - Result aggregation
        - **E2E LLM Integration**
        """)
    else:
        # Show E2E integration status for simple agent
        client = get_e2e_client()
        e2e_status = "🟢 E2E LLM Integrated" if client else "🔴 E2E LLM Not Connected"
        
        st.info(f"""
        **⚡ Simple Agent System**
        
        **Status:** {e2e_status}
        
        **Capabilities:**
        - Basic math calculations
        - E2E-powered conversations
        - Quick responses
        - Single-step processing
        
        **Best for:**
        - Quick calculations
        - Simple Q&A
        - Fast responses
        """)

# Conversation history
if st.session_state.conversation_history:
    st.markdown("---")
    st.subheader("📝 Conversation History")
    
    for i, conv in enumerate(reversed(st.session_state.conversation_history[-5:])):  # Show last 5
        with st.expander(f"💬 {conv['query'][:50]}... ({conv['timestamp'].strftime('%H:%M:%S')})"):
            st.write(f"**Query:** {conv['query']}")
            st.write(f"**Agent Mode:** {conv['agent_mode']}")
            st.write(f"**Duration:** {conv['duration']:.2f}s")
            
            if "Multi-Agent" in conv['agent_mode']:
                if 'final_result' in conv['result']:
                    st.markdown("**Result:**")
                    st.markdown(conv['result']['final_result'])
            else:
                st.write(f"**Result:** {conv['result']['result']}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🚀 <strong>Multi-Agent AI System Demo</strong> | Built with Streamlit & LangGraph</p>
    <p>💡 Experiment with different query types to see how agents collaborate!</p>
    <p>🔗 <strong>Enhanced with E2E Networks LLM for intelligent responses</strong></p>
</div>
""", unsafe_allow_html=True)