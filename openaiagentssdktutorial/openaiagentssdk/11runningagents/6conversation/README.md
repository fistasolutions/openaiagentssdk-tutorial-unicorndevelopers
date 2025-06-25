# 💬 Conversation Management with OpenAI Agents SDK

## 📚 Overview

This tutorial demonstrates how to manage multi-turn conversations with AI agents using the OpenAI Agents SDK. You'll learn how to maintain conversation context across multiple interactions, allowing agents to remember previous exchanges and build upon them.

## 🔍 Key Concepts Explained

### 💬 What is Conversation Management?

- **Context Preservation**: Agents remember previous interactions
- **Multi-turn Dialogue**: Support for back-and-forth conversations
- **State Continuity**: Maintaining conversation history across turns
- **Contextual Responses**: Agents can reference previous information

### 🎯 Conversation Components

A conversation typically includes:
- **Conversation History**: List of previous messages
- **Turn Management**: Handling multiple exchanges
- **Context Building**: Accumulating information over time
- **Response Generation**: Creating contextually aware responses

### 🔄 Single Turn vs Multi-turn

| Approach | Context | Memory | Use Case |
|----------|---------|--------|----------|
| **Single Turn** | None | No | Simple Q&A |
| **Multi-turn** | Full history | Yes | Conversations, complex tasks |

## 🎯 What You'll Learn

- How to maintain conversation context across multiple turns
- Using `to_input_list()` to preserve conversation history
- Building contextual conversations with agents
- Managing conversation state effectively

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
6conversation/
├── 6conversation.py    # Main script file
└── README.md           # This file
```

## 🔑 Environment Setup

Create a `.env` file in your project root with:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
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
# Load and set your OpenAI API key
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
model=os.environ.get("OPENAI_MODEL")
```

**Step-by-step explanation:**
1. `load_dotenv()`: Reads the `.env` file and loads variables
2. `set_default_openai_key()`: Sets the API key for the SDK
3. `os.environ.get("OPENAI_MODEL")`: Gets the model from environment

### 3. Agent Creation

```python
# Create the agent
agent = Agent(
    name="Assistant",
    instructions="Reply very concisely.",
    model=model
)
```

**Agent Configuration:**
- `name`: "Assistant" - general-purpose conversational agent
- `instructions`: "Reply very concisely" - encourages brief responses
- `model`: Uses the model specified in environment variables

### 4. First Turn - Initial Question

```python
# First turn
result1 = Runner.run_sync(agent, "What city is the Golden Gate Bridge in?")
print("Turn 1 Output:", result1.final_output)  # Expected: San Francisco
```

**What happens here:**
1. Agent receives the initial question about the Golden Gate Bridge
2. Generates a response (expected: "San Francisco")
3. The result object contains the response and conversation context

### 5. Context Preservation

```python
# Prepare input for second turn using previous context + new user message
second_input = result1.to_input_list() + [{"role": "user", "content": "What state is it in?"}]
```

**Context Building Breakdown:**
- `result1.to_input_list()`: Converts the first conversation to a list format
- `+ [{"role": "user", "content": "What state is it in?"}]`: Adds the new question
- The agent now has context: "Golden Gate Bridge is in San Francisco" + "What state is it in?"

### 6. Second Turn - Contextual Question

```python
# Second turn
result2 = Runner.run_sync(agent, second_input)
print("Turn 2 Output:", result2.final_output)  # Expected: California
```

**What happens here:**
1. Agent receives the full conversation context
2. Understands "it" refers to San Francisco from the previous turn
3. Generates a contextual response (expected: "California")

## 🚀 How to Run

1. **Navigate to the directory:**
   ```bash
   cd 6conversation
   ```

2. **Set up your environment:**
   - Create a `.env` file with your OpenAI API key and model
   - Install dependencies: `pip install openai-agents python-dotenv`

3. **Run the script:**
   ```bash
   uv run 6conversation.py
   ```

## 📝 Expected Output

```
Turn 1 Output: San Francisco
Turn 2 Output: California
```

## 🛠️ Customization Ideas

1. **Extended conversation:**
   ```python
   # Third turn
   third_input = result2.to_input_list() + [{"role": "user", "content": "What's the weather like there?"}]
   result3 = Runner.run_sync(agent, third_input)
   print("Turn 3 Output:", result3.final_output)
   ```

2. **Conversation with multiple topics:**
   ```python
   # Start with one topic
   result1 = Runner.run_sync(agent, "Tell me about Python programming.")
   
   # Switch to another topic while maintaining context
   second_input = result1.to_input_list() + [{"role": "user", "content": "How does that compare to JavaScript?"}]
   result2 = Runner.run_sync(agent, second_input)
   ```

3. **Conversation with specific instructions:**
   ```python
   agent = Agent(
       name="TravelGuide",
       instructions="You are a travel guide. Remember places mentioned and provide detailed information.",
       model=model
   )
   ```

## 💬 Building Advanced Conversations

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
    
    def get_history(self):
        return self.conversation_history.copy()
```

### Interactive Conversation

```python
# Initialize conversation
conversation = ConversationManager(agent)

# Interactive loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ['quit', 'exit', 'bye']:
        print("Goodbye!")
        break
    
    response = conversation.get_response(user_input)
    print(f"Assistant: {response}")
```

### Context Management

```python
def manage_context(conversation_history, max_turns=10):
    """Limit conversation history to prevent token overflow"""
    if len(conversation_history) > max_turns * 2:  # Each turn has 2 messages
        # Keep the most recent messages
        return conversation_history[-max_turns * 2:]
    return conversation_history
```

## 💬 When to Use Conversation Management

### ✅ **Use conversation management when:**
- Building chat applications
- Creating conversational AI
- Need context preservation
- Multi-step problem solving
- Interactive applications

### ❌ **Don't use conversation management when:**
- Simple one-off questions
- Batch processing
- Stateless operations
- Performance-critical applications

## ⚠️ Common Issues & Solutions

### Issue: "Agent forgets previous context"
**Solution:** Ensure `to_input_list()` is used to preserve conversation history

### Issue: "Context too long"
**Solution:** Implement conversation history limits or summarization

### Issue: "Performance degradation over time"
**Solution:** Use context management to limit conversation length

### Issue: "ModuleNotFoundError: No module named 'agents'"
**Solution:** Install the SDK: `pip install openai-agents`

## 🔗 Related Topics

- [Synchronous Agent Execution](../1runsync/)
- [Asynchronous Agent Execution](../2runasync/)
- [Streaming Responses](../3runasyncstreaming/)
- [Agent Loops](../4agentloop/)
- [Configuration Management](../5runconfig/)
- [Exception Handling](../7exception/)

## 📚 Additional Resources

- [OpenAI Agents SDK Documentation](https://github.com/openai/openai-agents)
- [Building Chatbots with Python](https://realpython.com/python-chatbot/)
- [Conversation Design Principles](https://developers.google.com/assistant/conversation-design)

## 🎉 Next Steps

Once you understand conversation management, try:
1. Building a complete chat application
2. Implementing conversation memory persistence
3. Adding context summarization
4. Creating specialized conversation agents

---

**Happy Coding! 🚀**

*This tutorial is part of the OpenAI Agents SDK learning series.* 