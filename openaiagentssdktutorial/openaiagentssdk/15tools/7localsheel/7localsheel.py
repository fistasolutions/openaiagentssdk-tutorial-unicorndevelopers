import asyncio
from agents import Agent, Runner, set_default_openai_key
from agents.tool import LocalShellTool
from dotenv import load_dotenv
import os

load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
model = os.environ.get("OPENAI_MODEL")

# Configure the Local Shell tool
shell_tool = LocalShellTool()

agent = Agent(
    name="Shell Agent",
    instructions="You can run shell commands on the local machine. Use this power responsibly!",
    tools=[shell_tool],
    model=model
)

async def main():
    result = await Runner.run(
        agent,
        input="List the files in the current directory using the shell."
    )
    print("💻 Final Output:\n", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
