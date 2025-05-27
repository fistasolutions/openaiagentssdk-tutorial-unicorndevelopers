# Sales Agent Example

This example demonstrates how to create an AI agent specialized in sales and customer interactions.

## Overview

The `3salesagent.py` file shows how to create an agent that can handle sales-related queries and customer interactions. This agent is designed to assist with product information, sales pitches, and customer service.

## Key Components

1. **Sales-Focused Agent**:
   - Named "Sales Agent"
   - Configured for sales and customer interaction
   - Uses GPT-4 model for sophisticated responses

2. **Interactive Sales Interface**:
   - Takes customer queries through input
   - Demonstrates real-time sales interaction

## Code Explanation

```python
agent = Agent(
    name="Sales Agent",
    instructions="You are a sales agent. You are given a product and a customer. You need to sell the product to the customer.",
    model=openai_model
)

# Interactive sales interaction
user_prompt = input("Enter your prompt: ")
result = Runner.run_sync(agent, user_prompt)
```

## How to Run

1. Make sure your OpenAI API key is in the `.env` file
2. Run the script:
   ```bash
   uv run 3salesagent.py
   ```
3. Enter your sales-related query when prompted

## Expected Output

The agent will respond with sales-oriented responses, including:
- Product information
- Sales pitches
- Customer service responses
- Follow-up questions

## Learning Points

- Creating sales-focused agents
- Handling customer interactions
- Real-time sales communication
- Dynamic response generation

## Use Cases

This agent can be used for:
- Product demonstrations
- Customer inquiries
- Sales pitch generation
- Customer service support

## Next Steps

After understanding this example, you can explore:
- Adding product-specific tools
- Implementing sales scripts
- Adding customer context
- Creating multi-stage sales processes
- Integrating with CRM systems 