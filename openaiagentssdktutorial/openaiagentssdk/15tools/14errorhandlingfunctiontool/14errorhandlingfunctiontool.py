import os
import asyncio
from dotenv import load_dotenv
from typing import Any
from agents import (
    Agent,
    Runner,
    RunContextWrapper,
    function_tool,
    set_default_openai_key,
)

# Load .env for OpenAI credentials
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_model = os.environ.get("OPENAI_MODEL")
set_default_openai_key(openai_api_key)


# ✅ Correct error handler (takes two arguments)
def custom_error_handler(ctx: RunContextWrapper[Any], err: Exception) -> str:
    return f"Oops! Something went wrong in the tool: {str(err)}"


# A function tool that may raise a division error
@function_tool(failure_error_function=custom_error_handler)
def risky_division(ctx: RunContextWrapper[Any], numerator: int, denominator: int) -> str:
    """
    Performs a division and returns the result.

    Args:
        numerator: The number to divide.
        denominator: The number to divide by.
    """
    result = numerator / denominator
    return f"Result: {result}"


# Main agent
agent = Agent(
    name="Math Helper",
    model=openai_model,
    instructions="You are a helpful calculator. Use the risky_division tool to divide numbers.",
    tools=[risky_division],
)


async def main():
    print("=== Tool Error Handling Demo ===\n")
    result = await Runner.run(
        agent,
        input="Divide 10 by 0 using risky_division."
    )
    print("=== Final Output ===")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
