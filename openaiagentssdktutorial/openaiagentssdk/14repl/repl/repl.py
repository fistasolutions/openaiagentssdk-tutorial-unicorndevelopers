import asyncio
from agents import Agent, run_demo_loop, set_default_openai_key
from dotenv import load_dotenv
import os

load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
model=os.environ.get("OPENAI_MODEL")

async def main() -> None:
    agent = Agent(name="Assistant", instructions="You are a helpful assistant.",model=model)
    await run_demo_loop(agent)

if __name__ == "__main__":
    asyncio.run(main())