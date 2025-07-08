"""
Title: Using Agents as Tools with OpenAI Agents SDK

Description:
This example demonstrates how to use specialized agents (e.g., for translating to Spanish and French)
as tools that are callable by a central orchestrator agent. This structure allows modular design
where the main agent delegates work without handing off conversation control.

Requirements:
- Basic Python knowledge (async functions, classes)
- OpenAI Agents SDK installed (`pip install openai-agents`)
- `.env` file with:
    OPENAI_API_KEY=your-api-key
    OPENAI_MODEL=gpt-4o or gpt-3.5-turbo
"""

import os
import asyncio
from dotenv import load_dotenv

from agents import Agent, Runner, set_default_openai_key

# Step 1: Load API Key and Model from environment
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_model = os.environ.get("OPENAI_MODEL")
set_default_openai_key(openai_api_key)

# Step 2: Create specialized agents for translation
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

# Step 3: Create the orchestrator agent and register translation agents as tools
orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation assistant. Use tools to translate user input into Spanish or French. "
        "If asked for multiple translations, call the corresponding tools."
    ),
    model=openai_model,
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
    ]
)

# Step 4: Main async function to run the orchestrator agent
async def main():
    print("=== Running Translation Orchestrator Agent ===\n")
    result = await Runner.run(
        orchestrator_agent,
        input="Say 'Hello, how are you?' in Spanish and French."
    )
    print("=== Final Output ===")
    print(result.final_output)


# Step 5: Run the script
if __name__ == "__main__":
    asyncio.run(main())
