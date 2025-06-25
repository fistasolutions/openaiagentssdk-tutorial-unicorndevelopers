# 📊 Understanding RunResult Properties with OpenAI Agents SDK

## 📚 Overview

This tutorial demonstrates how to access and utilize the various properties available in the `RunResult` object returned by the OpenAI Agents SDK. You'll learn how to extract different types of information from agent executions, including final outputs, agent details, input data, and metadata.

## 🔍 Key Concepts Explained

### 📊 What is RunResult?

- **Execution Summary**: Contains all information about an agent run
- **Rich Metadata**: Provides access to inputs, outputs, and execution details
- **Inheritance**: Inherits from `RunResultBase` for consistent structure
- **Comprehensive Data**: Includes everything needed to understand the execution

### 🎯 RunResult Properties

The `RunResult` object provides access to:
- **final_output**: The main response from the agent
- **last_agent**: The agent that performed the execution
- **input**: The original input provided to the agent
- **new_items**: Items generated during execution
- **raw_responses**: Raw response data from the model
- **guardrail_results**: Safety and validation results

### 🔄 Result Object Structure

```
RunResult (inherits from RunResultBase)
├── final_output: str
├── last_agent: Agent
├── input: Any
├── new_items: List[Item]
├── raw_responses: List[Any]
├── input_guardrail_results: List[Any]
└── output_guardrail_results: List[Any]
```

## 🎯 What You'll Learn

- How to access different properties of RunResult
- Understanding the structure of execution results
- Working with new items and raw responses
- Utilizing guardrail results for safety
- Building applications that leverage result metadata

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
1results/
├── 1results.py    # Main script file
└── README.md      # This file
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
# Load environment and API key
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
# Define your agent
agent = Agent(
    name="SummaryAgent",
    instructions="Summarize the user's message in 1 sentence.",
    model=model
)
```

**Agent Configuration:**
- `name`: "SummaryAgent" - specialized for summarization
- `instructions`: Clear directive to summarize in one sentence
- `model`: Uses the model specified in environment variables

### 4. Agent Execution

```python
# Run the agent using run_sync (returns RunResult)
result = Runner.run_sync(agent, "Explain the basics of quantum computing.")
```

**What happens here:**
1. `Runner.run_sync()` executes the agent with the input
2. Returns a `RunResult` object containing all execution data
3. The result object is stored for further analysis

### 5. Accessing RunResult Properties

#### Final Output
```python
print("\n📌 Final Output:")
print(result.final_output)
```
**Purpose:** Gets the main response from the agent

#### Last Agent Used
```python
print("\n👤 Last Agent Used:")
print(result.last_agent.name)
```
**Purpose:** Identifies which agent performed the execution

#### Original Input
```python
print("\n🧾 Original Input:")
print(result.input)
```
**Purpose:** Shows the original input provided to the agent

#### New Items Generated
```python
print("\n🆕 New Items Generated:")
for item in result.new_items:
    print(f"- {item.type}")
```
**Purpose:** Lists all items generated during execution

#### Raw Responses
```python
print("\n📤 Raw Responses:")
for response in result.raw_responses:
    print(response)
```
**Purpose:** Shows raw response data from the model

#### Guardrail Results
```python
print("\n🛡️ Input Guardrail Results:", result.input_guardrail_results)
print("🛡️ Output Guardrail Results:", result.output_guardrail_results)
```
**Purpose:** Shows safety and validation results

## 🚀 How to Run

1. **Navigate to the directory:**
   ```bash
   cd 1results
   ```

2. **Set up your environment:**
   - Create a `.env` file with your OpenAI API key and model
   - Install dependencies: `pip install openai-agents python-dotenv`

3. **Run the script:**
   ```bash
   uv run 1results.py
   ```

## 📝 Expected Output

```
📌 Final Output:
Quantum computing uses quantum mechanics principles to process information using qubits that can exist in multiple states simultaneously.

👤 Last Agent Used:
SummaryAgent

🧾 Original Input:
Explain the basics of quantum computing.

🆕 New Items Generated:
- message_output_item

📤 Raw Responses:
[Raw response data from the model]

🛡️ Input Guardrail Results: []
🛡️ Output Guardrail Results: []
```

## 🛠️ Customization Ideas

1. **Create a result analyzer:**
   ```python
   def analyze_result(result):
       print(f"Agent: {result.last_agent.name}")
       print(f"Input length: {len(str(result.input))}")
       print(f"Output length: {len(result.final_output)}")
       print(f"Items generated: {len(result.new_items)}")
       print(f"Raw responses: {len(result.raw_responses)}")
   ```

2. **Extract specific information:**
   ```python
   def extract_agent_info(result):
       agent = result.last_agent
       return {
           "name": agent.name,
           "instructions": agent.instructions,
           "model": agent.model
       }
   ```

3. **Build a result logger:**
   ```python
   import json
   from datetime import datetime
   
   def log_result(result, filename="agent_results.json"):
       log_entry = {
           "timestamp": datetime.now().isoformat(),
           "agent_name": result.last_agent.name,
           "input": result.input,
           "output": result.final_output,
           "items_count": len(result.new_items)
       }
       
       with open(filename, "a") as f:
           f.write(json.dumps(log_entry) + "\n")
   ```

## 📊 RunResult Properties Deep Dive

### final_output
- **Type:** `str`
- **Purpose:** The main response from the agent
- **Use case:** Display to users, process for further actions

### last_agent
- **Type:** `Agent`
- **Purpose:** Reference to the agent that performed the execution
- **Use case:** Continue conversations, access agent properties

### input
- **Type:** `Any`
- **Purpose:** The original input provided to the agent
- **Use case:** Debugging, logging, context preservation

### new_items
- **Type:** `List[Item]`
- **Purpose:** Items generated during execution (messages, reasoning, etc.)
- **Use case:** Extract structured data, analyze agent behavior

### raw_responses
- **Type:** `List[Any]`
- **Purpose:** Raw response data from the underlying model
- **Use case:** Debugging, custom processing, analytics

### guardrail_results
- **Type:** `List[Any]`
- **Purpose:** Results from input/output safety checks
- **Use case:** Safety monitoring, compliance, debugging

## 📊 When to Use RunResult Properties

### ✅ **Use RunResult properties when:**
- Building applications that need detailed execution info
- Debugging agent behavior
- Logging and analytics
- Building multi-agent systems
- Implementing safety monitoring

### ❌ **Don't use RunResult properties when:**
- Simple one-off agent calls
- Performance is critical (minimal overhead)
- You only need the final output

## ⚠️ Common Issues & Solutions

### Issue: "Property not found"
**Solution:** Check the SDK version and property name spelling

### Issue: "Empty new_items list"
**Solution:** This is normal for simple agent executions

### Issue: "Raw responses are complex"
**Solution:** Use specific properties or iterate through the list

### Issue: "ModuleNotFoundError: No module named 'agents'"
**Solution:** Install the SDK: `pip install openai-agents`

## 🔗 Related Topics

- [Input and Next Steps](../2inputnext/)
- [Final Agent Management](../3finalagent/)
- [New Items Processing](../4newitem/)
- [Synchronous Agent Execution](../../11runningagents/1runsync/)
- [Asynchronous Agent Execution](../../11runningagents/2runasync/)

## 📚 Additional Resources

- [OpenAI Agents SDK Documentation](https://github.com/openai/openai-agents)
- [Python Object Properties](https://docs.python.org/3/tutorial/classes.html)
- [Data Analysis with Python](https://pandas.pydata.org/docs/)

## 🎉 Next Steps

Once you understand RunResult properties, try:
1. Building result analysis tools
2. Creating comprehensive logging systems
3. Implementing multi-agent workflows
4. Adding result validation and monitoring

---

**Happy Coding! 🚀**

*This tutorial is part of the OpenAI Agents SDK learning series.* 