from agents import Agent, Runner, function_tool, ModelSettings, set_default_openai_key
import os
from dotenv import load_dotenv

load_dotenv()
set_default_openai_key(os.getenv("OPENAI_API_KEY"))

@function_tool
def add_numbers(a: int, b: int) -> int:
    return a + b

agent = Agent(
    name="No Tool Agent",
    instructions="You are a math assistant. You must answer without using tools.",
    tools=[add_numbers],  # tools are passed, but won't be used
    model_settings=ModelSettings(tool_choice="none"),
)

result = Runner.run_sync(agent, "What is 3 + 5?")
print("\n--- AUTO Result ---")
print(result.final_output)
