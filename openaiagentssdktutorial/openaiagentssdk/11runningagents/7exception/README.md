# 🛡️ Exception Handling with OpenAI Agents SDK

## 📚 Overview

This tutorial demonstrates how to handle exceptions and errors when working with the OpenAI Agents SDK. You'll learn about different types of exceptions that can occur, how to catch and handle them appropriately, and best practices for robust error management in AI applications.

## 🔍 Key Concepts Explained

### 🛡️ What is Exception Handling?

- **Error Prevention**: Gracefully handle unexpected situations
- **User Experience**: Provide meaningful error messages
- **Debugging**: Identify and resolve issues quickly
- **Reliability**: Make applications more robust and stable

### 🎯 Types of Exceptions in Agents SDK

The SDK provides several specific exception types:
- **MaxTurnsExceeded**: Conversation exceeded allowed turns
- **ModelBehaviorError**: Model gave invalid or unexpected response
- **UserError**: Incorrect usage of the SDK
- **InputGuardrailTripwireTriggered**: Input failed safety/validation
- **OutputGuardrailTripwireTriggered**: Output failed validation
- **AgentsException**: General SDK exceptions

### 🔄 Exception Hierarchy

```
Exception (Python built-in)
├── AgentsException (SDK base)
│   ├── MaxTurnsExceeded
│   ├── ModelBehaviorError
│   ├── UserError
│   ├── InputGuardrailTripwireTriggered
│   └── OutputGuardrailTripwireTriggered
└── Other exceptions
```

## 🎯 What You'll Learn

- How to import and use specific exception types
- Implementing comprehensive error handling
- Understanding different error scenarios
- Best practices for exception management
- Debugging and troubleshooting techniques

## 🔧 Prerequisites

- Python 3.7+ installed
- Basic understanding of Python programming
- Knowledge of try/except blocks
- OpenAI API key
- Understanding of environment variables

## 📦 Required Dependencies

```bash
pip install openai-agents python-dotenv
```

## 🏗️ Project Structure

```
7exception/
├── 7exception.py    # Main script file
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
from agents.exceptions import (
    AgentsException,
    MaxTurnsExceeded,
    ModelBehaviorError,
    UserError,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered
)
from dotenv import load_dotenv
import os
```

**What each import does:**
- `Agent`: The main class for creating AI agents
- `Runner`: Utility class for running agents
- `set_default_openai_key`: Sets the default API key for the SDK
- **Exception Classes**: Specific exception types for different error scenarios
- `load_dotenv`: Loads environment variables from `.env` file
- `os`: For accessing environment variables

### 2. Environment Configuration

```python
# Load and set API key
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
```

**Step-by-step explanation:**
1. `load_dotenv()`: Reads the `.env` file and loads variables
2. `set_default_openai_key()`: Sets the API key for the SDK

### 3. Agent Creation

```python
# Define an agent
agent = Agent(
    name="FaultyAgent",
    instructions="Produce invalid output to test error handling.",
    model="gpt-4o"
)
```

**Agent Configuration:**
- `name`: "FaultyAgent" - indicates this agent is designed for testing errors
- `instructions`: Specifically asks for invalid output to trigger errors
- `model`: Using "gpt-4o" for testing

### 4. Exception Handling Structure

```python
try:
    # Try a normal run (this will work fine unless the model misbehaves)
    result = Runner.run_sync(agent, "Tell me a story about a cat who codes.")
    print("Final Output:", result.final_output)

except MaxTurnsExceeded:
    print("❌ Error: The conversation exceeded the allowed number of turns.")

except ModelBehaviorError:
    print("❌ Error: The model gave a bad response (e.g. invalid JSON).")

except InputGuardrailTripwireTriggered:
    print("🚨 Guardrail Triggered: The input didn't meet safety/validation rules.")

except OutputGuardrailTripwireTriggered:
    print("🚨 Guardrail Triggered: The output failed validation or policy checks.")

except UserError:
    print("❌ UserError: You likely made a mistake in how you used the SDK.")

except AgentsException as e:
    print(f"⚠️ General SDK Exception: {e}")

except Exception as e:
    print(f"🔥 Unexpected Error: {e}")
```

**Exception Handling Breakdown:**
1. **Specific Exceptions First**: Catch specific SDK exceptions before general ones
2. **MaxTurnsExceeded**: Handles conversations that go too long
3. **ModelBehaviorError**: Handles invalid model responses
4. **Guardrail Exceptions**: Handles safety and validation failures
5. **UserError**: Handles SDK usage mistakes
6. **AgentsException**: Catches any other SDK-specific exceptions
7. **Exception**: Catches any unexpected errors

## 🚀 How to Run

1. **Navigate to the directory:**
   ```bash
   cd 7exception
   ```

2. **Set up your environment:**
   - Create a `.env` file with your OpenAI API key
   - Install dependencies: `pip install openai-agents python-dotenv`

3. **Run the script:**
   ```bash
   uv run 7exception.py
   ```

## 📝 Expected Output

```
Final Output: [Story about a coding cat]
```

*Note: The actual output will depend on the model's response. The exception handling is in place to catch any errors that might occur.*

## 🛠️ Customization Ideas

1. **Add logging to exceptions:**
   ```python
   import logging
   
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)
   
   try:
       result = Runner.run_sync(agent, "Tell me a story.")
       print("Final Output:", result.final_output)
   except MaxTurnsExceeded as e:
       logger.error(f"MaxTurnsExceeded: {e}")
       print("❌ Error: The conversation exceeded the allowed number of turns.")
   ```

2. **Retry mechanism:**
   ```python
   import time
   
   def run_with_retry(agent, message, max_retries=3):
       for attempt in range(max_retries):
           try:
               result = Runner.run_sync(agent, message)
               return result
           except ModelBehaviorError as e:
               if attempt == max_retries - 1:
                   raise e
               print(f"Attempt {attempt + 1} failed, retrying...")
               time.sleep(1)
   ```

3. **Custom exception handling:**
   ```python
   class AgentErrorHandler:
       def __init__(self, agent):
           self.agent = agent
       
       def safe_run(self, message):
           try:
               return Runner.run_sync(self.agent, message)
           except MaxTurnsExceeded:
               return "I apologize, but this conversation has become too long. Please start a new conversation."
           except ModelBehaviorError:
               return "I encountered an issue processing your request. Please try again."
           except Exception as e:
               return f"An unexpected error occurred: {str(e)}"
   ```

## 🛡️ Exception Types Explained

### MaxTurnsExceeded
**When it occurs:** Conversation exceeds the maximum allowed turns
**Common causes:** Infinite loops, very long conversations
**Solution:** Implement turn limits or conversation resets

### ModelBehaviorError
**When it occurs:** Model returns invalid or unexpected responses
**Common causes:** Model hallucinations, invalid JSON, malformed responses
**Solution:** Retry the request, validate responses, use different models

### UserError
**When it occurs:** Incorrect usage of the SDK
**Common causes:** Wrong parameters, invalid configurations
**Solution:** Check SDK documentation, validate inputs

### Guardrail Exceptions
**When they occur:** Input or output fails safety/validation checks
**Common causes:** Inappropriate content, policy violations
**Solution:** Review content, adjust guardrail settings

## 🛡️ Best Practices for Exception Handling

### 1. Specific Before General
```python
try:
    result = Runner.run_sync(agent, message)
except MaxTurnsExceeded:
    # Handle specific case
except AgentsException:
    # Handle general SDK errors
except Exception:
    # Handle everything else
```

### 2. Meaningful Error Messages
```python
except MaxTurnsExceeded:
    print("❌ Conversation too long. Please start a new chat.")
    # Provide actionable guidance
```

### 3. Logging and Monitoring
```python
import logging

logger = logging.getLogger(__name__)

try:
    result = Runner.run_sync(agent, message)
except Exception as e:
    logger.error(f"Agent execution failed: {e}", exc_info=True)
    # Log for debugging and monitoring
```

### 4. Graceful Degradation
```python
def get_agent_response(agent, message):
    try:
        result = Runner.run_sync(agent, message)
        return result.final_output
    except Exception as e:
        return f"I'm sorry, I encountered an error: {str(e)}"
```

## 🛡️ When to Use Exception Handling

### ✅ **Use exception handling when:**
- Building production applications
- Creating user-facing AI services
- Need robust error recovery
- Want to provide better user experience
- Debugging and monitoring applications

### ❌ **Don't use exception handling when:**
- Simple scripts or experiments
- You want to see raw errors
- Performance is critical (minimal overhead)

## ⚠️ Common Issues & Solutions

### Issue: "Exception not being caught"
**Solution:** Ensure you're catching the specific exception type

### Issue: "Too many exception types"
**Solution:** Use `AgentsException` to catch all SDK exceptions

### Issue: "Silent failures"
**Solution:** Always log or handle exceptions appropriately

### Issue: "ModuleNotFoundError: No module named 'agents'"
**Solution:** Install the SDK: `pip install openai-agents`

## 🔗 Related Topics

- [Synchronous Agent Execution](../1runsync/)
- [Asynchronous Agent Execution](../2runasync/)
- [Streaming Responses](../3runasyncstreaming/)
- [Agent Loops](../4agentloop/)
- [Configuration Management](../5runconfig/)
- [Conversation Management](../6conversation/)

## 📚 Additional Resources

- [OpenAI Agents SDK Documentation](https://github.com/openai/openai-agents)
- [Python Exception Handling](https://docs.python.org/3/tutorial/errors.html)
- [Logging in Python](https://docs.python.org/3/howto/logging.html)

## 🎉 Next Steps

Once you understand exception handling, try:
1. Building robust production applications
2. Implementing comprehensive error monitoring
3. Creating user-friendly error messages
4. Adding retry mechanisms and fallbacks

---

**Happy Coding! 🚀**

*This tutorial is part of the OpenAI Agents SDK learning series.* 