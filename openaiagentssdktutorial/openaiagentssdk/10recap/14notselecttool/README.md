# Not Select Tool Example

This example demonstrates how to create an agent that has access to tools but is instructed not to use them, showing how to control tool usage behavior.

## Overview

The `14notselecttool.py` file shows how to:
1. Create function tools
2. Configure agents to not use tools
3. Implement direct responses
4. Control tool usage behavior

## Key Components

1. **Function Tool**:
   ```python
   @function_tool
   def add_numbers(a: int, b: int) -> int:
       """Adds two numbers together."""
       return a + b
   ```

2. **No-Tool Agent**:
   ```python
   agent = Agent(
       name="No Tool Agent",
       instructions="You are a math assistant. You must answer without using tools.",
       tools=[add_numbers],  # tools are passed, but won't be used
       model_settings=ModelSettings(tool_choice="none"),
   )
   ```

## Code Explanation

```python
# Create the agent that won't use tools
agent = Agent(
    name="No Tool Agent",
    instructions="You are a math assistant. You must answer without using tools.",
    tools=[add_numbers],
    model_settings=ModelSettings(tool_choice="none"),
)

# Run a query that would normally use a tool
result = Runner.run_sync(agent, "What is 3 + 5?")
```

## How to Run

1. Ensure your OpenAI API key is in the `.env` file
2. Run the script:
   ```bash
   uv run 14notselecttool.py
   ```

## Expected Output

The agent will:
1. Not use any tools
2. Provide direct answers
3. Ignore available tools
4. Respond naturally to queries

## Learning Points

- Creating function tools
- Controlling tool usage
- Implementing direct responses
- Tool behavior configuration
- Agent instruction control

## No-Tool Benefits

1. **Simplicity**:
   - Direct responses
   - No tool overhead
   - Natural language answers

2. **Control**:
   - Explicit tool usage control
   - Predictable behavior
   - Clear response patterns

## Next Steps

After understanding this example, you can explore:
- Implementing conditional tool usage
- Creating tool usage rules
- Adding tool usage validation
- Implementing tool usage logging
- Creating tool usage policies 