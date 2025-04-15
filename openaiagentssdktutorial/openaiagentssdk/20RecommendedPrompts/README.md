# 📝 Recommended Prompts Example

## What This Code Does (Big Picture)
Imagine having a template that helps your robot friend understand exactly how to respond in the most effective way! This code shows how to use OpenAI's recommended prompt prefix to improve agent performance, making your AI assistants more helpful, harmless, and honest in their responses.

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
from agents import Agent, Runner, set_default_openai_key
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
```
The AI assistants need a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Creating Agents with the Recommended Prompt Prefix 🤖
```python
# Create an agent using the recommended prompt prefix
billing_agent = Agent(
    name="Billing Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    You are a billing specialist for a software company. Your responsibilities include:
    
    1. Answering questions about subscription plans and pricing
    2. Helping customers understand their invoices and charges
    3. Processing refund requests according to company policy
    4. Assisting with payment method updates and billing information changes
    5. Explaining billing cycles and renewal processes
    
    When helping customers:
    - Be clear and transparent about all charges and policies
    - Provide specific details about pricing when asked
    - Explain complex billing concepts in simple terms
    - Show empathy when customers are confused or frustrated
    - Follow company policies while finding solutions for customers
    
    Our refund policy allows full refunds within 30 days of purchase, and partial refunds up to 60 days.
    """,
)

# Create another agent using the recommended prompt prefix
support_agent = Agent(
    name="Technical Support Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    You are a technical support specialist for a software company. Your responsibilities include:
    
    1. Troubleshooting software issues and error messages
    2. Guiding customers through installation and setup processes
    3. Explaining how to use product features and functionality
    4. Providing workarounds for known issues
    5. Collecting information for bug reports when necessary
    
    When helping customers:
    - Ask clarifying questions to understand the exact issue
    - Provide step-by-step instructions that are easy to follow
    - Avoid technical jargon unless necessary
    - Confirm that the solution worked before concluding
    - Document any new issues for the development team
    
    Our software is compatible with Windows 10/11, macOS 10.14+, and major Linux distributions.
    """,
)
```
This creates two agents that use the recommended prompt prefix:
- A billing agent who handles payment and refund questions
- A technical support agent who helps with software issues

The key innovation is using `RECOMMENDED_PROMPT_PREFIX` at the beginning of the instructions, which adds OpenAI's recommended guidelines for better agent behavior.

## Step 3: Creating a Standard Agent Without the Prefix 🤖
```python
# Create a standard agent without the recommended prompt prefix for comparison
standard_agent = Agent(
    name="Standard Agent",
    instructions="""
    You are a customer service agent for a software company. Your responsibilities include:
    
    1. Answering general questions about our products and services
    2. Directing customers to the appropriate department for specialized help
    3. Providing information about company policies and procedures
    4. Assisting with account management and basic inquiries
    5. Collecting customer feedback and suggestions
    
    When helping customers:
    - Be friendly and professional
    - Provide accurate information
    - Escalate complex issues to specialists
    - Follow up to ensure customer satisfaction
    - Document customer interactions
    """,
)
```
This creates a standard agent without the recommended prompt prefix for comparison purposes. This will help us see the difference the prefix makes in agent responses.

## Step 4: Creating a Response Comparison Function 🔍
```python
# Function to compare responses between agents
async def compare_responses(query):
    print(f"\n=== Query: {query} ===\n")
    
    print("--- Response with Recommended Prompt Prefix ---")
    result = await Runner.run(billing_agent, input=query)
    print(result.final_output)
    
    print("\n--- Response with Standard Prompt ---")
    result = await Runner.run(standard_agent, input=query)
    print(result.final_output)
```
This function:
- Takes a query as input
- Runs it on both a prefix-enhanced agent and a standard agent
- Displays the responses side by side for comparison

This helps us see how the recommended prompt prefix affects the quality and style of responses.

## Step 5: Displaying the Recommended Prompt Prefix 📋
```python
# Print the recommended prompt prefix for reference
print("=== Recommended Prompt Prefix ===")
print(RECOMMENDED_PROMPT_PREFIX)
```
This displays the actual content of the recommended prompt prefix so we can see what guidelines it contains.

## Step 6: Testing with Different Types of Queries 🧪
```python
# Example queries to test with different agents
billing_query = "I was charged twice for my subscription this month. Can I get a refund?"
technical_query = "I'm having trouble installing your software on my Mac. It keeps showing an error during installation."
general_query = "What are your business hours and how can I contact customer support?"

# Compare responses between agents with and without the recommended prompt prefix
await compare_responses(billing_query)

# Test the technical support agent with a relevant query
print("\n=== Technical Support Query ===")
print(f"Query: {technical_query}")

result = await Runner.run(support_agent, input=technical_query)
print("\nResponse:")
print(result.final_output)

# Test the standard agent with a general query
print("\n=== General Query ===")
print(f"Query: {general_query}")

result = await Runner.run(standard_agent, input=general_query)
print("\nResponse:")
print(result.final_output)
```
This tests the agents with different types of queries:
1. A billing query about a double charge and refund
2. A technical query about installation issues
3. A general query about business hours

It shows how each agent handles queries in its domain, and how the recommended prompt prefix affects responses.

## Step 7: Creating an Interactive Mode with Agent Selection 💬
```python
# Interactive mode
print("\n=== Interactive Mode ===")
print("Choose an agent to interact with:")
print("1. Billing Agent (with recommended prompt)")
print("2. Technical Support Agent (with recommended prompt)")
print("3. Standard Agent (without recommended prompt)")
print("Type 'exit' to quit")

while True:
    agent_choice = input("\nSelect agent (1-3): ")
    if agent_choice.lower() == 'exit':
        break
    
    try:
        agent_num = int(agent_choice)
        if agent_num == 1:
            selected_agent = billing_agent
            print("Using Billing Agent")
        elif agent_num == 2:
            selected_agent = support_agent
            print("Using Technical Support Agent")
        elif agent_num == 3:
            selected_agent = standard_agent
            print("Using Standard Agent")
        else:
            print("Invalid choice. Please select 1-3.")
            continue
    except ValueError:
        print("Invalid input. Please enter a number 1-3.")
        continue
    
    user_query = input("Your query: ")
    if user_query.lower() == 'exit':
        break
    
    print("Processing...")
    result = await Runner.run(selected_agent, input=user_query)
    print("\nResponse:")
    print(result.final_output)
```
This creates an interactive mode where:
- You can choose which agent to interact with
- You can compare agents with and without the recommended prompt
- You can ask any question to see how different agents respond
- You can type "exit" to quit

## Final Summary 📌
✅ We imported the recommended prompt prefix from the agents library
✅ We created agents that use this prefix for better responses
✅ We created a standard agent without the prefix for comparison
✅ We compared responses between agents with and without the prefix
✅ We tested different types of queries with specialized agents
✅ We created an interactive mode with agent selection

## Try It Yourself! 🚀
1. Install the required packages:
   ```
   uv add openai-agents python-dotenv
   ```
2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Run the program:
   ```
   uv run recommendedprompts.py
   ```
4. Try comparing responses with and without the recommended prompt prefix!

## What You'll Learn 🧠
- How to use OpenAI's recommended prompt prefix
- How this prefix improves agent responses
- How to create specialized agents for different domains
- How to compare responses between different agent configurations
- How to build an interactive system with agent selection

Happy coding! 🎉 