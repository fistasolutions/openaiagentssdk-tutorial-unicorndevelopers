import asyncio
from dataclasses import dataclass
from typing import List

from agents import Agent, RunContextWrapper, Runner, function_tool
from agents import set_default_openai_key
from dotenv import load_dotenv
import os

# Load your environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(api_key)

# Define a user info data class
@dataclass
class UserInfo:
    name: str
    uid: int

# Define a multi-user context wrapper that can support a dynamic list of users
@dataclass
class MultiUserInfo:
    users: List[UserInfo]

# Tool that fetches ages (hardcoded here for simplicity, can be replaced with actual logic)
@function_tool
async def fetch_user_ages(wrapper: RunContextWrapper[MultiUserInfo]) -> str:
    # Simulate user age resolution (here, a fixed age for demo purposes)
    responses = [
        f"{user.name} (uid={user.uid}) is {40 + i} years old"
        for i, user in enumerate(wrapper.context.users)
    ]
    return "\n".join(responses)

# Main runner
async def main():
    # Create any number of users dynamically
    users = [
        UserInfo(name="Alice", uid=1),
        UserInfo(name="Bob", uid=2),
        UserInfo(name="Charlie", uid=3),
    ]
    context = MultiUserInfo(users=users)

    # Create agent
    agent = Agent[MultiUserInfo](
        name="User Info Assistant",
        tools=[fetch_user_ages],
    )
    input1 = "What are the ages of all users?"
    input2 = "What is the age of Alice?"
    input3 = "What is the age of Bob?"
    input4 = "What is the age of Charlie?"
    input5 = "What are the ages of Alice and Bob?"
    input6 = "What are the ages of Alice and Charlie?"
    input7 = "What are the ages of Bob and Charlie?"
    # Run the agent
    print("Query 1:", input1)
    result = await Runner.run(
        starting_agent=agent,
        input=input1,
        context=context,
    )
    print(result.final_output)
    print("\n===============\n")
    print("Query 2:", input2)
    result = await Runner.run(
        starting_agent=agent,
        input=input2,
        context=context,
    )
    print(result.final_output)
    print("\n===============\n")
    print("Query 3:", input3)
    result = await Runner.run(
        starting_agent=agent,
        input=input5,
        context=context,
    )
    print(result.final_output)
    

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
