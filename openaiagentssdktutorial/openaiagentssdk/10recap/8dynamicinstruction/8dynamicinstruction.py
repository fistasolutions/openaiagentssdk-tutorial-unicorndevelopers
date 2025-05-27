from agents import Agent, Runner, set_default_openai_key
from dataclasses import dataclass
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
set_default_openai_key(os.getenv("OPENAI_API_KEY"))
openai_model = os.environ.get("OPENAI_MODEL")
# Define a simple user context
@dataclass
class UserContext:
    name: str
    is_premium: bool

# Dynamic instructions function
def dynamic_instructions(context, agent) -> str:
    user_name = context.context.name
    if context.context.is_premium:
        return f"Hello {user_name}! You are a premium user. Give detailed premium support."
    else:
        return f"Hello {user_name}! Provide standard support."

# Create agent using dynamic instructions
agent = Agent[UserContext](
    name="Dynamic Agent",
    instructions=dynamic_instructions,
    model=openai_model
)

# Run the agent for different users

# Premium user
premium_user = UserContext(name="Alice", is_premium=True)
print("\n--- Premium User ---")
result1 = Runner.run_sync(agent, "What support do I have access to?", context=premium_user)
print(result1.final_output)

# Free user
free_user = UserContext(name="Bob", is_premium=False)
print("\n--- Free User ---")
result2 = Runner.run_sync(agent, "What support do I have access to?", context=free_user)
print(result2.final_output)
