import os
from dotenv import load_dotenv
from agents import Agent, Runner, handoff, set_default_openai_key
from agents.extensions import handoff_filters

# 🔐 Load API keys
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
openai_model = os.environ.get("OPENAI_MODEL")

# 🎯 FAQ Agent (receives handoff)
faq_agent = Agent(
    name="FAQ Agent",
    instructions="You answer frequently asked questions clearly and concisely.",
    model=openai_model
)

# 🧹 Handoff with input filter to remove tool calls
faq_handoff = handoff(
    agent=faq_agent,
    input_filter=handoff_filters.remove_all_tools
)

# 🧠 Main agent (performs handoff)
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You handle general customer queries. "
        "If the user is asking a standard FAQ, use the FAQ handoff tool to pass it along."
    ),
    model=openai_model,
    handoffs=[faq_handoff],
)

# 🚀 Run a sample query
result = Runner.run_sync(triage_agent, "What is your refund policy?")

# 🖨️ Output
print("🤖 Final Output:\n", result.final_output)
