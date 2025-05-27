# Auto Selecting Tool Example

This example demonstrates how to create an agent that can automatically select and use appropriate tools based on the input query.

## Overview

The `13autoselectingtool.py` file shows how to:
1. Create multiple function tools
2. Allow automatic tool selection
3. Implement tool-based responses
4. Handle dynamic tool usage

## Key Components

1. **Function Tools**:
   ```python
   @function_tool
   def add_numbers(a: int, b: int) -> int:
       """Adds two numbers together."""
       return a + b

   @function_tool
   def multiply_numbers(a: int, b: int) -> int:
       """Multiplies two numbers together."""
       return a * b
   ```

2. **Auto-Selecting Agent**:
   ```python
   agent = Agent(
       name="Math Agent",
       instructions="You are a math assistant. Use the appropriate tool based on the operation needed.",
       tools=[add_numbers, multiply_numbers],
       model_settings=ModelSettings(tool_choice="auto"),  # Allow automatic tool selection
   )
   ```

## Code Explanation

```python
# Create the agent with automatic tool selection
agent = Agent(
    name="Math Agent",
    instructions="You are a math assistant. Use the appropriate tool based on the operation needed.",
    tools=[add_numbers, multiply_numbers],
    model_settings=ModelSettings(tool_choice="auto"),
)

# Run queries that will trigger different tools
result1 = Runner.run_sync(agent, "What is 3 + 5?")  # Will use add_numbers
result2 = Runner.run_sync(agent, "What is 4 * 6?")  # Will use multiply_numbers
```

## How to Run

1. Ensure your OpenAI API key is in the `.env` file
2. Run the script:
   ```bash
   uv run 13autoselectingtool.py
   ```

## Expected Output

The agent will:
1. Automatically select the appropriate tool
2. Use addition tool for addition queries
3. Use multiplication tool for multiplication queries
4. Return the result of the selected tool

## Learning Points

- Creating multiple tools
- Implementing automatic tool selection
- Handling different operation types
- Dynamic tool usage
- Tool-based responses

## Auto Selection Benefits

1. **Flexibility**:
   - Automatic tool selection
   - Handles multiple operations
   - Adapts to query type

2. **Intelligence**:
   - Smart tool choice
   - Context-aware selection
   - Efficient operation handling

## Next Steps

After understanding this example, you can explore:
- Adding more complex tools
- Implementing tool selection logic
- Creating tool chains
- Adding tool validation
- Implementing tool fallbacks 