"""
Title: Automatic Argument and Docstring Parsing with OpenAI Agents SDK

Description:
This example demonstrates how to use the OpenAI Agents SDK to automatically parse Python
function signatures and docstrings to generate tool schemas and documentation for an AI agent.
This helps the AI know what tools are available, what inputs they require, and how to use them.

Pre-Requisites:
- Basic knowledge of Python (functions, typing, async)
- Installed OpenAI Agents SDK (`pip install openai-agents`)
- `.env` file with:
    OPENAI_API_KEY=your-openai-key
    OPENAI_MODEL=gpt-4o or gpt-3.5-turbo
"""

import os
import json
from dotenv import load_dotenv
from typing_extensions import TypedDict, Any

from agents import Agent, Runner, FunctionTool, function_tool, set_default_openai_key


# Step 1: Load environment variables (API Key and Model Name)
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_model = os.environ.get("OPENAI_MODEL")
set_default_openai_key(openai_api_key)


# Step 2: Define input structure using TypedDict (for structured inputs)
class Location(TypedDict):
    lat: float
    long: float


# Step 3: Define a tool function with docstring and type hints
@function_tool
async def fetch_weather(location: Location) -> str:
    """
    Fetch the weather for a given location.

    Args:
        location: The location to fetch the weather for, including latitude and longitude.

    Returns:
        A string describing the weather.
    """
    # In a real app, this would call a weather API.
    return f"The weather at lat {location['lat']}, long {location['long']} is sunny."


# Step 4: Register the tool in an Agent
agent = Agent(
    name="WeatherBot",
    instructions="You are a helpful weather assistant. Use the tool to check current weather.",
    model=openai_model,
    tools=[fetch_weather]
)


# Step 5: Run the agent with a sample query
if __name__ == "__main__":
    result = Runner.run_sync(
        agent,
        input="What's the weather like at latitude 37.7749 and longitude -122.4194?"
    )
    print("=== Final Output ===")
    print(result.final_output)

    # Step 6: (Optional) Print tool metadata extracted from function
    print("\n=== Tool Metadata ===")
    for tool in agent.tools:
        if isinstance(tool, FunctionTool):
            print("Tool Name:", tool.name)
            print("Description:", tool.description)
            print("JSON Schema:")
            print(json.dumps(tool.params_json_schema, indent=2))
