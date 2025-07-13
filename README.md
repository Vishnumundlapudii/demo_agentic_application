# 🤖 Multi-Agent AI System Demo

An interactive Streamlit application showcasing hierarchical multi-agent collaboration using LangGraph.

## 🏗️ Architecture

### Multi-Agent System
- **🎯 Coordinator Agent**: Plans tasks, routes to specialists, aggregates results
- **🔍 Research Agent**: Web search, information gathering
- **📊 Analysis Agent**: Mathematical calculations, data visualization  
- **✍️ Writing Agent**: Content creation, report generation

### Simple Agent System
- **⚡ Simple Agent**: Basic math calculations and conversations

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit App
```bash
streamlit run streamlit_app.py
```

### 3. Open in Browser
Visit `http://localhost:8501` to access the demo interface.

## 📱 Features

### 🎮 Interactive Interface
- **Agent Selection**: Choose between Multi-Agent or Simple Agent systems
- **Example Queries**: Pre-built examples for different use cases
- **Real-time Processing**: Watch agents collaborate in real-time
- **Conversation History**: Track previous interactions

### 🤖 Agent Capabilities

#### Multi-Agent System
- **Research + Analysis**: "What is AI and calculate 10 + 5?"
- **Analysis + Writing**: "Calculate 15 * 25 and write a summary"
- **Research + Writing**: "Research Python and create documentation"

#### Simple Agent System  
- **Math Calculations**: "What is 100 / 4?"
- **Basic Conversations**: "How are you?"

### 📊 Execution Tracking
- **Execution Plan**: See which agents will be used
- **Agent Results**: View individual agent outputs
- **Performance Metrics**: Execution time and steps
- **Metadata**: Agents used, duration, timestamps

## 📁 Project Structure

```
├── streamlit_app.py          # Main Streamlit application
├── agents.py                 # Individual agent implementations
├── multi_agent_workflow.py   # LangGraph workflow orchestration
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── Multi_Agent_System.ipynb  # Jupyter notebook implementation
└── Simple_LangGraph_Agent.ipynb  # Simple agent notebook
```

## 🔧 Technical Details

### Technologies Used
- **Streamlit**: Web interface framework
- **LangGraph**: Multi-agent workflow orchestration
- **LangChain**: Agent tools and utilities
- **Python**: Core implementation language

### Key Components

#### Agent Tools
```python
@tool
def web_search(query: str) -> str:
    """Simulate web search for research tasks"""

@tool  
def advanced_calculator(expression: str) -> str:
    """Advanced mathematical calculations"""

@tool
def content_generator(topic: str, style: str) -> str:
    """Generate content based on topic and style"""
```

#### Workflow Management
```python
# Dynamic routing based on task plan
def route_to_next_agent(state: Dict) -> str:
    """Determine which agent to execute next"""

# Conditional execution flow
workflow.add_conditional_edges(
    "start_coordination",
    route_to_next_agent,
    {
        "execute_research": "execute_research",
        "execute_analysis": "execute_analysis", 
        "execute_writing": "execute_writing"
    }
)
```

## 🎯 Example Use Cases

### 1. Research + Analysis
**Query**: "What is machine learning and calculate the average of 10, 20, 30?"

**Execution**:
1. **Coordinator** → Plans: [Research, Analysis]
2. **Research Agent** → Gathers ML information
3. **Analysis Agent** → Calculates average (20)
4. **Coordinator** → Combines results

### 2. Analysis + Writing
**Query**: "Calculate 15 * 25 and write a technical summary"

**Execution**:
1. **Coordinator** → Plans: [Analysis, Writing]
2. **Analysis Agent** → Calculates 15 * 25 = 375
3. **Writing Agent** → Creates technical summary
4. **Coordinator** → Aggregates final content

### 3. Complex Multi-Step
**Query**: "Research AI, calculate 100/4, and generate creative content"

**Execution**:
1. **Coordinator** → Plans: [Research, Analysis, Writing]
2. **Research Agent** → AI information gathering
3. **Analysis Agent** → Mathematical calculation
4. **Writing Agent** → Creative content creation
5. **Coordinator** → Final result aggregation

## 🛠️ Customization

### Adding New Agents
1. Create agent class in `agents.py`
2. Add workflow function in `multi_agent_workflow.py`
3. Update routing logic
4. Register in Streamlit interface

### Adding New Tools
```python
@tool
def your_custom_tool(input_param: str) -> str:
    """Your tool description"""
    # Implementation
    return result
```

### Extending UI
- Modify `streamlit_app.py` for new features
- Add new example queries
- Customize visualization components

## 🎮 Demo Scenarios

Try these queries to see different agent collaborations:

### Research-Heavy
- "What is blockchain technology?"
- "Tell me about quantum computing"
- "Research artificial intelligence trends"

### Analysis-Heavy  
- "Calculate the sum of 1,2,3,4,5 and show statistics"
- "What is 50 * 30 + 100 / 2?"
- "Find average of 10,20,30,40,50 and visualize"

### Writing-Heavy
- "Create a technical summary about Python"
- "Write creative content about space exploration"  
- "Generate documentation for API usage"

### Multi-Modal
- "Research climate change and calculate 25 * 4"
- "What is data science and write a summary?"
- "Calculate 100/5 and create a report about it"

## 📈 Performance Notes

- **Multi-Agent System**: Best for complex, multi-step tasks
- **Simple Agent**: Optimal for quick calculations and basic Q&A
- **Processing Time**: Varies based on query complexity and agent count
- **Scalability**: Easy to add new agents and capabilities

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Implement new agents or tools
4. Test with Streamlit interface
5. Submit pull request

## 📄 License

This project is open source. Feel free to use and modify for educational and research purposes.