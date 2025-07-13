"""
Multi-Agent System Core Components
Extracted from Jupyter notebook for Streamlit integration
"""

import re
import json
import requests
import random
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from langchain.tools import tool

# Agent Tools
@tool
def web_search(query: str) -> str:
    """Simulate web search for research tasks"""
    search_results = {
        "python programming": "Python is a high-level programming language known for its simplicity and versatility. Latest version is 3.12.",
        "machine learning": "Machine learning is a subset of AI that enables computers to learn without explicit programming. Popular frameworks include TensorFlow and PyTorch.",
        "climate change": "Climate change refers to long-term shifts in global temperatures and weather patterns. Human activities are the main driver since the 1800s.",
        "artificial intelligence": "AI is intelligence demonstrated by machines, as opposed to human intelligence. It includes machine learning, natural language processing, and robotics.",
        "data science": "Data science combines statistics, programming, and domain expertise to extract insights from data.",
        "blockchain": "Blockchain is a distributed ledger technology that maintains a secure and decentralized record of transactions.",
        "quantum computing": "Quantum computing uses quantum mechanical phenomena to process information in ways classical computers cannot."
    }
    
    for topic, result in search_results.items():
        if topic.lower() in query.lower():
            return f"🔍 Search Results: {result}"
    
    return f"🔍 Search Results: Found general information about '{query}'. This topic is actively researched with many recent developments."

@tool
def advanced_calculator(expression: str) -> str:
    """Advanced mathematical calculations with statistical functions"""
    try:
        # Handle special functions
        if "average" in expression.lower() or "mean" in expression.lower():
            numbers = [float(x) for x in re.findall(r'-?\d+\.?\d*', expression)]
            if numbers:
                result = sum(numbers) / len(numbers)
                return f"📊 Average of {numbers} = {result:.2f}"
        
        if "sum" in expression.lower():
            numbers = [float(x) for x in re.findall(r'-?\d+\.?\d*', expression)]
            if numbers:
                result = sum(numbers)
                return f"📊 Sum of {numbers} = {result}"
        
        # Standard calculation
        expression = re.sub(r'[^0-9+\-*/.() ]', '', expression)
        result = eval(expression)
        return f"🧮 {expression} = {result}"
    except:
        return "❌ Error in calculation"

@tool
def data_visualizer(data_description: str) -> str:
    """Create simple data visualizations"""
    chart_types = ["bar chart", "line graph", "pie chart", "scatter plot"]
    selected_chart = random.choice(chart_types)
    
    return f"📈 Created {selected_chart} for: {data_description}. Visualization shows clear trends and patterns."

@tool
def content_generator(topic: str, style: str = "informative") -> str:
    """Generate content based on topic and style"""
    styles = {
        "informative": f"📝 Comprehensive guide on {topic} covering key concepts, applications, and best practices.",
        "summary": f"📋 Quick summary: {topic} is an important concept with significant practical applications.",
        "technical": f"🔧 Technical documentation for {topic} including implementation details and specifications.",
        "creative": f"✨ Creative exploration of {topic} from unique perspectives and innovative angles."
    }
    
    return styles.get(style, styles["informative"])

# Multi-Agent State Management
class MultiAgentState:
    def __init__(self, user_query: str):
        self.user_query = user_query
        self.task_plan = []
        self.agent_results = {}
        self.final_result = ""
        self.current_step = 0
        self.conversation_log = []
        self.metadata = {
            "start_time": datetime.now(),
            "agents_used": [],
            "total_steps": 0
        }
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_query": self.user_query,
            "task_plan": self.task_plan,
            "agent_results": self.agent_results,
            "final_result": self.final_result,
            "current_step": self.current_step,
            "conversation_log": self.conversation_log,
            "metadata": self.metadata
        }
    
    def log_agent_action(self, agent_name: str, action: str, result: str):
        self.conversation_log.append({
            "timestamp": datetime.now(),
            "agent": agent_name,
            "action": action,
            "result": result
        })
        if agent_name not in self.metadata["agents_used"]:
            self.metadata["agents_used"].append(agent_name)

# Individual Agent Classes
class CoordinatorAgent:
    def __init__(self):
        self.name = "Coordinator"
    
    def plan_task(self, state_dict: Dict) -> Dict:
        query = state_dict["user_query"]
        
        # Analyze query to determine which agents to use
        plan = []
        
        # Check for research needs
        research_keywords = ["what is", "tell me about", "research", "find information", "explain"]
        if any(keyword in query.lower() for keyword in research_keywords):
            plan.append({"agent": "research", "task": "gather_information"})
        
        # Check for analysis needs
        analysis_keywords = ["calculate", "analyze", "compare", "statistics", "average", "sum", "+", "-", "*", "/"]
        if any(keyword in query.lower() for keyword in analysis_keywords):
            plan.append({"agent": "analysis", "task": "process_data"})
        
        # Check for writing needs
        writing_keywords = ["write", "create", "generate", "summarize", "report", "document"]
        if any(keyword in query.lower() for keyword in writing_keywords):
            plan.append({"agent": "writing", "task": "create_content"})
        
        # Default plan if no specific keywords found
        if not plan:
            plan = [
                {"agent": "research", "task": "gather_information"},
                {"agent": "writing", "task": "create_content"}
            ]
        
        state_dict["task_plan"] = plan
        state_dict["current_step"] = 0
        state_dict["metadata"]["total_steps"] = len(plan)
        
        return state_dict
    
    def aggregate_results(self, state_dict: Dict) -> Dict:
        results = state_dict["agent_results"]
        
        # Combine all agent results
        final_parts = []
        
        if "research" in results:
            final_parts.append(f"📚 **Research Findings:**\n{results['research']}")
        
        if "analysis" in results:
            final_parts.append(f"📊 **Analysis Results:**\n{results['analysis']}")
        
        if "writing" in results:
            final_parts.append(f"✍️ **Generated Content:**\n{results['writing']}")
        
        state_dict["final_result"] = "\n\n".join(final_parts)
        state_dict["metadata"]["end_time"] = datetime.now()
        
        return state_dict

class ResearchAgent:
    def __init__(self):
        self.name = "Research"
    
    def gather_information(self, state_dict: Dict) -> Dict:
        query = state_dict["user_query"]
        
        # Extract main topic from query
        search_result = web_search.invoke({"query": query})
        
        state_dict["agent_results"]["research"] = search_result
        return state_dict

class AnalysisAgent:
    def __init__(self):
        self.name = "Analysis"
    
    def process_data(self, state_dict: Dict) -> Dict:
        query = state_dict["user_query"]
        
        results = []
        
        # Check for mathematical expressions
        math_patterns = re.findall(r'[0-9+\-*/().\s]+', query)
        if math_patterns:
            for pattern in math_patterns:
                if any(op in pattern for op in ['+', '-', '*', '/']):
                    calc_result = advanced_calculator.invoke({"expression": pattern})
                    results.append(calc_result)
        
        # Check for data visualization needs
        viz_keywords = ["chart", "graph", "visualize", "plot"]
        if any(keyword in query.lower() for keyword in viz_keywords):
            viz_result = data_visualizer.invoke({"data_description": query})
            results.append(viz_result)
        
        # Default analysis if no specific calculations
        if not results:
            results.append("📊 Analysis completed: Data patterns and insights identified.")
        
        state_dict["agent_results"]["analysis"] = " | ".join(results)
        return state_dict

class WritingAgent:
    def __init__(self):
        self.name = "Writing"
    
    def create_content(self, state_dict: Dict) -> Dict:
        query = state_dict["user_query"]
        
        # Determine content style
        style = "informative"
        if "summary" in query.lower():
            style = "summary"
        elif "technical" in query.lower():
            style = "technical"
        elif "creative" in query.lower():
            style = "creative"
        
        content = content_generator.invoke({"topic": query, "style": style})
        
        # Enhance with research results if available
        if "research" in state_dict["agent_results"]:
            content += f"\n\nBased on research findings: {state_dict['agent_results']['research']}"
        
        state_dict["agent_results"]["writing"] = content
        return state_dict

# Simple Agent System (from original notebook)
class SimpleAgent:
    def __init__(self):
        self.name = "Simple Agent"
    
    def process_query(self, user_input: str) -> Dict[str, Any]:
        """Process query with simple routing logic"""
        state = {
            "user_input": user_input,
            "needs_math": self._check_math_need(user_input),
            "result": ""
        }
        
        if state["needs_math"]:
            state = self._do_math(state)
        else:
            state = self._chat_response(state)
        
        return state
    
    def _check_math_need(self, user_input: str) -> bool:
        user_input = user_input.lower()
        math_keywords = ["calculate", "what is", "+", "-", "*", "/", "plus", "minus", "times"]
        has_numbers = bool(re.search(r'\d', user_input))
        has_math_words = any(word in user_input for word in math_keywords)
        return has_numbers and has_math_words
    
    def _do_math(self, state: Dict) -> Dict:
        user_input = state["user_input"]
        math_pattern = r'[0-9+\-*/().\s]+'
        matches = re.findall(math_pattern, user_input)
        
        if matches:
            expression = matches[0].strip()
            result = advanced_calculator.invoke({"expression": expression})
            state["result"] = f"The answer is: {result}"
        else:
            state["result"] = "I couldn't find a math expression to calculate."
        
        return state
    
    def _chat_response(self, state: Dict) -> Dict:
        user_input = state["user_input"].lower()
        
        responses = {
            "how are you": "I'm doing great! I'm a helpful AI agent that can chat and do math calculations.",
            "who are you": "I'm a simple LangGraph agent. I can help with conversations and mathematical calculations!",
            "hello": "Hello! How can I help you today? I can chat or help with math calculations.",
            "hi": "Hi there! How can I help you today? I can chat or help with math calculations."
        }
        
        for pattern, response in responses.items():
            if pattern in user_input:
                state["result"] = response
                return state
        
        # Default response
        state["result"] = "I'm a helpful AI assistant. I can help with math calculations and simple conversations!"
        return state