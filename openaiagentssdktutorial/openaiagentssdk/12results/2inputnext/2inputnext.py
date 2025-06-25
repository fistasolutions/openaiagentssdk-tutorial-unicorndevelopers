from agents import Agent, Runner, set_default_openai_key
from dotenv import load_dotenv
import os

# Load environment variables and OpenAI key
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))

# Define the assistant agent
agent = Agent(
    name="Concise Assistant",
    instructions="Reply briefly but accurately.",
    model="gpt-4o"
)

# Step 1: First user input
first_result = Runner.run_sync(agent, "What city is the Golden Gate Bridge in?")
print("📍 First answer:", first_result.final_output)

# Step 2: Use `.to_input_list()` to maintain context, and ask a follow-up
follow_up_input = first_result.to_input_list() + [{"role": "user", "content": "What state is that in?"}]
second_result = Runner.run_sync(agent, follow_up_input)
print("📍 Follow-up answer:", second_result.final_output)
