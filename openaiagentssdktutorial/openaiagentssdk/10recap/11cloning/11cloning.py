from agents import Agent, Runner, set_default_openai_key
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
set_default_openai_key(os.getenv("OPENAI_API_KEY"))

# Step 1: Create a base agent (Pirate Agent)
pirate_agent = Agent(
    name="Pirate",
    instructions="You are a pirate. Answer everything like a pirate. Use phrases like 'Ahoy!', 'Matey!', and 'Arrr!'.",
    model="o3-mini",  # Optional: You can set your preferred model
)

# Step 2: Clone the pirate agent and change behavior to Robot
robot_agent = pirate_agent.clone(
    name="Robot",
    instructions="You are a robot. Respond in a robotic, logical tone. Mention efficiency and systems.",
)

# Step 3: Run both agents with the same input to compare their styles
query = "How do you feel today?"

print("\n--- Pirate Agent Response ---")
pirate_result = Runner.run_sync(pirate_agent, query)
print(pirate_result.final_output)

print("\n--- Robot Agent Response ---")
robot_result = Runner.run_sync(robot_agent, query)
print(robot_result.final_output)
