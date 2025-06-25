import asyncio
from agents import Agent, Runner, set_default_openai_key
from agents.tool import CodeInterpreterTool, CodeInterpreter
from dotenv import load_dotenv
import os

load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
model=os.environ.get("OPENAI_MODEL")

# Define the agent with the code interpreter tool
agent = Agent(
    name="Code Genius",
    instructions="You can write and execute Python code to solve problems.",
    tools=[
        CodeInterpreterTool(CodeInterpreter(type='code_interpreter', container={'type': 'auto'})),
    ],
    model=model
)

async def main():
    result = await Runner.run(
        agent,
        input="Write Python code to calculate the sum of numbers from 1 to 100 and explain the result."
    )
    print("🔢 Final Output:\n", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
