from agents import Agent, Runner, set_default_openai_key, ItemHelpers
from dotenv import load_dotenv
import os

load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))

agent = Agent(
    name="Assistant",
    instructions="Answer concisely. Share your reasoning."
)

result = Runner.run_sync(agent, "Explain gravity in simple words.")

# Print Final Output
print("🔹 Final Output:\n", result.final_output)
print("\n🧾 New Items Generated:")

# Loop through new_items
for item in result.new_items:
    print(f"\n▶️ Item Type: {item.type}")
    if item.type == "message_output_item":
        print("💬 Message:", ItemHelpers.text_message_output(item))
    elif item.type == "reasoning_item":
        print("🧠 Reasoning:", item.raw_item.reasoning)
    else:
        print("📦 Raw Item Data:", item.raw_item)
