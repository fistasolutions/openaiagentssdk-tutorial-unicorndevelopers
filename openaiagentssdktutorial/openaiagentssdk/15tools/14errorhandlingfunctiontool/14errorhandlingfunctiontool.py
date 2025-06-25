from agents import Agent, Runner, RunContextWrapper, function_tool, set_default_openai_key
from dotenv import load_dotenv
import os

load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
openai_model = os.environ.get("OPENAI_MODEL")


# ❌ Intentionally crashing tool
@function_tool(
    failure_error_function=lambda ctx, e: f"❗ Custom Error Handler: Something went wrong! Error: {str(e)}"
)
def crashing_tool(ctx: RunContextWrapper[None]) -> str:
    """This tool crashes on purpose to demonstrate error handling."""
    raise ValueError("This is a simulated tool crash.")


# 🧠 Agent setup
agent = Agent(
    name="Resilient Assistant",
    instructions="Use tools, and if they fail, show custom error message.",
    tools=[crashing_tool],
    model=openai_model
)


# 🚀 Run it
if __name__ == "__main__":
    result = Runner.run_sync(agent, "Call the crashing tool")
    print("🧠 Final Output:\n", result.final_output)
