from agents import Agent, Runner, handoff, set_default_openai_key
import asyncio
from dotenv import load_dotenv
import os
from agents import set_default_openai_key
load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)

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

async def main():
    
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

if __name__ == "__main__":
    asyncio.run(main()) 