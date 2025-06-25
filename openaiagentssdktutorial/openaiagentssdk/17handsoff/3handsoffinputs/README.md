# 📦 Handoff Inputs Example

## 📋 Overview
This example demonstrates how to pass **structured input** to a handoff agent using Pydantic models. This allows you to validate and process complex data when escalating or delegating queries.

## 🎯 Key Concepts

### **Structured Handoff Input**
- **Pydantic Models**: Define and validate structured input data.
- **Async Callbacks**: Run asynchronous logic when a handoff occurs.
- **Input Type**: Specify the expected input schema for the handoff.

## 📁 Code Walkthrough

```python
import os
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import Agent, handoff, Runner, RunContextWrapper, set_default_openai_key

# Load OpenAI key and model
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
openai_model = os.environ.get("OPENAI_MODEL")

# Define expected handoff input
class EscalationData(BaseModel):
    reason: str

# Callback executed when handoff is triggered
async def on_handoff(ctx: RunContextWrapper[None], input_data: EscalationData):
    print(f"🚨 Escalation triggered with reason: {input_data.reason}")

# Escalation agent
escalation_agent = Agent(
    name="Escalation Agent",
    instructions="You handle high-priority customer complaints.",
    model=openai_model
)

# Handoff object with input type + callback
escalation_handoff = handoff(
    agent=escalation_agent,
    on_handoff=on_handoff,
    input_type=EscalationData
)

# Central agent that may escalate
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are a customer support agent. If a complaint is very serious, escalate it using the handoff tool."
        " Ask the user for a reason and pass it to the escalation tool."
    ),
    model=openai_model,
    handoffs=[escalation_handoff],
)

# Run the agent
result = Runner.run_sync(
    triage_agent,
    "This is outrageous, my credit card was charged twice and nobody is responding!"
)

# Show result
print("🤖 Final Output:\n", result.final_output)
```

## 🚀 How to Run

```bash
uv run 3handsoffinputs.py
```

## 🛠️ Customization Ideas

- **Add More Input Fields**: Expand the Pydantic model for richer data.
- **Handle Different Escalation Types**: Use enums or multiple models for different scenarios.
- **Async Processing**: Perform async operations (e.g., send notifications) in the callback.
- **Input Validation**: Enforce stricter validation rules.

## 🔍 How It Works

1. **User Query**: The user submits a complaint.
2. **Triage Agent**: Decides if escalation is needed.
3. **Input Collection**: Asks for and validates escalation reason.
4. **Async Callback**: Runs custom logic with the structured input.
5. **Escalation Agent**: Handles the escalated query.
6. **Result**: The final output is printed.

## 🐛 Troubleshooting

- **Validation Errors**: Check the Pydantic model and input data.
- **Callback Not Running**: Ensure the callback is async and passed to `handoff()`.
- **No Output**: Verify your OpenAI API key and model are set.

## 📚 Best Practices

- **Use Structured Input for Complex Data**: Ensures data integrity and clarity.
- **Validate Input**: Catch errors early with Pydantic.
- **Leverage Async Callbacks**: For I/O-bound or long-running operations.
- **Document Input Schemas**: Make it clear what data is expected.

---

*This example shows how to safely and flexibly pass structured data to handoff agents, enabling advanced workflows and escalation logic.* 