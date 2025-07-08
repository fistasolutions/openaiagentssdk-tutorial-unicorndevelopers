"""
Title: Customizing Tool Agents using OpenAI Agents SDK

Description:
This example shows how to wrap an Agent as a custom function tool, where you invoke it using
Runner.run() with advanced configurations like max_turns and run_config.
"""

import os
import asyncio
from dotenv import load_dotenv
from typing import Any

from agents import (
    Agent,
    Runner,
    RunConfig,
    ModelSettings,
    function_tool,
    RunContextWrapper,
    set_default_openai_key
)

# Step 1: Load API key and default model
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_model = os.environ.get("OPENAI_MODEL")
set_default_openai_key(openai_api_key)


# Step 2: Define a function tool that internally runs an agent
@function_tool
async def run_my_agent() -> str:
    """A tool that runs a specialized agent with advanced settings."""
    
    agent = Agent(
        name="My Custom Agent",
        instructions="You are a creative assistant. Give detailed, poetic answers.",
        model=openai_model
    )

    # Custom run configuration (e.g., temperature, trace metadata, etc.)
    run_config = RunConfig(
        model=openai_model,
        model_settings=ModelSettings(temperature=0.9),
        max_turns=3,
        workflow_name="custom_tool_agent_workflow",
        trace_metadata={"use_case": "custom_tool_agent"}
    )

    # Execute the agent with advanced config
    result = await Runner.run(
        agent,
        input="Tell me a poetic description of the moon.",
        run_config=run_config
    )

    return str(result.final_output)


# Step 3: Create a main agent that uses the above as a tool
main_agent = Agent(
    name="Tool-Orchestrator Agent",
    instructions="You use the tool to describe nature poetically.",
    model=openai_model,
    tools=[run_my_agent]
)


# Step 4: Async runner
async def main():
    print("=== Running Custom Tool Agent ===\n")
    result = await Runner.run(
        main_agent,
        input="Can you describe the moon for me?"
    )
    print("=== Final Output ===")
    print(result.final_output)


# Step 5: Execute
if __name__ == "__main__":
    asyncio.run(main())
