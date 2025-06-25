from agents import Agent, Runner
from dotenv import load_dotenv
from agents import set_default_openai_key
import os

# Load API key
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)

# Create agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model="gpt-4o"
)

# Run synchronously
result = Runner.run_sync(agent, "What is the capital of Pakistan?")
print(result.final_output)
