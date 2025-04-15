from agents import Agent, handoff, Runner, set_default_openai_key
from agents.extensions import handoff_filters
import asyncio
from dotenv import load_dotenv
import os
from typing import List, Dict, Any

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
# Create a custom input filter that adds context about the customer
def add_customer_context(input_text: str) -> str:
    return f"""
Customer context: Gold tier member since 2019, prefers email communication, has purchased premium plan.

Customer inquiry: {input_text}
"""

# Create a custom wrapper for remove_all_tools for demonstration purposes
def demo_remove_all_tools(input_text: str) -> str:
    # This is a simplified version just for demonstration
    return "This would remove all tool references from: " + input_text

# Create a custom input filter that adds system instructions
def add_system_instructions(input_text: str) -> str:
    return f"""
SYSTEM INSTRUCTIONS:
- Be concise and direct in your responses
- Use bullet points for lists
- Avoid technical jargon unless necessary
- Always confirm understanding before proceeding

USER QUERY:
{input_text}
"""

# Create a custom input filter that sanitizes sensitive information
def sanitize_sensitive_info(input_text: str) -> str:
    # In a real implementation, this would use regex or more sophisticated methods
    # to identify and redact sensitive information
    sanitized = input_text
    sanitized = sanitized.replace("credit card", "[PAYMENT METHOD]")
    sanitized = sanitized.replace("SSN", "[REDACTED ID]")
    sanitized = sanitized.replace("password", "[CREDENTIALS]")
    sanitized = sanitized.replace("account number", "[ACCOUNT ID]")
    
    # Add a note about sanitization if changes were made
    if sanitized != input_text:
        sanitized += "\n\n[Note: Some sensitive information has been redacted for security purposes.]"
    
    return sanitized

# Create specialized agents for different purposes
faq_agent = Agent(
    name="FAQ Agent",
    instructions="""
    You are an FAQ specialist who provides clear, concise answers to common questions.
    
    Your responsibilities:
    1. Provide accurate information about our products and services
    2. Answer frequently asked questions efficiently
    3. Direct users to relevant resources when appropriate
    4. Keep responses brief and to the point
    
    Stick to answering common questions and avoid lengthy explanations unless necessary.
    """,
)

technical_agent = Agent(
    name="Technical Agent",
    instructions="""
    You are a technical support specialist who helps users with complex technical issues.
    
    Your responsibilities:
    1. Troubleshoot technical problems step by step
    2. Provide clear instructions for resolving issues
    3. Explain technical concepts in accessible language
    4. Recommend best practices for using our products
    
    Be thorough but clear in your explanations, and focus on practical solutions.
    """,
)

billing_agent = Agent(
    name="Billing Agent",
    instructions="""
    You are a billing specialist who handles financial and account-related inquiries.
    
    Your responsibilities:
    1. Address questions about billing and payments
    2. Explain pricing plans and subscription options
    3. Help with account management issues
    4. Provide information about refunds and credits
    
    Be precise and transparent about financial matters, and maintain customer privacy.
    """,
)

# Create handoff objects with different input filters
faq_handoff = handoff(
    agent=faq_agent,
    input_filter=handoff_filters.remove_all_tools,  # This is fine as it will be used correctly in handoff
    tool_name_override="ask_faq_specialist",
    tool_description_override="Transfer to an FAQ specialist for answers to common questions.",
)

technical_handoff = handoff(
    agent=technical_agent,
    input_filter=add_system_instructions,  # Add system instructions to the input
    tool_name_override="get_technical_support",
    tool_description_override="Transfer to a technical specialist for help with technical issues.",
)

billing_handoff = handoff(
    agent=billing_agent,
    input_filter=lambda text: sanitize_sensitive_info(add_customer_context(text)),  # Chain multiple filters
    tool_name_override="contact_billing_department",
    tool_description_override="Transfer to the billing department for help with account and payment issues.",
)

# Create a main agent that can hand off to specialized agents with filtered inputs
main_agent = Agent(
    name="Customer Service Agent",
    instructions="""
    You are the primary customer service agent. Your role is to:
    
    1. Greet customers and understand their initial needs
    2. Handle simple inquiries directly
    3. Direct customers to the appropriate specialized agent when needed:
       - FAQ Specialist: For common questions about our products and services
       - Technical Support: For help with technical issues and troubleshooting
       - Billing Department: For questions about billing, payments, and accounts
    
    Before transferring a customer, briefly explain why you're connecting them with a specialist
    and what they can expect from the handoff.
    
    You have access to customer tools that should not be shared with other agents.
    """,
    handoffs=[
        faq_handoff,
        technical_handoff,
        billing_handoff,
    ],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "access_customer_database",
                "description": "Access the customer database to retrieve customer information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "customer_id": {
                            "type": "string",
                            "description": "The customer's ID"
                        }
                    },
                    "required": ["customer_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_customer_record",
                "description": "Update the customer's record in the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "customer_id": {
                            "type": "string",
                            "description": "The customer's ID"
                        },
                        "field": {
                            "type": "string",
                            "description": "The field to update"
                        },
                        "value": {
                            "type": "string",
                            "description": "The new value for the field"
                        }
                    },
                    "required": ["customer_id", "field", "value"]
                }
            }
        }
    ]
)

# Function to demonstrate the effect of input filters
def demonstrate_filters():
    sample_input = "I need help with my account number 12345-6789. My credit card isn't working and I forgot my password."
    
    print("=== Input Filter Demonstration ===\n")
    print(f"Original input: \"{sample_input}\"\n")
    
    print("After demo_remove_all_tools (simulating handoff_filters.remove_all_tools):")
    print(f"\"{demo_remove_all_tools(sample_input)}\"\n")
    
    print("After add_customer_context:")
    print(f"\"{add_customer_context(sample_input)}\"\n")
    
    print("After add_system_instructions:")
    print(f"\"{add_system_instructions(sample_input)}\"\n")
    
    print("After sanitize_sensitive_info:")
    print(f"\"{sanitize_sensitive_info(sample_input)}\"\n")
    
    print("After chaining filters (sanitize + add_customer_context):")
    print(f"\"{sanitize_sensitive_info(add_customer_context(sample_input))}\"\n")

async def main():
    
    # Demonstrate the effect of different input filters
    demonstrate_filters()
    
    # Example customer inquiries for different scenarios
    faq_inquiry = "What are the differences between your Basic, Premium, and Enterprise plans?"
    technical_inquiry = "I'm having trouble connecting my device to Wi-Fi. I've tried restarting it but it still won't connect."
    billing_inquiry = "I was charged twice for my subscription this month. My account number is ABC-12345 and I paid with my credit card ending in 7890."
    
    # Test the main agent with different inquiries
    print("\n=== FAQ Inquiry Example ===")
    print(f"Customer: {faq_inquiry}")
    
    try:
        result = await Runner.run(main_agent, input=faq_inquiry)
        print("\nFinal Response:")
        print(result.final_output)
    except Exception as e:
        print(f"\nError: {e}")
        print("Skipping this example due to error.")
    
    print("\n=== Technical Inquiry Example ===")
    print(f"Customer: {technical_inquiry}")
    
    try:
        result = await Runner.run(main_agent, input=technical_inquiry)
        print("\nFinal Response:")
        print(result.final_output)
    except Exception as e:
        print(f"\nError: {e}")
        print("Skipping this example due to error.")
    
    print("\n=== Billing Inquiry Example ===")
    print(f"Customer: {billing_inquiry}")
    
    try:
        result = await Runner.run(main_agent, input=billing_inquiry)
        print("\nFinal Response:")
        print(result.final_output)
    except Exception as e:
        print(f"\nError: {e}")
        print("Skipping this example due to error.")
    
    # Interactive mode
    print("\n=== Interactive Customer Service Mode ===")
    print("Type 'exit' to quit")
    
    while True:
        user_input = input("\nYour inquiry: ")
        if user_input.lower() == 'exit':
            break
        
        print("Processing...")
        try:
            result = await Runner.run(main_agent, input=user_input)
            print("\nFinal Response:")
            print(result.final_output)
        except Exception as e:
            print(f"\nError: {e}")
            print("Could not process your inquiry due to an error.")

if __name__ == "__main__":
    asyncio.run(main()) 