from agents import Agent, Runner
from dotenv import load_dotenv
from agents import set_default_openai_key
import os

# Load OpenAI API key
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
openai_model = os.environ.get("OPENAI_MODEL")
# Create agent
agent = Agent(
    name="LoopTester",
    instructions="You are a helpful assistant. Answer clearly.",
    model=openai_model
)

# Run synchronously using agent loop
result = Runner.run_sync(agent, "What is the capital of Pakistan?")
print("\n--- Final Output ---")
print(result.final_output)
