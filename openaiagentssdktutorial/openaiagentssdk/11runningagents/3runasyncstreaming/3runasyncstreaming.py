from agents import Agent, Runner
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
from agents import set_default_openai_key
import os
import asyncio

# Load API key
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)

# Create agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant that explains things clearly.",
    model="gpt-4o"
)

# Async function using streaming
async def main():
    print("=== Starting Stream ===")
    
    # Get the streaming result
    result = Runner.run_streamed(agent, "Explain recursion in programming in simple terms.")
    
    # Process the streaming events
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
    
    print("\n=== Stream Complete ===")

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
