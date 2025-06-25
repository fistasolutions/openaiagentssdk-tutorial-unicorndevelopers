# 📝 Recommended Prompt Prefix Example

## 📋 Overview
This example demonstrates how to use the **recommended prompt prefix** for agent handoff. Using a standard prompt prefix helps the agent understand when and how to use handoff tools, improving reliability and clarity.

## 🎯 Key Concepts

### **Recommended Prompt Prefix**
- **Purpose**: Guide the agent to use handoff tools correctly.
- **Clarity**: Makes agent instructions explicit and handoff-friendly.
- **Best Practices**: Encourages consistent, reliable handoff behavior.

## 📁 Code Walkthrough

```python
import os
from dotenv import load_dotenv
from agents import Agent, Runner, handoff, set_default_openai_key
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

# Load API keys
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
openai_model = os.environ.get("OPENAI_MODEL")

# Refund Agent (receives handoff)
refund_agent = Agent(
    name="Refund Agent",
    instructions="You specialize in handling refund-related customer queries.",
    model=openai_model
)

# Handoff object
refund_handoff = handoff(agent=refund_agent)

# Main Triage Agent with recommended handoff instructions
triage_agent = Agent(
    name="Triage Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are a customer service assistant. Handle general inquiries, but if the question is about refunds, use the refund tool.""",
    model=openai_model,
    handoffs=[refund_handoff],
)

# Test query
result = Runner.run_sync(triage_agent, "I want to request a refund for my last order.")

# Output
print("🤖 Final Output:\n", result.final_output)
```

## 🚀 How to Run

```bash
uv run 5recomendedprompt.py
```

## 🛠️ Customization Ideas

- **Customize the Prompt**: Add more details or instructions for complex routing.
- **Combine with Other Handoff Features**: Use with callbacks, input filters, or structured input.
- **Test with Different Queries**: Ensure the agent uses the handoff tool as intended.

## 🔍 How It Works

1. **User Query**: The user submits a question.
2. **Triage Agent**: Uses the recommended prompt prefix to guide handoff behavior.
3. **Refund Agent**: Handles refund-related queries.
4. **Result**: The final output is printed.

## 🐛 Troubleshooting

- **Agent Not Using Handoff Tool**: Ensure the recommended prompt prefix is included in the instructions.
- **No Output**: Verify your OpenAI API key and model are set.
- **Unexpected Behavior**: Refine the prompt or add more explicit instructions.

## 📚 Best Practices

- **Always Use the Recommended Prefix**: For best handoff reliability.
- **Keep Instructions Clear**: The more explicit, the better.
- **Test with Realistic Scenarios**: Try various user queries.

---

*This example shows how to use prompt engineering best practices to guide agent handoff, making your support system more robust and predictable.* 