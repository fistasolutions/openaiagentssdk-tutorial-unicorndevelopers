# 🤖 Running Agents Synchronously with OpenAI Agents SDK

## 📚 Overview

This tutorial demonstrates how to create and run an AI agent synchronously using the OpenAI Agents SDK. This is the most basic way to interact with an AI agent - you send a message and wait for a response.

## 🎯 What You'll Learn

- How to set up the OpenAI Agents SDK
- How to create a basic AI agent
- How to run the agent synchronously
- How to handle environment variables for API keys
- Understanding the difference between synchronous and asynchronous execution

## 🔧 Prerequisites

- Python 3.7+ installed
- Basic understanding of Python programming
- OpenAI API key
- Knowledge of environment variables and `.env` files

## 📦 Required Dependencies

```bash
pip install openai-agents python-dotenv
```

## 🏗️ Project Structure

```
1runsync/
├── 1runsync.py    # Main script file
└── README.md      # This file
```

## 🔑 Environment Setup

Create a `.env` file in your project root with:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
```

## 📖 Code Explanation

### 1. Import Statements

```python
from agents import Agent, Runner
from dotenv import load_dotenv
from agents import set_default_openai_key
import os
import asyncio
```

**What each import does:**
- `Agent`: The main class for creating AI agents
- `Runner`: Utility class for running agents
- `load_dotenv`: Loads environment variables from `.env` file
- `set_default_openai_key`: Sets the default API key for the SDK
- `os`: For accessing environment variables
- `asyncio`: For running asynchronous functions

### 2. Environment Configuration

```python
# Load API key
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
openai_model = os.environ.get("OPENAI_MODEL")
```

**Step-by-step explanation:**
1. `load_dotenv()`: Reads the `.env` file and loads variables into the environment
2. `os.environ.get("OPENAI_API_KEY")`: Retrieves the API key from environment variables
3. `set_default_openai_key()`: Sets the API key for the SDK to use
4. `os.environ.get("OPENAI_MODEL")`: Gets the model name (e.g., "gpt-4")

### 3. Agent Creation

```python
# Create agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=openai_model
)
```

**Agent Configuration:**
- `name`: A friendly name for your agent
- `instructions`: The system prompt that defines the agent's behavior
- `model`: The OpenAI model to use (e.g., "gpt-4", "gpt-3.5-turbo")

### 4. Main Function

```python
# Async function using run()
async def main():
    result = await Runner.run(agent, "What is the capital of Pakistan?")
    print(result.final_output)
```

**What happens here:**
1. We define an `async` function (required for the SDK)
2. `Runner.run()` executes the agent with a specific message
3. We wait for the result using `await`
4. We print the final output from the agent

### 5. Execution

```python
# Run the async function
asyncio.run(main())
```

This line starts the execution of our async function.

## 🚀 How to Run

1. **Navigate to the directory:**
   ```bash
   cd 1runsync
   ```

2. **Set up your environment:**
   - Create a `.env` file with your OpenAI API key
   - Install dependencies: `pip install openai-agents python-dotenv`

3. **Run the script:**
   ```bash
   python 1runsync.py
   ```

## 📝 Expected Output

```
Islamabad is the capital of Pakistan.
```

## 🔍 Key Concepts Explained

### 🤖 What is an AI Agent?

An AI agent is a software program that can:
- Understand natural language input
- Process information using AI models
- Generate human-like responses
- Perform tasks based on instructions

### ⚡ Synchronous vs Asynchronous

- **Synchronous**: The program waits for each operation to complete before moving to the next
- **Asynchronous**: The program can handle multiple operations simultaneously

In this example, we use `async/await` because the OpenAI Agents SDK is built on asynchronous programming, even though we're running it in a synchronous manner.

### 🎯 The Runner.run() Method

`Runner.run()` is a utility method that:
- Takes an agent and a message as input
- Sends the message to the agent
- Waits for the agent to process and respond
- Returns the result object containing the response

## 🛠️ Customization Ideas

1. **Change the agent's personality:**
   ```python
   agent = Agent(
       name="Math Tutor",
       instructions="You are a patient math tutor who explains concepts step by step",
       model=openai_model
   )
   ```

2. **Ask different questions:**
   ```python
   result = await Runner.run(agent, "Explain quantum physics in simple terms")
   ```

3. **Use different models:**
   ```python
   # In your .env file
   OPENAI_MODEL=gpt-3.5-turbo
   ```

## ⚠️ Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'agents'"
**Solution:** Install the SDK: `pip install openai-agents`

### Issue: "OPENAI_API_KEY not found"
**Solution:** Check your `.env` file and ensure the API key is correct

### Issue: "Invalid API key"
**Solution:** Verify your OpenAI API key is valid and has sufficient credits

## 🔗 Related Topics

- [Asynchronous Agent Execution](../2runasync/)
- [Streaming Responses](../3runasyncstreaming/)
- [Agent Loops](../4agentloop/)
- [Configuration Management](../5runconfig/)

## 📚 Additional Resources

- [OpenAI Agents SDK Documentation](https://github.com/openai/openai-agents)
- [Python Async/Await Tutorial](https://realpython.com/async-io-python/)
- [Environment Variables in Python](https://realpython.com/python-dotenv/)

## 🎉 Next Steps

Once you understand this basic example, try:
1. Creating agents with different personalities
2. Handling more complex conversations
3. Adding tools and functions to your agent
4. Exploring asynchronous execution patterns

---

**Happy Coding! 🚀**

*This tutorial is part of the OpenAI Agents SDK learning series.* 