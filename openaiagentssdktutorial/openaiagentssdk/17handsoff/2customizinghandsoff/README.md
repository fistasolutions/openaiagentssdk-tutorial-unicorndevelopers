# 🛠️ Customizing Agent Handoff Example

## 📋 Overview
This example demonstrates how to **customize agent handoff** behavior using callbacks and tool overrides. You can run custom logic when a handoff occurs, and change the tool's name and description for clarity.

## 🎯 Key Concepts

### **Customizing Handoff**
- **Callback (`on_handoff`)**: Run custom code (e.g., logging, notifications) when a handoff is triggered.
- **Tool Name/Description Override**: Change how the handoff tool appears to the agent.
- **Explicit Handoff**: Use the `handoff()` function for advanced customization.

## 📁 Code Walkthrough

```python
from dotenv import load_dotenv
import os
from agents import Agent, Runner, handoff, set_default_openai_key, RunContextWrapper

# Load env variables
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
openai_model = os.environ.get("OPENAI_MODEL")

# Specialized agent to handoff to
refund_agent = Agent(
    name="RefundAgent",
    instructions="You handle all refund-related queries.",
    model=openai_model
)

# Callback on handoff trigger
def on_handoff_trigger(ctx: RunContextWrapper[None]):
    print("📤 Handoff triggered to RefundAgent!")

# Create customized handoff object
refund_handoff = handoff(
    agent=refund_agent,
    on_handoff=on_handoff_trigger,
    tool_name_override="custom_refund_tool",
    tool_description_override="Handles refund issues for the user."
)

# Central agent (triage)
triage_agent = Agent(
    name="TriageAgent",
    instructions="""
        You determine if the user's query is about refunds, and if so, call the appropriate handoff tool.
    """,
    model=openai_model,
    handoffs=[refund_handoff]
)

# Trigger a refund-related query
result = Runner.run_sync(
    triage_agent,
    "I was overcharged and want to request a refund."
)

# Output result
print("🤖 Final Output:\n", result.final_output)
```

## 🚀 How to Run

```bash
uv run 2customizinghandsoff.py
```

## 🛠️ Customization Ideas

- **Log Handoff Events**: Use the callback to log or notify when a handoff occurs.
- **Change Tool Name/Description**: Make the handoff tool more descriptive for the agent.
- **Add More Callbacks**: Trigger different actions for different handoffs.
- **Combine with Input Filters**: Sanitize or preprocess input before handoff.

## 🔍 How It Works

1. **User Query**: The user submits a question.
2. **Triage Agent**: Decides if the query is about refunds.
3. **Handoff Triggered**: Callback runs, logging the event.
4. **Refund Agent**: Handles the query and returns a response.
5. **Result**: The final output is printed.

## 🐛 Troubleshooting

- **Callback Not Running**: Ensure the callback function is passed to `handoff()`.
- **Tool Name Not Changing**: Check the `tool_name_override` and `tool_description_override` parameters.
- **No Output**: Verify your OpenAI API key and model are set.

## 📚 Best Practices

- **Use Callbacks for Monitoring**: Track handoff events for analytics or auditing.
- **Make Tool Names Clear**: Helps agents understand what each tool does.
- **Test Customizations**: Try different queries and callbacks to ensure correct behavior.

---

*This example shows how to add custom logic and clarity to agent handoff, making your support system more robust and transparent.* 