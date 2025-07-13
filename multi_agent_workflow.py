"""
Multi-Agent Workflow Implementation
LangGraph-based orchestration for agent coordination
"""

from typing import Dict, Any
from langgraph.graph import StateGraph, END
from agents import CoordinatorAgent, ResearchAgent, AnalysisAgent, WritingAgent
from datetime import datetime

# Initialize agents
coordinator = CoordinatorAgent()
research_agent = ResearchAgent()
analysis_agent = AnalysisAgent()
writing_agent = WritingAgent()

# Workflow functions
def start_coordination(state: Dict) -> Dict:
    """Entry point - coordinator plans the task"""
    return coordinator.plan_task(state)

def execute_research(state: Dict) -> Dict:
    """Research agent gathers information"""
    return research_agent.gather_information(state)

def execute_analysis(state: Dict) -> Dict:
    """Analysis agent processes data"""
    return analysis_agent.process_data(state)

def execute_writing(state: Dict) -> Dict:
    """Writing agent creates content"""
    return writing_agent.create_content(state)

def finalize_results(state: Dict) -> Dict:
    """Coordinator aggregates all results"""
    return coordinator.aggregate_results(state)

# Dynamic routing functions
def route_to_next_agent(state: Dict) -> str:
    """Determine which agent to execute next"""
    current_step = state["current_step"]
    task_plan = state["task_plan"]
    
    if current_step >= len(task_plan):
        return "finalize"
    
    next_task = task_plan[current_step]
    agent_type = next_task["agent"]
    
    # Update step counter
    state["current_step"] += 1
    
    return f"execute_{agent_type}"

def should_continue(state: Dict) -> str:
    """Check if more agents need to execute"""
    current_step = state["current_step"]
    total_steps = len(state["task_plan"])
    
    if current_step < total_steps:
        return "continue"
    else:
        return "finalize"

# Build the Multi-Agent Graph
def create_multi_agent_workflow():
    """Create and compile the multi-agent workflow"""
    
    # Create the workflow graph
    multi_agent_workflow = StateGraph(dict)

    # Add all agent nodes
    multi_agent_workflow.add_node("start_coordination", start_coordination)
    multi_agent_workflow.add_node("execute_research", execute_research)
    multi_agent_workflow.add_node("execute_analysis", execute_analysis)
    multi_agent_workflow.add_node("execute_writing", execute_writing)
    multi_agent_workflow.add_node("finalize_results", finalize_results)

    # Set entry point
    multi_agent_workflow.set_entry_point("start_coordination")

    # Add conditional routing from coordinator
    multi_agent_workflow.add_conditional_edges(
        "start_coordination",
        route_to_next_agent,
        {
            "execute_research": "execute_research",
            "execute_analysis": "execute_analysis", 
            "execute_writing": "execute_writing",
            "finalize": "finalize_results"
        }
    )

    # Add conditional routing from each agent back to coordinator
    for agent_node in ["execute_research", "execute_analysis", "execute_writing"]:
        multi_agent_workflow.add_conditional_edges(
            agent_node,
            should_continue,
            {
                "continue": "start_coordination",
                "finalize": "finalize_results"
            }
        )

    # End at finalize
    multi_agent_workflow.add_edge("finalize_results", END)

    # Compile the multi-agent system
    return multi_agent_workflow.compile()

class MultiAgentSystem:
    """High-level interface for the multi-agent system"""
    
    def __init__(self):
        self.workflow = create_multi_agent_workflow()
        self.conversation_history = []
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a query through the multi-agent system"""
        
        # Create initial state
        initial_state = {
            "user_query": query,
            "task_plan": [],
            "agent_results": {},
            "final_result": "",
            "current_step": 0,
            "metadata": {
                "start_time": datetime.now(),
                "agents_used": [],
                "total_steps": 0
            }
        }
        
        # Execute multi-agent workflow
        result = self.workflow.invoke(initial_state)
        
        # Add execution time
        if "end_time" in result["metadata"]:
            duration = result["metadata"]["end_time"] - result["metadata"]["start_time"]
            result["metadata"]["duration_seconds"] = duration.total_seconds()
        
        # Store in conversation history
        self.conversation_history.append({
            "timestamp": datetime.now(),
            "query": query,
            "result": result
        })
        
        return result
    
    def get_conversation_history(self) -> list:
        """Get the conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []