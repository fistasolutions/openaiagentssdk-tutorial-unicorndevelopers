from agents import Agent, Runner, set_default_openai_key
import asyncio
import os
from dotenv import load_dotenv

# Load your OpenAI API key from the .env file
load_dotenv()
set_default_openai_key(os.getenv("OPENAI_API_KEY"))
openai_model = os.environ.get("OPENAI_MODEL")
# Define the sub-agent for handling orders
order_agent = Agent(
    name="Order Agent",
    instructions="You handle all questions about orders, shipping, and delivery.",
)

# Define the sub-agent for handling support issues
support_agent = Agent(
    name="Support Agent",
    instructions="You handle support-related issues like login problems or account settings.",
)

# Define the main agent that decides who should answer
main_agent = Agent(
    name="Main Agent",
    instructions="""
        You help customers with general questions.
        If the question is about orders, hand it off to the Order Agent.
        If it's about support, hand it off to the Support Agent.
    """,
    handoffs=[order_agent, support_agent],
)

# Run an example

    # Test 1: Order-related question
print("\n--- Order Question ---")
result1 = Runner.run_sync(main_agent, "Where is my package?")
print(result1.final_output)

# Test 2: Support-related question
print("\n--- Support Question ---")
result2 = Runner.run_sync(main_agent, "I can't log in to my account.")
print(result2.final_output)

