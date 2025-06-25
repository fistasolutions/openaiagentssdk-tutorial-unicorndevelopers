# ⚙️ Run Configuration with OpenAI Agents SDK

## 📚 Overview

This tutorial demonstrates how to use run configuration with the OpenAI Agents SDK. Run configuration allows you to override agent settings for specific executions, control model parameters like temperature, and add metadata for better traceability and debugging.

## 🔍 Key Concepts Explained

### ⚙️ What is Run Configuration?

- **Runtime Overrides**: Change agent settings for specific runs
- **Model Control**: Adjust temperature, model selection, and other parameters
- **Traceability**: Add metadata for debugging and monitoring
- **Flexibility**: Use different configurations for different use cases

### 🎯 RunConfig Components

A `RunConfig` object can include:
- **Model Override**: Use a different model than the agent's default
- **Model Settings**: Control temperature, max tokens, etc.
- **Workflow Name**: For organizing traces and logs
- **Trace Metadata**: Additional context for debugging

### 🔄 Agent vs Run Configuration

| Setting | Agent Level | Run Level | Priority |
|---------|-------------|-----------|----------|
| **Model** | Default model | Override model | Run wins |
| **Temperature** | Not set | Configurable | Run only |
| **Instructions** | Always set | Cannot override | Agent only |
| **Metadata** | Not available | Configurable | Run only |

## 🎯 What You'll Learn

- How to create and use `RunConfig` objects
- Overriding agent settings at runtime
- Controlling model parameters like temperature
- Adding metadata for traceability
- Understanding configuration precedence

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
5runconfig/
├── 5runconfig.py    # Main script file
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
from agents import Agent, Runner, set_default_openai_key, ModelSettings, RunConfig
from dotenv import load_dotenv
import os
```

**What each import does:**
- `Agent`: The main class for creating AI agents
- `Runner`: Utility class for running agents
- `set_default_openai_key`: Sets the default API key for the SDK
- `ModelSettings`: Class for configuring model parameters
- `RunConfig`: Class for runtime configuration
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

### 3. Agent Creation

```python
agent = Agent(
    name="Poet Agent",
    instructions="You are a poetic assistant.",
    model="gpt-3.5-turbo"  # This will be overridden by run_config if set
)
```

**Agent Configuration:**
- `name`: "Poet Agent" - specialized for poetry
- `instructions`: Clear role definition for poetry assistance
- `model`: Set to "gpt-3.5-turbo" but will be overridden

### 4. Run Configuration

```python
run_config = RunConfig(
    model="gpt-4o",  # Overrides agent's default if needed
    model_settings=ModelSettings(temperature=0.8),  # More creative responses
    workflow_name="creative_poem_run",  # Good for trace organization
    trace_metadata={"project": "poetry", "env": "dev"}
)
```

**RunConfig Breakdown:**
- `model="gpt-4o"`: Overrides the agent's default model
- `model_settings=ModelSettings(temperature=0.8)`: Sets higher creativity
- `workflow_name="creative_poem_run"`: Organizes traces and logs
- `trace_metadata`: Adds context for debugging and monitoring

### 5. Model Settings

```python
model_settings=ModelSettings(temperature=0.8)
```

**Temperature Explanation:**
- **0.0**: Very deterministic, consistent responses
- **0.8**: More creative, varied responses
- **1.0**: Maximum creativity, unpredictable

### 6. Execution with Configuration

```python
result = Runner.run_sync(agent, "Write a haiku about spring.", run_config=run_config)
print(result.final_output)
```

**What happens here:**
1. `Runner.run_sync()` executes with the run configuration
2. The agent uses "gpt-4o" instead of "gpt-3.5-turbo"
3. Temperature is set to 0.8 for more creative poetry
4. Metadata is attached for traceability

## 🚀 How to Run

1. **Navigate to the directory:**
   ```bash
   cd 5runconfig
   ```

2. **Set up your environment:**
   - Create a `.env` file with your OpenAI API key
   - Install dependencies: `pip install openai-agents python-dotenv`

3. **Run the script:**
   ```bash
   uv run 5runconfig.py
   ```

## 📝 Expected Output

```
Cherry blossoms fall
Softly on the morning dew
Spring awakens now
```

## 🛠️ Customization Ideas

1. **Different temperature settings:**
   ```python
   # Very creative
   run_config = RunConfig(
       model="gpt-4o",
       model_settings=ModelSettings(temperature=1.0)
   )
   
   # Very deterministic
   run_config = RunConfig(
       model="gpt-4o",
       model_settings=ModelSettings(temperature=0.1)
   )
   ```

2. **Multiple run configurations:**
   ```python
   # Creative writing config
   creative_config = RunConfig(
       model="gpt-4o",
       model_settings=ModelSettings(temperature=0.9),
       workflow_name="creative_writing"
   )
   
   # Factual config
   factual_config = RunConfig(
       model="gpt-4o",
       model_settings=ModelSettings(temperature=0.1),
       workflow_name="factual_qa"
   )
   ```

3. **Environment-specific configurations:**
   ```python
   # Development config
   dev_config = RunConfig(
       model="gpt-3.5-turbo",  # Cheaper for testing
       model_settings=ModelSettings(temperature=0.7),
       trace_metadata={"env": "dev", "purpose": "testing"}
   )
   
   # Production config
   prod_config = RunConfig(
       model="gpt-4o",  # Best quality
       model_settings=ModelSettings(temperature=0.5),
       trace_metadata={"env": "prod", "purpose": "user_facing"}
   )
   ```

## ⚙️ ModelSettings Options

### Temperature
```python
ModelSettings(temperature=0.8)  # 0.0 to 1.0
```

### Max Tokens
```python
ModelSettings(max_tokens=1000)  # Limit response length
```

### Top P
```python
ModelSettings(top_p=0.9)  # Nucleus sampling
```

### Frequency Penalty
```python
ModelSettings(frequency_penalty=0.1)  # Reduce repetition
```

### Presence Penalty
```python
ModelSettings(presence_penalty=0.1)  # Encourage new topics
```

## 🔍 Trace Metadata Use Cases

### Debugging
```python
trace_metadata={
    "debug": True,
    "user_id": "12345",
    "session_id": "abc123"
}
```

### Analytics
```python
trace_metadata={
    "feature": "poetry_generator",
    "user_tier": "premium",
    "request_type": "creative"
}
```

### Monitoring
```python
trace_metadata={
    "service": "poetry_api",
    "version": "1.0.0",
    "region": "us-east-1"
}
```

## ⚙️ When to Use Run Configuration

### ✅ **Use run configuration when:**
- Need different models for different tasks
- Want to adjust creativity levels
- Building multi-tenant applications
- Need detailed traceability
- A/B testing different parameters

### ❌ **Don't use run configuration when:**
- Simple, consistent agent usage
- Single model and settings work for all cases
- Performance is critical (minimal overhead)

## ⚠️ Common Issues & Solutions

### Issue: "Model override not working"
**Solution:** Ensure `run_config` is passed to the `run_sync()` method

### Issue: "Temperature not affecting output"
**Solution:** Check that `ModelSettings` is properly configured

### Issue: "Metadata not appearing in traces"
**Solution:** Verify the `trace_metadata` format and SDK version

### Issue: "ModuleNotFoundError: No module named 'agents'"
**Solution:** Install the SDK: `pip install openai-agents`

## 🔗 Related Topics

- [Synchronous Agent Execution](../1runsync/)
- [Asynchronous Agent Execution](../2runasync/)
- [Streaming Responses](../3runasyncstreaming/)
- [Agent Loops](../4agentloop/)
- [Conversation Management](../6conversation/)

## 📚 Additional Resources

- [OpenAI Agents SDK Documentation](https://github.com/openai/openai-agents)
- [OpenAI Model Parameters](https://platform.openai.com/docs/api-reference/chat/create)
- [Temperature and Sampling](https://platform.openai.com/docs/guides/gpt/parameter-details)

## 🎉 Next Steps

Once you understand run configuration, try:
1. Building A/B testing frameworks
2. Creating environment-specific configurations
3. Implementing dynamic parameter adjustment
4. Adding comprehensive traceability

---

**Happy Coding! 🚀**

*This tutorial is part of the OpenAI Agents SDK learning series.* 