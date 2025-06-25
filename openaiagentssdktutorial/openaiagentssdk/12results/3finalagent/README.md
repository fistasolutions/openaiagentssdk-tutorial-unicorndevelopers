# 🎯 Final Agent Management with OpenAI Agents SDK

## 📚 Overview

This tutorial demonstrates how to manage and utilize the `last_agent` property from RunResult objects in the OpenAI Agents SDK. You'll learn how to continue conversations with the same agent that performed the previous execution, enabling seamless multi-agent workflows and conversation continuity.

## 🔍 Key Concepts Explained

### 🎯 What is Final Agent Management?

- **Agent Continuity**: Continuing conversations with the same agent
- **Workflow Management**: Managing multi-agent systems effectively
- **Context Preservation**: Maintaining agent-specific context and behavior
- **Handoff Support**: Supporting agent-to-agent transitions

### 🎯 The `last_agent` Property

The `last_agent` property:
- **Identifies Agent**: Shows which agent performed the last execution
- **Enables Continuity**: Allows continuing with the same agent
- **Preserves Context**: Maintains agent-specific instructions and behavior
- **Supports Handoffs**: Enables agent-to-agent transitions

### 🔄 Agent Workflow Patterns

```
Agent A → Result → last_agent (Agent A) → Continue with Agent A
   ↓         ↓           ↓                    ↓
Initial   Response   Agent Reference    Follow-up with same agent
```

## 🎯 What You'll Learn

- How to use `last_agent` for conversation continuity
- Managing multi-agent workflows
- Building agent handoff systems
- Understanding agent persistence
- Creating seamless conversation flows

## 🔧 Prerequisites

- Python 3.7+ installed
- Basic understanding of Python programming
- Knowledge of agent basics (from previous tutorials)
- OpenAI API key
- Understanding of environment variables

## 📦 Required Dependencies

```bash
pip install openai-agents python-dotenv
```

## 🏗️ Project Structure

```
3finalagent/
├── 3finalagent.py    # Main script file
└── README.md         # This file
```

## 🔑 Environment Setup

Create a `.env` file in your project root with:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 📖 Code Explanation

### 1. Import Statements

```python
from agents import Agent, Runner, set_default_openai_key
from dotenv import load_dotenv
import os
```

**What each import does:**
- `Agent`: The main class for creating AI agents
- `Runner`: Utility class for running agents
- `set_default_openai_key`: Sets the default API key for the SDK
- `load_dotenv`: Loads environment variables from `.env` file
- `os`: For accessing environment variables

### 2. Environment Configuration

```python
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
```

**Step-by-step explanation:**
1. `load_dotenv()`: Reads the `.env` file and loads variables
2. `set_default_openai_key()`: Sets the API key for the SDK

### 3. Multi-Agent Setup

```python
# Define two agents: a triage and a specialist
triage_agent = Agent(
    name="Triage Agent",
    instructions="Route to the correct agent if necessary, or answer simply."
)

specialist_agent = Agent(
    name="Specialist Agent",
    instructions="You are a detailed assistant specialized in answering tech questions."
)
```

**Agent Configuration:**
- **Triage Agent**: General-purpose agent for initial routing
- **Specialist Agent**: Specialized agent for detailed technical answers
- Each agent has distinct instructions and behavior

### 4. Initial Agent Execution

```python
# Simulate a handoff manually for the example
result = Runner.run_sync(specialist_agent, "What is an API?")
print("🔹 Final output:", result.final_output)
```

**What happens here:**
1. Specialist agent receives the technical question
2. Generates a detailed response about APIs
3. The result object contains the response and agent reference

### 5. Using last_agent for Continuity

```python
# Use last_agent to continue the conversation
follow_up_input = result.to_input_list() + [{"role": "user", "content": "Can you give an example of an API?"}]
next_result = Runner.run_sync(result.last_agent, follow_up_input)
print("🔹 Follow-up answer:", next_result.final_output)
```

**Continuity Breakdown:**
- `result.last_agent`: References the specialist agent that performed the previous execution
- `Runner.run_sync(result.last_agent, follow_up_input)`: Continues with the same agent
- The specialist agent maintains its specialized behavior and context

## 🚀 How to Run

1. **Navigate to the directory:**
   ```bash
   cd 3finalagent
   ```

2. **Set up your environment:**
   - Create a `.env` file with your OpenAI API key
   - Install dependencies: `pip install openai-agents python-dotenv`

3. **Run the script:**
   ```bash
   uv run 3finalagent.py
   ```

## 📝 Expected Output

```
🔹 Final output: An API (Application Programming Interface) is a set of rules and protocols that allows different software applications to communicate with each other...
🔹 Follow-up answer: Here's an example: The Twitter API allows developers to access Twitter data and functionality...
```

## 🛠️ Customization Ideas

1. **Dynamic agent selection:**
   ```python
   def select_agent(topic):
       if "tech" in topic.lower():
           return specialist_agent
       else:
           return triage_agent
   
   # Use the selected agent
   selected_agent = select_agent("What is machine learning?")
   result = Runner.run_sync(selected_agent, "What is machine learning?")
   ```

2. **Agent handoff system:**
   ```python
   def handle_conversation(user_input):
       # Start with triage agent
       result = Runner.run_sync(triage_agent, user_input)
       
       # Check if specialist is needed
       if "technical" in result.final_output.lower():
           # Handoff to specialist
           specialist_result = Runner.run_sync(specialist_agent, user_input)
           return specialist_result
       
       return result
   ```

3. **Multi-agent conversation:**
   ```python
   # Create a conversation with multiple agents
   agents = {
       "general": Agent(name="General", instructions="Answer general questions."),
       "tech": Agent(name="Tech", instructions="Answer technical questions."),
       "creative": Agent(name="Creative", instructions="Answer creative questions.")
   }
   ```

## 🎯 Building Advanced Agent Management

### Agent Router Class

```python
class AgentRouter:
    def __init__(self):
        self.agents = {
            "general": Agent(name="General", instructions="Answer general questions."),
            "tech": Agent(name="Tech", instructions="Answer technical questions."),
            "creative": Agent(name="Creative", instructions="Answer creative questions.")
        }
        self.current_agent = None
    
    def route_question(self, question):
        # Simple routing logic
        if any(word in question.lower() for word in ["api", "code", "programming", "software"]):
            self.current_agent = self.agents["tech"]
        elif any(word in question.lower() for word in ["story", "creative", "art", "design"]):
            self.current_agent = self.agents["creative"]
        else:
            self.current_agent = self.agents["general"]
        
        return self.current_agent
    
    def continue_conversation(self, result, follow_up):
        # Continue with the last agent used
        follow_up_input = result.to_input_list() + [{"role": "user", "content": follow_up}]
        return Runner.run_sync(result.last_agent, follow_up_input)
```

### Intelligent Agent Handoff

```python
def intelligent_handoff(initial_agent, user_input, result):
    """Intelligently decide if agent handoff is needed"""
    
    # Analyze the result to determine if specialist is needed
    response = result.final_output.lower()
    
    # Check for indicators that specialist knowledge is needed
    tech_indicators = ["api", "programming", "code", "software", "technical"]
    creative_indicators = ["creative", "story", "art", "design", "imaginative"]
    
    if any(indicator in response for indicator in tech_indicators):
        # Handoff to tech specialist
        specialist = Agent(name="Tech Specialist", instructions="Provide detailed technical explanations.")
        return Runner.run_sync(specialist, user_input)
    
    elif any(indicator in response for indicator in creative_indicators):
        # Handoff to creative specialist
        creative = Agent(name="Creative Specialist", instructions="Provide creative and imaginative responses.")
        return Runner.run_sync(creative, user_input)
    
    # Continue with current agent
    return result
```

### Agent State Management

```python
class AgentStateManager:
    def __init__(self):
        self.agent_history = []
        self.current_agent = None
    
    def execute_with_agent(self, agent, input_data):
        """Execute with a specific agent and track state"""
        result = Runner.run_sync(agent, input_data)
        
        # Track agent usage
        self.agent_history.append({
            "agent": agent.name,
            "input": input_data,
            "output": result.final_output
        })
        
        self.current_agent = result.last_agent
        return result
    
    def get_agent_history(self):
        """Get history of agent usage"""
        return self.agent_history
    
    def get_current_agent(self):
        """Get the current active agent"""
        return self.current_agent
```

## 🎯 When to Use Final Agent Management

### ✅ **Use final agent management when:**
- Building multi-agent systems
- Creating agent handoff workflows
- Need conversation continuity
- Implementing specialized agent routing
- Building complex AI applications

### ❌ **Don't use final agent management when:**
- Simple single-agent applications
- Stateless operations
- Performance-critical systems
- Basic Q&A applications

## ⚠️ Common Issues & Solutions

### Issue: "Agent not found in last_agent"
**Solution:** Ensure the agent was properly executed and result is valid

### Issue: "Context lost during handoff"
**Solution:** Use `to_input_list()` to preserve conversation context

### Issue: "Wrong agent selected"
**Solution:** Implement better routing logic and agent selection criteria

### Issue: "ModuleNotFoundError: No module named 'agents'"
**Solution:** Install the SDK: `pip install openai-agents`

## 🔗 Related Topics

- [RunResult Properties](../1results/)
- [Input and Next Steps](../2inputnext/)
- [New Items Processing](../4newitem/)
- [Agent Loops](../../11runningagents/4agentloop/)
- [Conversation Management](../../11runningagents/6conversation/)

## 📚 Additional Resources

- [OpenAI Agents SDK Documentation](https://github.com/openai/openai-agents)
- [Multi-Agent Systems](https://en.wikipedia.org/wiki/Multi-agent_system)
- [Agent-Based Modeling](https://en.wikipedia.org/wiki/Agent-based_model)

## 🎉 Next Steps

Once you understand final agent management, try:
1. Building intelligent agent routing systems
2. Implementing dynamic agent selection
3. Creating agent handoff workflows
4. Building multi-agent conversation systems

---

**Happy Coding! 🚀**

*This tutorial is part of the OpenAI Agents SDK learning series.* 