from agents import Agent, Runner, set_default_openai_key
from dotenv import load_dotenv
import os

# Load and set your OpenAI API key
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
model=os.environ.get("OPENAI_MODEL")
# Create the agent
agent = Agent(
    name="Assistant",
    instructions="Reply very concisely.",
    model=model
)

# First turn
result1 = Runner.run_sync(agent, "What city is the Golden Gate Bridge in?")
print("Turn 1 Output:", result1.final_output)  # Expected: San Francisco

# Prepare input for second turn using previous context + new user message
second_input = result1.to_input_list() + [{"role": "user", "content": "What state is it in?"}]

# Second turn
result2 = Runner.run_sync(agent, second_input)
print("Turn 2 Output:", result2.final_output)  # Expected: California
