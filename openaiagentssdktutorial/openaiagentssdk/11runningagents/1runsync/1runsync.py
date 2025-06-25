from agents import Agent, Runner
from dotenv import load_dotenv
from agents import set_default_openai_key
import os
import asyncio

# Load API key
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
openai_model = os.environ.get("OPENAI_MODEL")

# Create agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=openai_model
)

# Async function using run()
async def main():
    result = await Runner.run(agent, "What is the capital of Pakistan?")
    print(result.final_output)

# Run the async function
asyncio.run(main())
