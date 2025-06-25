import os
from dotenv import load_dotenv
from agents import Agent, Runner, handoff, set_default_openai_key
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

# 🔐 Load API keys
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
openai_model = os.environ.get("OPENAI_MODEL")

# 🧾 Refund Agent (receives handoff)
refund_agent = Agent(
    name="Refund Agent",
    instructions="You specialize in handling refund-related customer queries.",
    model=openai_model
)

# 🤝 Handoff object
refund_handoff = handoff(agent=refund_agent)

# 🧠 Main Triage Agent with recommended handoff instructions
triage_agent = Agent(
    name="Triage Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are a customer service assistant. Handle general inquiries, but if the question is about refunds, use the refund tool.""",
    model=openai_model,
    handoffs=[refund_handoff],
)

# 🚀 Test query
result = Runner.run_sync(triage_agent, "I want to request a refund for my last order.")

# 🖨️ Output
print("🤖 Final Output:\n", result.final_output)
