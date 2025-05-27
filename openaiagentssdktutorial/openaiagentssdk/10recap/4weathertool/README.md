# Weather Tool Example

This example demonstrates how to create and use function tools with AI agents, specifically focusing on weather-related functionality.

## Overview

The `4weathertool.py` file shows how to:
1. Create custom function tools
2. Attach tools to agents
3. Use multiple agents with different tools
4. Handle tool-based interactions

## Key Components

1. **Function Tools**:
   - `get_weather`: A tool to get weather information
   - `sales_guide`: A tool to get product sales guides

2. **Multiple Agents**:
   - Weather Agent: Specialized in weather queries
   - Sales Guide Agent: Specialized in product information

## Code Explanation

```python
@function_tool
def get_weather(location: str) -> str:
    """Get the weather of a location."""
    return f"The weather of {location} is sunny."

@function_tool
def sales_guide(product: str) -> str:
    """Get the sales guide of a product."""
    return f"The sales guide of {product} is a guide to sell the product."

# Create specialized agents
weather_agent = Agent(
    name="Weather Agent",
    instructions="You are a weather agent. You are given a location and you need to return the weather of the location.",
    tools=[get_weather]
)

sales_guide_agent = Agent(
    name="Sales Guide Agent",
    instructions="You are a sales guide agent. You are given a product and you need to return the sales guide of the product.",
    tools=[sales_guide]
)
```

## How to Run

1. Ensure your OpenAI API key is in the `.env` file
2. Run the script:
   ```bash
   uv run 4weathertool.py
   ```
3. Enter your query when prompted

## Expected Output

The agents will respond using their respective tools:
- Weather Agent: Provides weather information for locations
- Sales Guide Agent: Provides product sales guides

## Learning Points

- Creating function tools
- Using the `@function_tool` decorator
- Attaching tools to agents
- Handling multiple agents
- Tool-based interactions

## Tool Structure

Each tool follows this pattern:
1. Function definition with type hints
2. Docstring for tool description
3. Tool implementation
4. Agent configuration with tools

## Next Steps

After understanding this example, you can explore:
- Creating more complex tools
- Adding error handling to tools
- Implementing tool chains
- Creating tool-specific agents
- Adding tool validation 