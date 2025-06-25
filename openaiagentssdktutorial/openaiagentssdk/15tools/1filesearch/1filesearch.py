from agents import Agent, FileSearchTool, Runner, WebSearchTool, set_default_openai_key
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
model=os.environ.get("OPENAI_MODEL")
agent = Agent(
    name="Assistant",
    tools=[
        FileSearchTool(
            max_num_results=3,
            vector_store_ids=["vs_6859b7221d108191884ab0709e033181"],
        ),
    ],
    model=model
)

async def main():
    result = await Runner.run(agent, "What is Current position of Muhammad Usman")

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())