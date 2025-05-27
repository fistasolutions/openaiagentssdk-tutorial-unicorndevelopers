from agents import Agent, Runner, function_tool, ModelSettings, set_default_openai_key
import os
from dotenv import load_dotenv

load_dotenv()
set_default_openai_key(os.getenv("OPENAI_API_KEY"))

@function_tool
def add_numbers(a: int, b: int) -> int:
    return a + b

agent = Agent(
    name="Auto Agent",
    instructions="You can use the tool if needed.",
    tools=[add_numbers],
    model_settings=ModelSettings(tool_choice="auto"),
)

result = Runner.run_sync(agent, "What is 3 + 5?")
print("\n--- AUTO Result ---")
print(result.final_output)
