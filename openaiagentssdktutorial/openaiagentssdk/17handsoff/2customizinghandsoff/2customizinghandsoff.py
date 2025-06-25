from dotenv import load_dotenv
import os
from agents import Agent, Runner, handoff, set_default_openai_key, RunContextWrapper

# 🔐 Load env variables
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
openai_model = os.environ.get("OPENAI_MODEL")

# 🎯 Specialized agent to handoff to
refund_agent = Agent(
    name="RefundAgent",
    instructions="You handle all refund-related queries.",
    model=openai_model
)

# ✅ Callback on handoff trigger
def on_handoff_trigger(ctx: RunContextWrapper[None]):
    print("📤 Handoff triggered to RefundAgent!")

# 🔧 Create customized handoff object
refund_handoff = handoff(
    agent=refund_agent,
    on_handoff=on_handoff_trigger,
    tool_name_override="custom_refund_tool",
    tool_description_override="Handles refund issues for the user."
)

# 🧠 Central agent (triage)
triage_agent = Agent(
    name="TriageAgent",
    instructions="""
        You determine if the user's query is about refunds, and if so, call the appropriate handoff tool.
    """,
    model=openai_model,
    handoffs=[refund_handoff]
)

# 🚀 Trigger a refund-related query
result = Runner.run_sync(
    triage_agent,
    "I was overcharged and want to request a refund."
)

# 📦 Output result
print("🤖 Final Output:\n", result.final_output)
