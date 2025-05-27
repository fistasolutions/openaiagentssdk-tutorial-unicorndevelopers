from agents import Agent, Runner, function_tool, ModelSettings, set_default_openai_key
import os
from dotenv import load_dotenv

# Load OpenAI key
load_dotenv()
set_default_openai_key(os.getenv("OPENAI_API_KEY"))

@function_tool
# Define a simple tool
def add_numbers(a: int, b: int) -> int:
    return a + b

# Create the agent
agent = Agent(
    name="Math Agent",
    instructions="You are a math assistant. Use the tool to add numbers.",
    tools=[add_numbers],
    model_settings=ModelSettings(tool_choice="required"),  # Force tool use
    tool_use_behavior="stop_on_first_tool",  # Stop after first tool is used
)

# Run a query that triggers tool use
query = "What is 3 + 5?"

# Execute
result = Runner.run_sync(agent, query)
print("\n--- Final Result ---")
print(result.final_output)  # Should be 8 (via tool)
