# 🤝 Basic Agent Handoff Example

## 📋 Overview
This example demonstrates the **agent handoff** feature, where a central "triage" agent decides which specialized agent should handle a user's query. This is useful for routing customer support requests to the right expert (e.g., billing or refund).

## 🎯 Key Concepts

### **Agent Handoff**
- **Purpose**: Automatically delegate user queries to the most appropriate specialized agent.
- **Triage Agent**: An agent that analyzes the query and decides which agent should handle it.
- **Specialized Agents**: Agents with expertise in specific topics (e.g., billing, refunds).
- **`handoff`**: Mechanism to define and customize handoff behavior.

## 📁 Code Walkthrough

```python
from dotenv import load_dotenv
import os
from agents import Agent, Runner, handoff, set_default_openai_key

# Load environment variables
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
openai_model = os.environ.get("OPENAI_MODEL")

# Specialized agents
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

# Triage agent that delegates
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

# Run
result = Runner.run_sync(
    triage_agent,
    "I was charged twice for my subscription and I need my money back."
)

print("🤖 Final Output:\n", result.final_output)
```

## 🚀 How to Run

```bash
uv run 1basichandsoff.py
```

## 🛠️ Customization Ideas

- **Add More Specialized Agents**: Create agents for technical support, account management, etc.
- **Change Triage Logic**: Update the triage agent's instructions to handle more complex routing.
- **Customize Handoff**: Use the `handoff()` function to add callbacks, input filters, or tool descriptions.
- **Logging**: Print or log which agent handled each query for auditing.

## 🔍 How It Works

1. **User Query**: The user submits a question.
2. **Triage Agent**: Analyzes the query and decides if it's about billing or refunds.
3. **Handoff**: Delegates the query to the appropriate specialized agent.
4. **Specialized Agent**: Handles the query and returns a response.
5. **Result**: The final output is printed.

## 🐛 Troubleshooting

- **Agent Not Delegating**: Check the triage agent's instructions for clarity.
- **No Output**: Ensure your OpenAI API key and model are set in your environment variables.
- **Wrong Agent Handling Query**: Refine the triage agent's instructions or add more explicit handoff logic.

## 📚 Best Practices

- **Keep Agent Instructions Clear**: The more specific the instructions, the better the routing.
- **Test with Different Queries**: Try various user questions to ensure correct handoff.
- **Use Explicit Handoffs for Customization**: The `handoff()` function allows for advanced features (callbacks, input filters, etc.).

---

*This example shows how to build a modular, scalable support system by routing queries to the right expert agent automatically.* 