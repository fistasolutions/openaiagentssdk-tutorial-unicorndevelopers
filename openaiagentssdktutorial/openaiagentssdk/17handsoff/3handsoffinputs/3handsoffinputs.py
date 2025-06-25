import os
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import Agent, handoff, Runner, RunContextWrapper, set_default_openai_key

# 🔐 Load OpenAI key and model
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
openai_model = os.environ.get("OPENAI_MODEL")

# 📝 Define expected handoff input
class EscalationData(BaseModel):
    reason: str

# 🔁 Callback executed when handoff is triggered
async def on_handoff(ctx: RunContextWrapper[None], input_data: EscalationData):
    print(f"🚨 Escalation triggered with reason: {input_data.reason}")

# 🎯 Escalation agent
escalation_agent = Agent(
    name="Escalation Agent",
    instructions="You handle high-priority customer complaints.",
    model=openai_model
)

# 🔧 Handoff object with input type + callback
escalation_handoff = handoff(
    agent=escalation_agent,
    on_handoff=on_handoff,
    input_type=EscalationData
)

# 🧠 Central agent that may escalate
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are a customer support agent. If a complaint is very serious, escalate it using the handoff tool."
        " Ask the user for a reason and pass it to the escalation tool."
    ),
    model=openai_model,
    handoffs=[escalation_handoff],
)

# 🚀 Run the agent
result = Runner.run_sync(
    triage_agent,
    "This is outrageous, my credit card was charged twice and nobody is responding!"
)

# 🖨️ Show result
print("🤖 Final Output:\n", result.final_output)
