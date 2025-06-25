from agents import Agent, Runner, FunctionTool, RunContextWrapper, set_default_openai_key
from dotenv import load_dotenv
from pydantic import BaseModel
import os
from typing import Any

# === Load ENV and OpenAI Key ===
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
openai_model = os.environ.get("OPENAI_MODEL")

# === Business Logic Function ===
def do_some_work(data: str) -> str:
    return f"[Processed] {data}"

# === Tool Input Schema ===
class FunctionArgs(BaseModel):
    username: str
    age: int

# === Tool Execution Handler ===
async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = FunctionArgs.model_validate_json(args)
    return do_some_work(data=f"{parsed.username} is {parsed.age} years old")

# === Manually Created Function Tool ===
schema = FunctionArgs.model_json_schema()
schema["additionalProperties"] = False

custom_tool = FunctionTool(
    name="process_user",
    description="Processes extracted user data",
    params_json_schema=schema,
    on_invoke_tool=run_function,
)

# === Agent Configuration ===
agent = Agent(
    name="UserProcessorAgent",
    instructions="You are an assistant who extracts and processes user data using tools.",
    tools=[custom_tool],
    model=openai_model
)

# === Run the Agent Synchronously ===
result = Runner.run_sync(agent, "The user's name is Sarah and she is 30 years old.")
print("🔹 Final Output:\n", result.final_output)
