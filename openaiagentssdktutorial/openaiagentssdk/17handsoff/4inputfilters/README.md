# 🧹 Handoff Input Filters Example

## 📋 Overview
This example demonstrates how to use **input filters** with agent handoff. Input filters allow you to modify or sanitize the input before it is passed to the handoff agent, ensuring only relevant information is forwarded.

## 🎯 Key Concepts

### **Input Filters**
- **Purpose**: Clean or transform input before handoff.
- **Preprocessing**: Remove tool calls, sensitive data, or irrelevant information.
- **Custom Filters**: Write your own filter functions for advanced scenarios.

## 📁 Code Walkthrough

```python
import os
from dotenv import load_dotenv
from agents import Agent, Runner, handoff, set_default_openai_key
from agents.extensions import handoff_filters

# Load API keys
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
openai_model = os.environ.get("OPENAI_MODEL")

# FAQ Agent (receives handoff)
faq_agent = Agent(
    name="FAQ Agent",
    instructions="You answer frequently asked questions clearly and concisely.",
    model=openai_model
)

# Handoff with input filter to remove tool calls
faq_handoff = handoff(
    agent=faq_agent,
    input_filter=handoff_filters.remove_all_tools
)

# Main agent (performs handoff)
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You handle general customer queries. "
        "If the user is asking a standard FAQ, use the FAQ handoff tool to pass it along."
    ),
    model=openai_model,
    handoffs=[faq_handoff],
)

# Run a sample query
result = Runner.run_sync(triage_agent, "What is your refund policy?")

# Output
print("🤖 Final Output:\n", result.final_output)
```

## 🚀 How to Run

```bash
uv run 4inputfilters.py
```

## 🛠️ Customization Ideas

- **Write Custom Filters**: Create your own input filter functions for special cases.
- **Chain Filters**: Apply multiple filters in sequence.
- **Sanitize Sensitive Data**: Remove or mask personal information before handoff.
- **Preprocess for Specific Agents**: Tailor input for the needs of each handoff agent.

## 🔍 How It Works

1. **User Query**: The user submits a question.
2. **Triage Agent**: Decides if the query is a FAQ.
3. **Input Filter**: Cleans the input before passing to the FAQ agent.
4. **FAQ Agent**: Answers the question concisely.
5. **Result**: The final output is printed.

## 🐛 Troubleshooting

- **Filter Not Working**: Ensure the filter function is passed to `handoff()`.
- **No Output**: Verify your OpenAI API key and model are set.
- **Unexpected Input**: Test with different queries to ensure filtering works as expected.

## 📚 Best Practices

- **Use Filters for Data Hygiene**: Prevent unwanted or unsafe data from reaching agents.
- **Test Filters Thoroughly**: Try various input scenarios.
- **Document Filter Logic**: Make it clear what each filter does.

---

*This example shows how to use input filters to control and clean the data passed to handoff agents, improving reliability and safety.* 