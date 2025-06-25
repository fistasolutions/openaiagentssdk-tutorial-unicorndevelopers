from agents import Agent, Runner, set_default_openai_key
from dotenv import load_dotenv
import os

load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))

# Define two agents: a triage and a specialist
triage_agent = Agent(
    name="Triage Agent",
    instructions="Route to the correct agent if necessary, or answer simply."
)

specialist_agent = Agent(
    name="Specialist Agent",
    instructions="You are a detailed assistant specialized in answering tech questions."
)

# Simulate a handoff manually for the example
result = Runner.run_sync(specialist_agent, "What is an API?")
print("🔹 Final output:", result.final_output)

# Use last_agent to continue the conversation
follow_up_input = result.to_input_list() + [{"role": "user", "content": "Can you give an example of an API?"}]
next_result = Runner.run_sync(result.last_agent, follow_up_input)
print("🔹 Follow-up answer:", next_result.final_output)
