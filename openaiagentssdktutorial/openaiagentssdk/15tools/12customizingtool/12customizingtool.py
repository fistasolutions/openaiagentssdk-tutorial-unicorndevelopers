from agents import Agent, Runner, set_default_openai_key, function_tool, RunConfig
from dotenv import load_dotenv
import os
import asyncio

# === Load Environment Variables ===
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
openai_model = os.environ.get("OPENAI_MODEL")

# === Define a Function Tool that Internally Runs a Custom Agent ===
@function_tool
async def run_my_agent() -> str:
    """A tool that runs the agent with custom configs"""

    # Define internal agent
    agent = Agent(
        name="My agent",
        instructions="You are a motivational coach. Give a powerful 2-line quote.",
        model=openai_model
    )

    # RunConfig to customize the run
    run_config = RunConfig(
        model=openai_model,
        model_settings={"temperature": 0.9},  # More creative outputs
        workflow_name="custom_agent_tool_run"
    )

    # Run the agent with custom settings
    result = await Runner.run(
        agent,
        input="I feel unmotivated, inspire me.",
        max_turns=3,
        run_config=run_config
    )

    return str(result.final_output)

# === Use This Tool in Another Agent ===
main_agent = Agent(
    name="Orchestrator",
    instructions="Use the available tools to inspire the user.",
    tools=[run_my_agent],
    model=openai_model
)

# === Main Async Execution ===
async def main():
    result = await Runner.run(
        main_agent,
        input="I need some inspiration, please help."
    )
    print("🔹 Final Output:\n", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
