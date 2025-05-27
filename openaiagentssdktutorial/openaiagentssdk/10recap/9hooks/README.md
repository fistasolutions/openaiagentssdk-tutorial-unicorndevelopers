# Hooks Example

This example demonstrates how to use hooks with AI agents to add custom behavior at different stages of agent execution.

## Overview

The `9hooks.py` file shows how to:
1. Create custom hooks
2. Monitor agent execution
3. Add logging functionality
4. Handle agent lifecycle events

## Key Components

1. **Custom Hooks Class**:
   ```python
   class LoggingHooks(AgentHooks):
       def on_run_start(self, context, agent, input):
           print(f"[HOOK] Agent '{agent.name}' started a run with input: '{input}'")

       def on_run_end(self, context, agent, input, final_output):
           print(f"[HOOK] Agent '{agent.name}' completed the run. Output: '{final_output}'")

       def on_error(self, context, agent, input, error):
           print(f"[HOOK] Agent '{agent.name}' encountered an error: {error}")
   ```

2. **Hooked Agent**:
   - Attaches hooks to agent
   - Monitors execution
   - Provides logging

## Code Explanation

```python
# Create a simple agent and attach hooks
agent = Agent(
    name="Greeting Agent",
    instructions="Respond to greetings politely and kindly.",
    hooks=LoggingHooks(),
    model=openai_model
)

# Run the agent
query = "Hi there!"
result = Runner.run_sync(agent, query)
```

## How to Run

1. Ensure your OpenAI API key is in the `.env` file
2. Run the script:
   ```bash
   uv run 9hooks.py
   ```

## Expected Output

You'll see logging output at different stages:
```
[HOOK] Agent 'Greeting Agent' started a run with input: 'Hi there!'
[HOOK] Agent 'Greeting Agent' completed the run. Output: 'Hello! How can I help you today?'
```

## Learning Points

- Creating custom hooks
- Monitoring agent execution
- Implementing logging
- Handling agent lifecycle
- Error tracking

## Hook Types

1. **on_run_start**:
   - Triggered when agent starts
   - Access to input and context
   - Good for validation

2. **on_run_end**:
   - Triggered when agent completes
   - Access to final output
   - Good for logging results

3. **on_error**:
   - Triggered on errors
   - Access to error details
   - Good for error handling

## Next Steps

After understanding this example, you can explore:
- Adding more hook types
- Implementing complex logging
- Creating performance monitoring
- Adding validation hooks
- Implementing error recovery 