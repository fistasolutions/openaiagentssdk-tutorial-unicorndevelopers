"""
Title: Custom Output Extraction from Tool-Agent in OpenAI Agents SDK

Description:
This example shows how to use a custom_output_extractor to extract a specific part of the sub-agent's output.
The sub-agent returns a JSON response, and the orchestrator only consumes the JSON object.
"""

import os
import asyncio
from dotenv import load_dotenv
from agents import (
    Agent,
    Runner,
    RunResult,
    ToolCallOutputItem,
    set_default_openai_key
)

# Step 1: Load API key and model
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_model = os.environ.get("OPENAI_MODEL")
set_default_openai_key(openai_api_key)


# Step 2: Define the sub-agent that returns JSON data
data_agent = Agent(
    name="Data Agent",
    model=openai_model,
    instructions="""
    You are a data bot that returns structured information.
    Respond with JSON data only. For example:
    {"city": "Paris", "country": "France", "population": "2M"}
    """
)


# Step 3: Define a custom output extractor function
async def extract_json_payload(run_result: RunResult) -> str:
    """
    Extracts JSON payload from tool output messages.
    Looks in reverse order of messages for ToolCallOutputItem containing JSON.
    """
    for item in reversed(run_result.new_items):
        if isinstance(item, ToolCallOutputItem) and item.output.strip().startswith("{"):
            return item.output.strip()
    return "{}"  # fallback if nothing found


# Step 4: Turn the sub-agent into a tool with custom extractor
json_tool = data_agent.as_tool(
    tool_name="get_data_json",
    tool_description="Runs the data agent and returns only JSON output",
    custom_output_extractor=extract_json_payload,
)


# Step 5: Define the orchestrator agent that uses the above tool
orchestrator_agent = Agent(
    name="Orchestrator Agent",
    model=openai_model,
    instructions=(
        "You are a smart orchestrator. Use the get_data_json tool to get structured data "
        "about cities, and just return what the tool gives you."
    ),
    tools=[json_tool],
)


# Step 6: Run the orchestrator
async def main():
    print("=== Custom Output Extraction Demo ===\n")
    result = await Runner.run(
        orchestrator_agent,
        input="Tell me about Paris in JSON format."
    )
    print("=== Extracted JSON Output ===")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
