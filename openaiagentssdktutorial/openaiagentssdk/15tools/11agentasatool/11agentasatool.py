from agents import Agent, Runner, set_default_openai_key
from dotenv import load_dotenv
import os
import asyncio

# === Load API Key and Model ===
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
openai_model = os.environ.get("OPENAI_MODEL")

# === Specialized Translation Agents ===
spanish_agent = Agent(
    name="Spanish agent",
    instructions="You translate the user's message to Spanish.",
    model=openai_model
)

french_agent = Agent(
    name="French agent",
    instructions="You translate the user's message to French.",
    model=openai_model
)

# === Orchestrator Agent That Uses Other Agents as Tools ===
orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions=(
        "You are a translation assistant. "
        "Use the tools to translate the user's message into the requested language."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate user input into Spanish."
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate user input into French."
        )
    ],
    model=openai_model
)

# === Main Async Runner ===
async def main():
    result = await Runner.run(
        orchestrator_agent,
        input="Translate 'Good morning, my friend!' to Spanish and French."
    )
    print("🔹 Final Output:\n", result.final_output)

# === Run Async Function ===
if __name__ == "__main__":
    asyncio.run(main())
