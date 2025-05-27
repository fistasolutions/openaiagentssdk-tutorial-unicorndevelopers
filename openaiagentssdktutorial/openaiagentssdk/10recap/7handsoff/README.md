# Handoffs Example

This example demonstrates how to implement agent handoffs, showing how to create a system where one agent can delegate tasks to specialized sub-agents.

## Overview

The `7handsoff.py` file shows how to:
1. Create specialized sub-agents
2. Implement a main routing agent
3. Handle task delegation
4. Manage multiple agent interactions

## Key Components

1. **Sub-Agents**:
   - Order Agent: Handles order-related queries
   - Support Agent: Handles support issues

2. **Main Agent**:
   - Routes queries to appropriate sub-agents
   - Manages handoff logic
   - Coordinates responses

## Code Explanation

```python
# Define specialized sub-agents
order_agent = Agent(
    name="Order Agent",
    instructions="You handle all questions about orders, shipping, and delivery.",
)

support_agent = Agent(
    name="Support Agent",
    instructions="You handle support-related issues like login problems or account settings.",
)

# Define the main routing agent
main_agent = Agent(
    name="Main Agent",
    instructions="""
        You help customers with general questions.
        If the question is about orders, hand it off to the Order Agent.
        If it's about support, hand it off to the Support Agent.
    """,
    handoffs=[order_agent, support_agent],
)
```

## How to Run

1. Ensure your OpenAI API key is in the `.env` file
2. Run the script:
   ```bash
   python 7handsoff.py
   ```

## Expected Output

The system will:
1. Receive a query
2. Route it to the appropriate agent
3. Return a specialized response

Example queries:
- "Where is my package?" → Order Agent
- "I can't log in to my account." → Support Agent

## Learning Points

- Creating agent hierarchies
- Implementing handoff logic
- Managing multiple agents
- Task delegation patterns
- Specialized agent creation

## Handoff Benefits

1. **Specialization**:
   - Each agent focuses on specific tasks
   - Better response quality
   - Clearer responsibility boundaries

2. **Scalability**:
   - Easy to add new specialized agents
   - Modular design
   - Maintainable code

## Next Steps

After understanding this example, you can explore:
- Adding more specialized agents
- Implementing complex routing logic
- Creating agent chains
- Adding handoff validation
- Implementing fallback mechanisms 