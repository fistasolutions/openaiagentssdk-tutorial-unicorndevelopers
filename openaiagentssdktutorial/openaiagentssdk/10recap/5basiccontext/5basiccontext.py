from dataclasses import dataclass
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
from agents import set_default_openai_key
import asyncio
import os

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(api_key)
openai_model = os.environ.get("OPENAI_MODEL")

@dataclass
class UserContext:
    uid: str
    is_pro_user: bool

@function_tool
def greet_user(context: UserContext) -> str:
    """Give a personalized greeting based on user's status."""
    if context.is_pro_user:
        return f"Hello Pro user {context.uid}, welcome back!"
    else:
        return f"Hello {context.uid}, upgrade to Pro for more features!"
    
agent = Agent[UserContext](
    name="Simple Greeter",
    instructions="Greet the user based on their account type using the tool.",
    tools=[greet_user],
    model=openai_model
)

pro_user = UserContext(uid="alice123", is_pro_user=True)
free_user = UserContext(uid="bob456", is_pro_user=False)

print("\n--- Pro User ---")
result = Runner.run_sync(agent, "Please greet me", context=pro_user)
print(result.final_output)

print("\n--- Free User ---")
result = Runner.run_sync(agent, "Please greet me", context=free_user)
print(result.final_output)