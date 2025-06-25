from agents import Agent, Runner, set_default_openai_key
from dotenv import load_dotenv
import os

# Load environment and API key
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
model=os.environ.get("OPENAI_MODEL")
# Define your agent
agent = Agent(
    name="SummaryAgent",
    instructions="Summarize the user's message in 1 sentence.",
    model=model
)

# Run the agent using run_sync (returns RunResult)
result = Runner.run_sync(agent, "Explain the basics of quantum computing.")

# ✅ Access useful properties from RunResult (inherits RunResultBase)
print("\n📌 Final Output:")
print(result.final_output)

print("\n👤 Last Agent Used:")
print(result.last_agent.name)

print("\n🧾 Original Input:")
print(result.input)

print("\n🆕 New Items Generated:")
for item in result.new_items:
    print(f"- {item.type}")

print("\n📤 Raw Responses:")
for response in result.raw_responses:
    print(response)

# Guardrails (if any were used)
print("\n🛡️ Input Guardrail Results:", result.input_guardrail_results)
print("🛡️ Output Guardrail Results:", result.output_guardrail_results)
