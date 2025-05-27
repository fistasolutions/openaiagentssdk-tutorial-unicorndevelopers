# Hello Agents Example

This is a basic example that demonstrates how to create and use a simple AI agent using the OpenAI Agents framework.

## Overview

The `1helloagents.py` file shows the most basic implementation of an AI agent. It's perfect for beginners who want to understand the fundamental concepts of the framework.

## Key Components

1. **Agent Creation**: 
   - Creates a simple agent named "Assistant"
   - Uses GPT-4 model
   - Has basic instructions to be helpful

2. **Basic Setup**:
   - Loads environment variables
   - Sets up OpenAI API key
   - Demonstrates basic agent configuration

## Code Explanation

```python
# Create a basic agent
agent = Agent(
    name="Assistant", 
    instructions="You are a helpful assistant", 
    model="gpt-4o"
)

# Run the agent with a simple query
result = Runner.run_sync(agent, "What is the capital of Pakistan?")
```

## How to Run

1. Make sure you have your OpenAI API key in the `.env` file
2. Run the script:
   ```bash
   uv run 1helloagents.py
   ```

## Expected Output

The agent will respond to the question about Pakistan's capital with a natural language response.

## Learning Points

- Basic agent creation
- Environment setup
- Simple agent interaction
- Synchronous agent execution

## Next Steps

After understanding this example, you can move on to:
- Adding tools to your agent
- Using different models
- Implementing more complex instructions
- Adding context to your agents 