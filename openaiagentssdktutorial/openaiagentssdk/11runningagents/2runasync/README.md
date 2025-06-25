# ⚡ Running Agents Synchronously with `run_sync()`

## 📚 Overview

This tutorial demonstrates how to run AI agents synchronously using the `Runner.run_sync()` method. Unlike the previous example that used async/await, this approach provides a simpler, more straightforward way to execute agents without dealing with asynchronous programming.

## 🔍 Key Concepts Explained

### ⚡ Synchronous Execution

- **Synchronous**: The program waits for each operation to complete before moving to the next step
- **Blocking**: The execution pauses until the agent responds
- **Simple**: No need to handle async/await patterns

### 🎯 The `Runner.run_sync()` Method

`Runner.run_sync()` is a synchronous wrapper that:
- Takes an agent and a message as input
- Blocks execution until the agent responds
- Returns the result object containing the response
- Handles all async operations internally

### 🔄 Difference from `Runner.run()`

| Method | Complexity | Use Case |
|--------|------------|----------|
| `Runner.run()` | Requires async/await | When you need async control |
| `Runner.run_sync()` | Simple, blocking | When you want simplicity |

## 🎯 What You'll Learn

- How to use the `run_sync()` method for simple agent execution
- Understanding synchronous vs asynchronous execution
- When to choose `run_sync()` over `run()`
- Setting up agents with specific models

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
2runasync/
├── 2runasync.py    # Main script file
└── README.md       # This file
```

## 🔑 Environment Setup

Create a `.env` file in your project root with:

```env
OPENAI_API_KEY=your_openai_api_key_here
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
- `Runner`: Utility class for running agents (includes `run_sync`)
- `load_dotenv`: Loads environment variables from `.env` file
- `set_default_openai_key`: Sets the default API key for the SDK
- `os`: For accessing environment variables

### 2. Environment Configuration

```python
# Load API key
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
```

**Step-by-step explanation:**
1. `load_dotenv()`: Reads the `.env` file and loads variables
2. `os.environ.get("OPENAI_API_KEY")`: Retrieves the API key
3. `set_default_openai_key()`: Sets the API key for the SDK

### 3. Agent Creation

```python
# Create agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model="gpt-4o"
)
```

**Agent Configuration:**
- `name`: A friendly name for your agent
- `instructions`: The system prompt that defines behavior
- `model`: Directly specified as "gpt-4o" (no environment variable needed)

### 4. Synchronous Execution

```python
# Run synchronously
result = Runner.run_sync(agent, "What is the capital of Pakistan?")
print(result.final_output)
```

**What happens here:**
1. `Runner.run_sync()` executes the agent synchronously
2. The program waits for the response
3. We print the final output directly

## 🚀 How to Run

1. **Navigate to the directory:**
   ```bash
   cd 2runasync
   ```

2. **Set up your environment:**
   - Create a `.env` file with your OpenAI API key
   - Install dependencies: `pip install openai-agents python-dotenv`

3. **Run the script:**
   ```bash
   uv run 2runasync.py
   ```

## 📝 Expected Output

```
Islamabad is the capital of Pakistan.
```

## 🛠️ Customization Ideas

1. **Change the model:**
   ```python
   agent = Agent(
       name="Assistant",
       instructions="You are a helpful assistant",
       model="gpt-3.5-turbo"  # Different model
   )
   ```

2. **Ask different questions:**
   ```python
   result = Runner.run_sync(agent, "Explain machine learning in simple terms")
   ```

3. **Create specialized agents:**
   ```python
   agent = Agent(
       name="Code Helper",
       instructions="You are a programming expert who writes clean, efficient code",
       model="gpt-4o"
   )
   ```

## ⚡ When to Use `run_sync()`

### ✅ **Use `run_sync()` when:**
- You want simple, straightforward code
- You don't need to handle multiple operations simultaneously
- You're building simple scripts or tools
- You prefer blocking execution

### ❌ **Don't use `run_sync()` when:**
- You need to handle multiple agents at once
- You're building web applications
- You need non-blocking execution
- You want to process streaming responses

## ⚠️ Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'agents'"
**Solution:** Install the SDK: `pip install openai-agents`

### Issue: "OPENAI_API_KEY not found"
**Solution:** Check your `.env` file and ensure the API key is correct

### Issue: "Invalid API key"
**Solution:** Verify your OpenAI API key is valid and has sufficient credits

## 🔗 Related Topics

- [Synchronous Agent Execution](../1runsync/)
- [Streaming Responses](../3runasyncstreaming/)
- [Agent Loops](../4agentloop/)
- [Configuration Management](../5runconfig/)

## 📚 Additional Resources

- [OpenAI Agents SDK Documentation](https://github.com/openai/openai-agents)
- [Python Synchronous vs Asynchronous](https://realpython.com/async-io-python/)
- [Environment Variables in Python](https://realpython.com/python-dotenv/)

## 🎉 Next Steps

Once you understand this example, try:
1. Comparing performance between `run()` and `run_sync()`
2. Building simple command-line tools
3. Creating agents with different personalities
4. Exploring more complex agent configurations

---

**Happy Coding! 🚀**

*This tutorial is part of the OpenAI Agents SDK learning series.* 