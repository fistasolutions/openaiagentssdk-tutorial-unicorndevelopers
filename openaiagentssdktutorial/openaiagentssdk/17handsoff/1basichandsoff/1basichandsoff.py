from dotenv import load_dotenv
import os
from agents import Agent, Runner, handoff, set_default_openai_key

# 🔐 Load environment variables
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
openai_model = os.environ.get("OPENAI_MODEL")

# 🧾 Specialized agents
billing_agent = Agent(
    name="Billing agent",
    instructions="You are an expert in handling billing-related queries.",
    model=openai_model
)

refund_agent = Agent(
    name="Refund agent",
    instructions="You are an expert in refund processing.",
    model=openai_model
)

# 🧠 Triage agent that delegates
triage_agent = Agent(
    name="Triage agent",
    instructions="""
    You're a smart assistant that decides whether a user's query is about billing or refunds, 
    and then delegates to the correct agent.
    """,
    model=openai_model,
    handoffs=[
        billing_agent,  # Direct handoff
        handoff(refund_agent)  # Explicit handoff with customization options if needed
    ]
)

# 🚀 Run
result = Runner.run_sync(
    triage_agent,
    "I was charged twice for my subscription and I need my money back."
)

print("🤖 Final Output:\n", result.final_output)
