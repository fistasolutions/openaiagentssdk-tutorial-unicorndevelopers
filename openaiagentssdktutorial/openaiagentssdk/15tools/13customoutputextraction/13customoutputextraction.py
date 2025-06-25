from agents import Agent, Runner, RunResult, ToolCallOutputItem, set_default_openai_key
from dotenv import load_dotenv
import os
import asyncio

# Load API keys and config
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
openai_model = os.environ.get("OPENAI_MODEL")


# 🧠 Sub-agent that returns JSON-like data
data_agent = Agent(
    name="Data Agent",
    instructions="""
    Your task is to return only a JSON object like:
    {"title": "Engineer", "experience": 5}
    Don't explain anything. Just return JSON.
    """,
    model=openai_model
)


# 🔍 Custom output extractor: extract only JSON-like outputs
async def extract_json_payload(run_result: RunResult) -> str:
    for item in reversed(run_result.new_items):
        if isinstance(item, ToolCallOutputItem) and item.output.strip().startswith("{"):
            return item.output.strip()
    return "{}"  # Fallback value


# 🔧 Convert sub-agent into a tool
json_tool = data_agent.as_tool(
    tool_name="get_user_profile",
    tool_description="Get the user profile in JSON format",
    custom_output_extractor=extract_json_payload
)


# 🧑‍🔧 Main orchestrator agent
orchestrator = Agent(
    name="Orchestrator",
    instructions="""
    Use the tools to get the user profile in JSON.
    Only return the JSON.
    """,
    tools=[json_tool],
    model=openai_model
)


# 🚀 Run the full pipeline
async def main():
    result = await Runner.run(
        orchestrator,
        input="Get a user profile from the tool."
    )
    print("✅ Final extracted JSON:\n", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
