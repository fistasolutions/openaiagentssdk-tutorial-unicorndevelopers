from agents import Agent, AgentHooks, Runner, set_default_openai_key
import os
from dotenv import load_dotenv

# Load OpenAI API key
load_dotenv()
set_default_openai_key(os.getenv("OPENAI_API_KEY"))
openai_model = os.environ.get("OPENAI_MODEL")
# Step 1: Create custom hooks
class LoggingHooks(AgentHooks):
    def on_run_start(self, context, agent, input):
        print(f"[HOOK] Agent '{agent.name}' started a run with input: '{input}'")

    def on_run_end(self, context, agent, input, final_output):
        print(f"[HOOK] Agent '{agent.name}' completed the run. Output: '{final_output}'")

    def on_error(self, context, agent, input, error):
        print(f"[HOOK] Agent '{agent.name}' encountered an error: {error}")

# Step 2: Create a simple agent and attach hooks
agent = Agent(
    name="Greeting Agent",
    instructions="Respond to greetings politely and kindly.",
    hooks=LoggingHooks(),
    model=openai_model
)

# Step 3: Run the agent
print("\n--- Run Example ---")
query = "Hi there!"
result = Runner.run_sync(agent, query)
print("Final Output:", result.final_output)
