# 🔄 Input Management and Follow-up Conversations

## 📚 Overview

This tutorial demonstrates how to manage input context and create follow-up conversations using the `to_input_list()` method from the OpenAI Agents SDK. You'll learn how to maintain conversation context across multiple interactions and build coherent multi-turn dialogues.

## 🔍 Key Concepts Explained

### 🔄 What is Input Management?

- **Context Preservation**: Maintaining conversation history across turns
- **Follow-up Support**: Enabling natural conversation flow
- **State Continuity**: Ensuring agents remember previous interactions
- **Input Transformation**: Converting results to reusable input format

### 🎯 The `to_input_list()` Method

The `to_input_list()` method:
- **Converts Results**: Transforms RunResult objects into conversation format
- **Preserves Context**: Maintains the full conversation history
- **Enables Continuity**: Allows agents to reference previous exchanges
- **Standardizes Format**: Creates consistent input structure

### 🔗 Conversation Flow

```
Initial Input → Agent Response → to_input_list() → Follow-up Input → Agent Response
     ↓              ↓                ↓                ↓              ↓
  "Question"    "Answer"      [{"role": "user",      "Follow-up"   "Answer"
                              "content": "Question"}, 
                              {"role": "assistant", 
                               "content": "Answer"}]
```

## 🎯 What You'll Learn

- How to use `to_input_list()` for context preservation
- Building follow-up conversations with agents
- Managing conversation state across multiple turns
- Creating natural dialogue flows
- Understanding input transformation

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
2inputnext/
├── 2inputnext.py    # Main script file
└── README.md        # This file
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
# Load environment variables and OpenAI key
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
```

**Step-by-step explanation:**
1. `load_dotenv()`: Reads the `.env` file and loads variables
2. `set_default_openai_key()`: Sets the API key for the SDK

### 3. Agent Creation

```python
# Define the assistant agent
agent = Agent(
    name="Concise Assistant",
    instructions="Reply briefly but accurately.",
    model="gpt-4o"
)
```

**Agent Configuration:**
- `name`: "Concise Assistant" - emphasizes brief responses
- `instructions`: Clear directive for concise but accurate answers
- `model`: Using "gpt-4o" for optimal performance

### 4. First Interaction

```python
# Step 1: First user input
first_result = Runner.run_sync(agent, "What city is the Golden Gate Bridge in?")
print("📍 First answer:", first_result.final_output)
```

**What happens here:**
1. Agent receives the initial question about the Golden Gate Bridge
2. Generates a response (expected: "San Francisco")
3. The result object contains the response and context

### 5. Context Preservation

```python
# Step 2: Use `.to_input_list()` to maintain context, and ask a follow-up
follow_up_input = first_result.to_input_list() + [{"role": "user", "content": "What state is that in?"}]
```

**Context Building Breakdown:**
- `first_result.to_input_list()`: Converts the first conversation to list format
- `+ [{"role": "user", "content": "What state is that in?"}]`: Adds the follow-up question
- The agent now has context: "Golden Gate Bridge is in San Francisco" + "What state is that in?"

### 6. Follow-up Interaction

```python
second_result = Runner.run_sync(agent, follow_up_input)
print("📍 Follow-up answer:", second_result.final_output)
```

**What happens here:**
1. Agent receives the full conversation context
2. Understands "that" refers to San Francisco from the previous turn
3. Generates a contextual response (expected: "California")

## 🚀 How to Run

1. **Navigate to the directory:**
   ```bash
   cd 2inputnext
   ```

2. **Set up your environment:**
   - Create a `.env` file with your OpenAI API key
   - Install dependencies: `pip install openai-agents python-dotenv`

3. **Run the script:**
   ```bash
   uv run 2inputnext.py
   ```

## 📝 Expected Output

```
📍 First answer: San Francisco
📍 Follow-up answer: California
```

## 🛠️ Customization Ideas

1. **Extended conversation chain:**
   ```python
   # Third follow-up
   third_input = second_result.to_input_list() + [{"role": "user", "content": "What's the weather like there?"}]
   third_result = Runner.run_sync(agent, third_input)
   print("📍 Third answer:", third_result.final_output)
   ```

2. **Multi-topic conversation:**
   ```python
   # Start with one topic
   result1 = Runner.run_sync(agent, "Tell me about Python programming.")
   
   # Switch to related topic while maintaining context
   follow_up = result1.to_input_list() + [{"role": "user", "content": "How does that compare to JavaScript?"}]
   result2 = Runner.run_sync(agent, follow_up)
   ```

3. **Conversation with specific context:**
   ```python
   agent = Agent(
       name="TravelGuide",
       instructions="You are a travel guide. Remember places mentioned and provide detailed information.",
       model="gpt-4o"
   )
   ```

## 🔄 Building Advanced Input Management

### Conversation Class

```python
class ConversationManager:
    def __init__(self, agent):
        self.agent = agent
        self.conversation_history = []
    
    def add_message(self, role, content):
        self.conversation_history.append({"role": role, "content": content})
    
    def get_response(self, user_message):
        # Add user message
        self.add_message("user", user_message)
        
        # Get agent response
        result = Runner.run_sync(self.agent, self.conversation_history)
        
        # Add agent response
        self.add_message("assistant", result.final_output)
        
        return result.final_output
    
    def get_context(self):
        return self.conversation_history.copy()
```

### Using to_input_list() for Complex Scenarios

```python
def build_contextual_conversation(agent, initial_question, follow_ups):
    """Build a conversation with multiple follow-ups"""
    # Initial question
    result = Runner.run_sync(agent, initial_question)
    print(f"Q: {initial_question}")
    print(f"A: {result.final_output}")
    
    # Process follow-ups
    current_context = result.to_input_list()
    
    for follow_up in follow_ups:
        # Add follow-up to context
        new_input = current_context + [{"role": "user", "content": follow_up}]
        
        # Get response
        result = Runner.run_sync(agent, new_input)
        print(f"Q: {follow_up}")
        print(f"A: {result.final_output}")
        
        # Update context for next iteration
        current_context = result.to_input_list()
    
    return result
```

### Context Management Utilities

```python
def limit_context(conversation_list, max_turns=10):
    """Limit conversation history to prevent token overflow"""
    if len(conversation_list) > max_turns * 2:  # Each turn has 2 messages
        return conversation_list[-max_turns * 2:]
    return conversation_list

def summarize_context(conversation_list):
    """Create a summary of the conversation for long contexts"""
    if len(conversation_list) > 20:
        # Keep first and last few messages, summarize the middle
        summary = [
            conversation_list[0],  # First user message
            {"role": "assistant", "content": "[Previous conversation summarized]"},
            conversation_list[-2],  # Last user message
            conversation_list[-1]   # Last assistant message
        ]
        return summary
    return conversation_list
```

## 🔄 When to Use Input Management

### ✅ **Use input management when:**
- Building chat applications
- Creating conversational AI
- Need context preservation
- Multi-step problem solving
- Interactive applications

### ❌ **Don't use input management when:**
- Simple one-off questions
- Batch processing
- Stateless operations
- Performance-critical applications

## ⚠️ Common Issues & Solutions

### Issue: "Context too long"
**Solution:** Implement conversation history limits or summarization

### Issue: "Agent forgets previous context"
**Solution:** Ensure `to_input_list()` is used correctly

### Issue: "Performance degradation over time"
**Solution:** Use context management to limit conversation length

### Issue: "ModuleNotFoundError: No module named 'agents'"
**Solution:** Install the SDK: `pip install openai-agents`

## 🔗 Related Topics

- [RunResult Properties](../1results/)
- [Final Agent Management](../3finalagent/)
- [New Items Processing](../4newitem/)
- [Conversation Management](../../11runningagents/6conversation/)
- [Agent Loops](../../11runningagents/4agentloop/)

## 📚 Additional Resources

- [OpenAI Agents SDK Documentation](https://github.com/openai/openai-agents)
- [Building Chatbots with Python](https://realpython.com/python-chatbot/)
- [Conversation Design Principles](https://developers.google.com/assistant/conversation-design)

## 🎉 Next Steps

Once you understand input management, try:
1. Building complete chat applications
2. Implementing conversation memory persistence
3. Adding context summarization
4. Creating specialized conversation agents

---

**Happy Coding! 🚀**

*This tutorial is part of the OpenAI Agents SDK learning series.* 