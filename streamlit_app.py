"""
Streamlit Demo App for Multi-Agent System
Interactive web interface for testing agent capabilities
"""

import streamlit as st
import time
import json
from datetime import datetime
from agents import SimpleAgent
from multi_agent_workflow import MultiAgentSystem

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
        st.info("""
        **🤖 Multi-Agent System**
        
        **Agents Available:**
        - 🎯 Coordinator: Plans & orchestrates
        - 🔍 Research: Information gathering
        - 📊 Analysis: Math & data processing  
        - ✍️ Writing: Content generation
        
        **Capabilities:**
        - Complex multi-step tasks
        - Agent collaboration
        - Dynamic task planning
        - Result aggregation
        """)
    else:
        st.info("""
        **⚡ Simple Agent System**
        
        **Capabilities:**
        - Basic math calculations
        - Simple conversations
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
</div>
""", unsafe_allow_html=True)