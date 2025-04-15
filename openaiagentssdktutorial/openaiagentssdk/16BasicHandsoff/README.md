# 🔄 Basic Handoffs Example

## What This Code Does (Big Picture)
Imagine a customer service department where the receptionist directs customers to the right specialist! This code shows how to create a customer service system where a triage agent can hand off conversations to specialized agents for billing, refunds, or technical support.

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
from agents import Agent, Runner, handoff, set_default_openai_key
import asyncio
from dotenv import load_dotenv
import os
from agents import set_default_openai_key
load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
```
The AI assistants need a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Creating Specialized Customer Service Agents 👨‍💼👩‍💼👨‍💻
```python
# Create specialized agents for different customer service functions
billing_agent = Agent(
    name="Billing Agent",
    instructions="""
    You are a specialized billing support agent. You help customers with:
    
    1. Understanding their bill and charges
    2. Explaining billing policies
    3. Handling payment issues
    4. Setting up payment plans
    5. Updating billing information
    
    Be professional, clear, and helpful when addressing billing concerns.
    If the customer needs a refund, politely explain that you'll transfer them to the refund department.
    """,
    handoff_description="Transfer to this agent for billing-related questions, payment issues, or bill explanations."
)

refund_agent = Agent(
    name="Refund Agent",
    instructions="""
    You are a specialized refund support agent. You help customers with:
    
    1. Processing refund requests
    2. Explaining refund policies and timeframes
    3. Checking refund status
    4. Resolving refund issues
    5. Providing refund documentation
    
    Be empathetic and solution-oriented when handling refund requests.
    Clearly explain the refund process and expected timelines.
    """,
    handoff_description="Transfer to this agent for refund requests, refund status checks, or refund policy questions."
)

technical_agent = Agent(
    name="Technical Support Agent",
    instructions="""
    You are a specialized technical support agent. You help customers with:
    
    1. Troubleshooting product issues
    2. Providing setup assistance
    3. Resolving error messages
    4. Guiding through software updates
    5. Explaining technical features
    
    Be patient and thorough when providing technical assistance.
    Use clear, step-by-step instructions that are easy to follow.
    """,
    handoff_description="Transfer to this agent for technical issues, troubleshooting, or product functionality questions."
)
```
This creates three specialized customer service agents:
- A billing agent who handles payment issues and billing questions
- A refund agent who processes refund requests and explains policies
- A technical support agent who troubleshoots product issues

Each agent has a `handoff_description` that explains when they should receive handoffs.

## Step 3: Creating a Triage Agent That Can Hand Off to Specialists 🧑‍💼
```python
# Create a triage agent that can hand off to specialized agents
triage_agent = Agent(
    name="Customer Service Triage",
    instructions="""
    You are the initial customer service agent who triages customer inquiries.
    
    Your responsibilities:
    1. Greet the customer and identify their issue
    2. Handle simple general inquiries directly
    3. For specialized issues, transfer to the appropriate specialized agent:
       - Billing Agent: For billing questions, payment issues, or bill explanations
       - Refund Agent: For refund requests, refund status, or refund policy questions
       - Technical Support: For technical issues, troubleshooting, or product functionality
    
    Before transferring, briefly explain to the customer why you're transferring them
    and what the specialized agent will help them with.
    """,
    handoffs=[
        billing_agent,
        handoff(refund_agent),  # Using the handoff function (equivalent to just passing the agent)
        technical_agent,
    ],
)
```
This creates a triage agent that:
- Greets customers and identifies their issues
- Handles simple inquiries directly
- Transfers specialized issues to the appropriate agent
- Explains the transfer to the customer

Note that there are two ways to specify handoffs:
1. Directly including the agent in the handoffs list
2. Using the `handoff()` function (both approaches are equivalent)

## Step 4: Testing with Different Customer Inquiries 🧪
```python
# Example customer inquiries for different scenarios
billing_inquiry = "I'm confused about the charges on my last bill. There's an extra $20 fee I don't recognize."
refund_inquiry = "I want to request a refund for my recent purchase. The product doesn't work as advertised."
technical_inquiry = "My software keeps crashing whenever I try to save my work. How can I fix this?"
general_inquiry = "What are your business hours?"

# Test the triage agent with different inquiries
print("=== Billing Inquiry Example ===")
print(f"Customer: {billing_inquiry}")

result = await Runner.run(triage_agent, input=billing_inquiry)
print("\nResponse:")
print(result.final_output)
# Let's print the available attributes to debug
print(f"Available attributes: {dir(result)}")
# For now, just print the agent name we started with
print(f"Started with: {triage_agent.name}")
```
This tests the system with different types of customer inquiries:
1. A billing question about an unexpected charge
2. A refund request for a product
3. A technical issue with software crashing
4. A general question about business hours

For each inquiry, we run the triage agent and see how it responds.

## Step 5: Testing All Inquiry Types 🔄
```python
print("\n=== Refund Inquiry Example ===")
print(f"Customer: {refund_inquiry}")

result = await Runner.run(triage_agent, input=refund_inquiry)
print("\nResponse:")
print(result.final_output)
print(f"Started with: {triage_agent.name}")

print("\n=== Technical Inquiry Example ===")
print(f"Customer: {technical_inquiry}")

result = await Runner.run(triage_agent, input=technical_inquiry)
print("\nResponse:")
print(result.final_output)
print(f"Started with: {triage_agent.name}")

print("\n=== General Inquiry Example ===")
print(f"Customer: {general_inquiry}")

result = await Runner.run(triage_agent, input=general_inquiry)
print("\nResponse:")
print(result.final_output)
print(f"Started with: {triage_agent.name}")
```
This continues testing with the remaining inquiry types to see how the triage agent handles each one.

## Step 6: Creating an Interactive Customer Service Mode 💬
```python
# Interactive mode
print("\n=== Interactive Customer Service Mode ===")
print("Type 'exit' to quit")

while True:
    user_input = input("\nYour inquiry: ")
    if user_input.lower() == 'exit':
        break
    
    print("Processing...")
    result = await Runner.run(triage_agent, input=user_input)
    print("\nResponse:")
    print(result.final_output)
    print(f"Started with: {triage_agent.name}")
```
This creates an interactive mode where:
- You can type any customer service inquiry
- The triage agent will either handle it or hand it off
- You can see the response from the appropriate agent
- You can type "exit" to quit

## Final Summary 📌
✅ We created specialized agents for billing, refunds, and technical support
✅ We created a triage agent that can hand off to these specialists
✅ We tested the system with different types of customer inquiries
✅ We demonstrated two ways to specify handoffs
✅ We created an interactive customer service mode
✅ We tracked which agent handled each inquiry

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
   uv run basichandsoff.py
   ```
4. Try asking different types of customer service questions!

## What You'll Learn 🧠
- How to create specialized agents for different tasks
- How to set up handoff descriptions for agents
- How to create a triage agent that can hand off to specialists
- How to use the handoff() function (equivalent to direct agent inclusion)
- How to test a customer service system with different inquiry types
- How to build an interactive customer service interface

Happy coding! 🎉 