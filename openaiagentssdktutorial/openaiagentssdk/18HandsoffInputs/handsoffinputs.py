from pydantic import BaseModel, Field
from typing import Optional, List
import asyncio
import json

from agents import Agent, handoff, RunContextWrapper, Runner, set_default_openai_key
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)

# Define structured data models for different handoff scenarios
class EscalationData(BaseModel):
    reason: str = Field(..., description="The reason for escalation")
    priority: str = Field(..., description="Priority level (low, medium, high, urgent)")
    attempted_solutions: List[str] = Field(default_factory=list, description="Solutions already attempted")

class CustomerData(BaseModel):
    name: str = Field(..., description="Customer's name")
    account_id: Optional[str] = Field(None, description="Customer's account ID if available")
    issue_category: str = Field(..., description="Category of the customer's issue")
    is_premium: bool = Field(description="Whether the customer has premium status")

class TechnicalIssueData(BaseModel):
    product_name: str = Field(..., description="Name of the product with the issue")
    error_code: Optional[str] = Field(None, description="Error code if applicable")
    system_info: Optional[str] = Field(None, description="Customer's system information")
    steps_to_reproduce: List[str] = Field(default_factory=list, description="Steps to reproduce the issue")

# Define handoff callback functions that use the structured data
async def on_escalation_handoff(ctx: RunContextWrapper[None], input_data: EscalationData):
    print("\n[SYSTEM] Escalation process initiated")
    print(f"[SYSTEM] Reason for escalation: {input_data.reason}")
    print(f"[SYSTEM] Priority level: {input_data.priority}")
    if input_data.attempted_solutions:
        print("[SYSTEM] Solutions already attempted:")
        for i, solution in enumerate(input_data.attempted_solutions, 1):
            print(f"[SYSTEM]   {i}. {solution}")
    print("[SYSTEM] Notifying supervisor and preparing case file")

async def on_premium_handoff(ctx: RunContextWrapper[None], input_data: CustomerData):
    print("\n[SYSTEM] Premium customer service handoff initiated")
    print(f"[SYSTEM] Customer name: {input_data.name}")
    if input_data.account_id:
        print(f"[SYSTEM] Account ID: {input_data.account_id}")
    print(f"[SYSTEM] Issue category: {input_data.issue_category}")
    print(f"[SYSTEM] Premium status: {'Yes' if input_data.is_premium else 'No'}")
    print("[SYSTEM] Loading customer history and preferences")
    print("[SYSTEM] Preparing personalized greeting and expedited service options")

async def on_technical_handoff(ctx: RunContextWrapper[None], input_data: TechnicalIssueData):
    print("\n[SYSTEM] Technical support handoff initiated")
    print(f"[SYSTEM] Product: {input_data.product_name}")
    if input_data.error_code:
        print(f"[SYSTEM] Error code: {input_data.error_code}")
    if input_data.system_info:
        print(f"[SYSTEM] System information: {input_data.system_info}")
    if input_data.steps_to_reproduce:
        print("[SYSTEM] Steps to reproduce:")
        for i, step in enumerate(input_data.steps_to_reproduce, 1):
            print(f"[SYSTEM]   {i}. {step}")
    print("[SYSTEM] Searching knowledge base for known solutions")
    print("[SYSTEM] Preparing diagnostic tools")

# Create specialized agents
escalation_agent = Agent(
    name="Escalation Specialist",
    instructions="""
    You are an escalation specialist who handles complex or high-priority issues.
    
    Your responsibilities:
    1. Address customer concerns that couldn't be resolved by the first-line support
    2. Handle complaints and sensitive situations
    3. Provide solutions for complex problems
    4. Coordinate with other departments when necessary
    5. Ensure customer satisfaction for difficult cases
    
    Be empathetic but professional, and focus on finding effective solutions quickly.
    """,
)

premium_agent = Agent(
    name="Premium Customer Agent",
    instructions="""
    You are a premium customer service agent who provides enhanced support to our valued premium customers.
    
    Your responsibilities:
    1. Provide personalized, white-glove service to premium customers
    2. Offer expedited solutions and special accommodations
    3. Proactively address potential issues
    4. Ensure premium customers feel valued and appreciated
    5. Go above and beyond standard service protocols
    
    Be exceptionally courteous, attentive, and solution-oriented.
    """,
)

technical_agent = Agent(
    name="Technical Specialist",
    instructions="""
    You are a technical specialist with deep expertise in our products and services.
    
    Your responsibilities:
    1. Solve complex technical issues that require specialized knowledge
    2. Provide detailed technical explanations and guidance
    3. Troubleshoot difficult problems with systematic approaches
    4. Recommend advanced solutions and workarounds
    5. Document technical issues for product improvement
    
    Be thorough, precise, and methodical in your approach to technical problems.
    """,
)

# Create handoff objects with structured input types
escalation_handoff = handoff(
    agent=escalation_agent,
    on_handoff=on_escalation_handoff,
    input_type=EscalationData,
    tool_name_override="escalate_to_specialist",
    tool_description_override="Escalate the issue to a specialist for handling complex or high-priority cases.",
)

premium_handoff = handoff(
    agent=premium_agent,
    on_handoff=on_premium_handoff,
    input_type=CustomerData,
    tool_name_override="transfer_to_premium_service",
    tool_description_override="Transfer the customer to our premium service team for enhanced support.",
)

technical_handoff = handoff(
    agent=technical_agent,
    on_handoff=on_technical_handoff,
    input_type=TechnicalIssueData,
    tool_name_override="connect_with_technical_specialist",
    tool_description_override="Connect the customer with a technical specialist for advanced troubleshooting.",
)

# Create a main agent that can hand off to specialized agents with structured data
main_agent = Agent(
    name="Customer Service Agent",
    instructions="""
    You are the primary customer service agent. Your role is to:
    
    1. Assist customers with general inquiries and simple issues
    2. Identify when a case needs to be handled by a specialist
    3. Collect relevant information before transferring to a specialist
    4. Use the appropriate handoff tool with complete information:
    
       - For complex or high-priority issues, use escalate_to_specialist with:
         * reason: Clear description of why escalation is needed
         * priority: Appropriate level (low, medium, high, urgent)
         * attempted_solutions: List of solutions you've already tried
    
       - For premium customers, use transfer_to_premium_service with:
         * name: Customer's name
         * account_id: Customer's account ID if available
         * issue_category: Category of their issue
         * is_premium: Set to true for premium customers
    
       - For technical issues, use connect_with_technical_specialist with:
         * product_name: Name of the product with the issue
         * error_code: Error code if mentioned
         * system_info: Customer's system information if provided
         * steps_to_reproduce: Steps to reproduce the issue
    
    Always collect as much relevant information as possible before handoff.
    """,
    handoffs=[
        escalation_handoff,
        premium_handoff,
        technical_handoff,
    ],
)

async def main():
    
    # Example customer inquiries for different scenarios
    escalation_inquiry = "I've been trying to resolve an issue with my account for three days and nobody has helped me. I'm extremely frustrated and considering canceling my service. This is unacceptable!"
    
    premium_inquiry = "Hello, I'm Sarah Johnson, a premium member since 2018. My account number is PRE-12345. I need assistance with updating my payment method."
    
    technical_inquiry = "My XYZ-3000 printer is showing error code E-503 when I try to print. I'm using Windows 11, and I've already tried restarting the printer and checking the ink levels. The error appears after I click print and the printer makes a clicking sound."
    
    # Test the main agent with different inquiries
    print("=== Escalation Example ===")
    print(f"Customer: {escalation_inquiry}")
    
    result = await Runner.run(main_agent, input=escalation_inquiry)
    print("\nFinal Response:")
    print(result.final_output)
    
    print("\n=== Premium Customer Example ===")
    print(f"Customer: {premium_inquiry}")
    
    result = await Runner.run(main_agent, input=premium_inquiry)
    print("\nFinal Response:")
    print(result.final_output)
    
    print("\n=== Technical Issue Example ===")
    print(f"Customer: {technical_inquiry}")
    
    result = await Runner.run(main_agent, input=technical_inquiry)
    print("\nFinal Response:")
    print(result.final_output)
    
    # Interactive mode
    print("\n=== Interactive Customer Service Mode ===")
    print("Type 'exit' to quit")
    
    while True:
        user_input = input("\nYour inquiry: ")
        if user_input.lower() == 'exit':
            break
        
        print("Processing...")
        result = await Runner.run(main_agent, input=user_input)
        print("\nFinal Response:")
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main()) 