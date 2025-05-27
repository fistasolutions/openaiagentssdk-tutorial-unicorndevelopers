# Forcing Tools Example

This example demonstrates how to force agents to use specific tools for their responses, ensuring consistent and controlled behavior.

## Overview

The `12forcingtools.py` file shows how to:
1. Create function tools
2. Force tool usage
3. Control agent behavior
4. Implement required tool execution

## Key Components

1. **Function Tool**:
   ```python
   @function_tool
   def add_numbers(a: int, b: int) -> int:
       """Adds two numbers together."""
       return a + b
   ```

2. **Tool-Forcing Agent**:
   ```python
   agent = Agent(
       name="Math Agent",
       instructions="You are a math assistant. Use the tool to add numbers.",
       tools=[add_numbers],
       model_settings=ModelSettings(tool_choice="required"),  # Force tool use
       tool_use_behavior="stop_on_first_tool",  # Stop after first tool is used
   )
   ```

## Code Explanation

```python
# Create the agent with forced tool usage
agent = Agent(
    name="Math Agent",
    instructions="You are a math assistant. Use the tool to add numbers.",
    tools=[add_numbers],
    model_settings=ModelSettings(tool_choice="required"),
    tool_use_behavior="stop_on_first_tool",
)

# Run a query that triggers tool use
query = "What is 3 + 5?"
result = Runner.run_sync(agent, query)
```

## How to Run

1. Ensure your OpenAI API key is in the `.env` file
2. Run the script:
   ```bash
   uv run 12forcingtools.py
   ```

## Expected Output

The agent will:
1. Always use the add_numbers tool
2. Return the result of the tool execution
3. Not provide direct answers without using the tool

## Learning Points

- Creating function tools
- Forcing tool usage
- Controlling agent behavior
- Implementing required tool execution
- Tool-based responses

## Tool Forcing Benefits

1. **Consistency**:
   - Ensures tool usage
   - Predictable behavior
   - Controlled responses

2. **Reliability**:
   - Guaranteed tool execution
   - No direct answers
   - Structured responses

## Next Steps

After understanding this example, you can explore:
- Adding more complex tools
- Implementing tool chains
- Creating tool validation
- Adding tool error handling
- Implementing tool fallbacks 