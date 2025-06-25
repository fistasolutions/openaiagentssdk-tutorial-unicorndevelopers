# 🔄 Agent Loops with OpenAI Agents SDK

## 📚 Overview

This tutorial demonstrates how to use agent loops with the OpenAI Agents SDK. Agent loops are a fundamental concept that allows agents to maintain context and have multi-turn conversations. This example shows the basic structure of how agents can be run in a loop-like manner.

## 🔍 Key Concepts Explained

### 🔄 What is an Agent Loop?

- **Context Preservation**: Agents remember previous interactions
- **Multi-turn Conversations**: Support for back-and-forth dialogue
- **State Management**: Maintains conversation history
- **Iterative Processing**: Agents can process information over multiple turns

### 🎯 Agent Loop Components

An agent loop typically consists of:
- **Agent Initialization**: Creating the agent with instructions
- **Input Processing**: Handling user messages
- **Response Generation**: Agent generates responses
- **Context Update**: Updating conversation history
- **Loop Continuation**: Preparing for next interaction

### 🔗 Loop vs Single Turn

| Approach | Context | Use Case |
|----------|---------|----------|
| **Single Turn** | No memory | Simple Q&A |
| **Agent Loop** | Maintains context | Conversations, complex tasks |

## 🎯 What You'll Learn

- Understanding agent loops and their importance
- How to structure agents for multi-turn conversations
- Context preservation in agent interactions
- Building conversational AI applications

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
4agentloop/
├── 4agentloop.py    # Main script file
└── README.md        # This file
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
from agents import Agent, Runner
from dotenv import load_dotenv
from agents import set_default_openai_key
import os
```

**What each import does:**
- `Agent`: The main class for creating AI agents
- `Runner`: Utility class for running agents
- `load_dotenv`: Loads environment variables from `.env` file
- `set_default_openai_key`: Sets the default API key for the SDK
- `os`: For accessing environment variables

### 2. Environment Configuration

```python
# Load OpenAI API key
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
openai_model = os.environ.get("OPENAI_MODEL")
```

**Step-by-step explanation:**
1. `load_dotenv()`: Reads the `.env` file and loads variables
2. `os.environ.get("OPENAI_API_KEY")`: Retrieves the API key
3. `set_default_openai_key()`: Sets the API key for the SDK
4. `os.environ.get("OPENAI_MODEL")`: Gets the model from environment

### 3. Agent Creation

```python
# Create agent
agent = Agent(
    name="LoopTester",
    instructions="You are a helpful assistant. Answer clearly.",
    model=openai_model
)
```

**Agent Configuration:**
- `name`: "LoopTester" - indicates this agent is designed for loop testing
- `instructions`: Clear instructions for helpful responses
- `model`: Uses the model specified in environment variables

### 4. Agent Loop Execution

```python
# Run synchronously using agent loop
result = Runner.run_sync(agent, "What is the capital of Pakistan?")
print("\n--- Final Output ---")
print(result.final_output)
```

**What happens here:**
1. `Runner.run_sync()` executes the agent with the initial message
2. The agent processes the question and generates a response
3. We print the final output with clear formatting
4. This sets up the foundation for loop-based interactions

## 🚀 How to Run

1. **Navigate to the directory:**
   ```bash
   cd 4agentloop
   ```

2. **Set up your environment:**
   - Create a `.env` file with your OpenAI API key and model
   - Install dependencies: `pip install openai-agents python-dotenv`

3. **Run the script:**
   ```bash
   uv run 4agentloop.py
   ```

## 📝 Expected Output

```
--- Final Output ---
Islamabad is the capital of Pakistan.
```

## 🛠️ Customization Ideas

1. **Create a true conversation loop:**
   ```python
   while True:
       user_input = input("You: ")
       if user_input.lower() == 'quit':
           break
       
       result = Runner.run_sync(agent, user_input)
       print(f"Assistant: {result.final_output}")
   ```

2. **Add conversation history:**
   ```python
   conversation_history = []
   
   def chat_with_agent(message):
       # Add user message to history
       conversation_history.append({"role": "user", "content": message})
       
       # Run agent with full context
       result = Runner.run_sync(agent, conversation_history)
       
       # Add agent response to history
       conversation_history.append({"role": "assistant", "content": result.final_output})
       
       return result.final_output
   ```

3. **Create a specialized loop agent:**
   ```python
   agent = Agent(
       name="ConversationBot",
       instructions="You are a friendly conversation partner. Remember what we've discussed and build on previous topics.",
       model=openai_model
   )
   ```

## 🔄 Building True Agent Loops

### Basic Loop Structure

```python
# Initialize agent
agent = Agent(name="ChatBot", instructions="Be helpful and remember our conversation.")

# Conversation loop
conversation_context = []

while True:
    # Get user input
    user_message = input("You: ")
    
    if user_message.lower() in ['quit', 'exit', 'bye']:
        print("Goodbye!")
        break
    
    # Add user message to context
    conversation_context.append({"role": "user", "content": user_message})
    
    # Run agent with full context
    result = Runner.run_sync(agent, conversation_context)
    
    # Add agent response to context
    conversation_context.append({"role": "assistant", "content": result.final_output})
    
    # Display response
    print(f"Assistant: {result.final_output}")
```

### Advanced Loop Features

1. **Context Management:**
   ```python
   # Limit conversation history to prevent token overflow
   if len(conversation_context) > 10:
       conversation_context = conversation_context[-10:]
   ```

2. **Error Handling:**
   ```python
   try:
       result = Runner.run_sync(agent, conversation_context)
   except Exception as e:
       print(f"Error: {e}")
       continue
   ```

3. **Memory Persistence:**
   ```python
   import json
   
   # Save conversation
   with open('conversation.json', 'w') as f:
       json.dump(conversation_context, f)
   
   # Load conversation
   with open('conversation.json', 'r') as f:
       conversation_context = json.load(f)
   ```

## 🔄 When to Use Agent Loops

### ✅ **Use agent loops when:**
- Building chat applications
- Creating conversational AI
- Need context preservation
- Multi-step problem solving
- Interactive applications

### ❌ **Don't use agent loops when:**
- Simple one-off questions
- Batch processing
- Stateless operations
- Performance-critical applications

## ⚠️ Common Issues & Solutions

### Issue: "Context too long"
**Solution:** Implement conversation history limits

### Issue: "Agent forgets previous context"
**Solution:** Ensure conversation history is properly passed to each run

### Issue: "Performance degradation over time"
**Solution:** Implement context summarization or truncation

### Issue: "ModuleNotFoundError: No module named 'agents'"
**Solution:** Install the SDK: `pip install openai-agents`

## 🔗 Related Topics

- [Synchronous Agent Execution](../1runsync/)
- [Asynchronous Agent Execution](../2runasync/)
- [Streaming Responses](../3runasyncstreaming/)
- [Configuration Management](../5runconfig/)
- [Conversation Management](../6conversation/)

## 📚 Additional Resources

- [OpenAI Agents SDK Documentation](https://github.com/openai/openai-agents)
- [Building Chatbots with Python](https://realpython.com/python-chatbot/)
- [Conversation Design Principles](https://developers.google.com/assistant/conversation-design)

## 🎉 Next Steps

Once you understand agent loops, try:
1. Building a complete chat application
2. Implementing conversation memory
3. Adding context management features
4. Creating specialized conversation agents

---

**Happy Coding! 🚀**

*This tutorial is part of the OpenAI Agents SDK learning series.* 