# 🔄 Customizing Handoffs Example

## What This Code Does (Big Picture)
Imagine having a customer service system where you can customize exactly how customers are transferred between departments! This code shows how to create enhanced handoffs with custom callbacks, tool name overrides, and detailed descriptions to create a more professional customer service experience.

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
from agents import Agent, handoff, RunContextWrapper, Runner, set_default_openai_key
import asyncio
from dotenv import load_dotenv
import os
from typing import Any, Dict, Optional

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
```
The AI assistants need a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Creating Custom Handoff Callbacks 📞
```python
# Define custom handoff callbacks
def on_handoff_to_sales(ctx: RunContextWrapper[None]):
    print("\n[SYSTEM] Handoff to Sales Agent initiated")
    print("[SYSTEM] Logging customer information for sales follow-up")
    print("[SYSTEM] Preparing sales materials based on customer inquiry")

def on_handoff_to_support(ctx: RunContextWrapper[None]):
    print("\n[SYSTEM] Handoff to Support Agent initiated")
    print("[SYSTEM] Retrieving customer support history")
    print("[SYSTEM] Preparing troubleshooting resources")

def on_handoff_to_specialist(ctx: RunContextWrapper[None]):
    print("\n[SYSTEM] Handoff to Product Specialist initiated")
    print("[SYSTEM] Loading product documentation and specifications")
    print("[SYSTEM] Checking inventory and availability")
```
These functions:
- Are triggered when a handoff occurs
- Receive a context object with information about the handoff
- Perform special actions like logging information or preparing resources
- Display system messages to show what's happening behind the scenes

## Step 3: Creating Specialized Agents 👨‍💼👩‍💻👨‍🔧
```python
# Create specialized agents
sales_agent = Agent(
    name="Sales Agent",
    instructions="""
    You are a specialized sales agent. Your role is to:
    
    1. Help customers find the right products for their needs
    2. Provide pricing information and available discounts
    3. Explain product features and benefits
    4. Assist with placing orders
    5. Answer questions about shipping and delivery
    
    Be enthusiastic, helpful, and knowledgeable about our product offerings.
    Focus on understanding customer needs and recommending appropriate solutions.
    """,
)

support_agent = Agent(
    name="Support Agent",
    instructions="""
    You are a specialized technical support agent. Your role is to:
    
    1. Help customers troubleshoot issues with their products
    2. Provide step-by-step guidance for resolving problems
    3. Explain how to use product features
    4. Assist with software updates and installations
    5. Document issues for further follow-up if needed
    
    Be patient, clear, and thorough in your explanations.
    Focus on resolving the customer's issue efficiently and effectively.
    """,
)

product_specialist = Agent(
    name="Product Specialist",
    instructions="""
    You are a specialized product expert. Your role is to:
    
    1. Provide in-depth information about specific products
    2. Compare different product models and their features
    3. Explain technical specifications and compatibility
    4. Offer advice on product accessories and add-ons
    5. Share best practices for product use and maintenance
    
    Be detailed, accurate, and passionate about our products.
    Focus on helping customers understand the full capabilities of our offerings.
    """,
)
```
This creates three specialized agents:
- A sales agent who helps with product selection and purchasing
- A support agent who helps troubleshoot technical issues
- A product specialist who provides detailed product information

## Step 4: Creating Enhanced Handoff Objects 🔄
```python
# Create custom handoff objects with callbacks and overrides
sales_handoff = handoff(
    agent=sales_agent,
    on_handoff=on_handoff_to_sales,
    tool_name_override="transfer_to_sales_team",
    tool_description_override="Transfer the customer to our sales team for assistance with product selection, pricing, and purchasing.",
)

support_handoff = handoff(
    agent=support_agent,
    on_handoff=on_handoff_to_support,
    tool_name_override="connect_with_technical_support",
    tool_description_override="Connect the customer with our technical support team for help with troubleshooting and product issues.",
)

specialist_handoff = handoff(
    agent=product_specialist,
    on_handoff=on_handoff_to_specialist,
    tool_name_override="consult_product_specialist",
    tool_description_override="Arrange a consultation with a product specialist for detailed product information and expert advice.",
)
```
This creates enhanced handoff objects that:
- Connect to the specialized agents
- Include custom callback functions to run when handoffs occur
- Use professional tool names instead of default agent names
- Provide detailed descriptions of what each handoff does

## Step 5: Creating a Main Agent with Enhanced Handoffs 🤖
```python
# Create a main agent that can hand off to specialized agents
main_agent = Agent(
    name="Customer Service Agent",
    instructions="""
    You are the primary customer service agent. Your role is to:
    
    1. Greet customers and understand their initial needs
    2. Handle general inquiries and simple questions
    3. Direct customers to the appropriate specialized agent when needed:
       - Sales Team: For product selection, pricing, and purchasing
       - Technical Support: For troubleshooting and product issues
       - Product Specialist: For detailed product information and expert advice
    
    Before transferring a customer, briefly explain why you're connecting them with a specialist
    and what they can expect from the handoff.
    """,
    handoffs=[
        sales_handoff,
        support_handoff,
        specialist_handoff,
    ],
)
```
This creates a main customer service agent that:
- Handles general inquiries
- Uses our enhanced handoff objects to transfer customers
- Explains the handoff process to customers

## Step 6: Testing with Different Customer Inquiries 🧪
```python
# Example customer inquiries for different scenarios
sales_inquiry = "I'm interested in buying a new laptop for video editing. What do you recommend?"
support_inquiry = "My printer keeps showing an error code E-04. How can I fix this?"
specialist_inquiry = "Can you tell me about the differences between your premium camera models?"
general_inquiry = "What are your store hours this weekend?"

# Test the main agent with different inquiries
print("=== Sales Inquiry Example ===")
print(f"Customer: {sales_inquiry}")

result = await Runner.run(main_agent, input=sales_inquiry)
print("\nResponse:")
print(result.final_output)
```
This tests the system with different types of customer inquiries:
1. A sales inquiry about buying a laptop
2. A support inquiry about a printer error
3. A specialist inquiry about camera models
4. A general inquiry about store hours

## Step 7: Testing All Inquiry Types 🔄
```python
print("\n=== Support Inquiry Example ===")
print(f"Customer: {support_inquiry}")

result = await Runner.run(main_agent, input=support_inquiry)
print("\nResponse:")
print(result.final_output)

print("\n=== Specialist Inquiry Example ===")
print(f"Customer: {specialist_inquiry}")

result = await Runner.run(main_agent, input=specialist_inquiry)
print("\nResponse:")
print(result.final_output)

print("\n=== General Inquiry Example ===")
print(f"Customer: {general_inquiry}")

result = await Runner.run(main_agent, input=general_inquiry)
print("\nResponse:")
print(result.final_output)
```
This continues testing with the remaining inquiry types to see how the main agent handles each one and when it triggers the custom handoff callbacks.

## Step 8: Creating an Interactive Customer Service Mode 💬
```python
# Interactive mode
print("\n=== Interactive Customer Service Mode ===")
print("Type 'exit' to quit")

while True:
    user_input = input("\nYour inquiry: ")
    if user_input.lower() == 'exit':
        break
    
    print("Processing...")
    result = await Runner.run(main_agent, input=user_input)
    print("\nResponse:")
    print(result.final_output)
```
This creates an interactive mode where:
- You can type any customer service inquiry
- The main agent will handle it or hand it off to a specialist
- You'll see the system messages when handoffs occur
- You can type "exit" to quit

## Final Summary 📌
✅ We created custom callback functions for different handoff types
✅ We created specialized agents for sales, support, and product information
✅ We created enhanced handoff objects with callbacks and overrides
✅ We created a main agent that uses these enhanced handoffs
✅ We tested the system with different types of customer inquiries
✅ We created an interactive customer service mode

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
   uv run customizinghandsoff.py
   ```
4. Try asking different types of customer service questions!

## What You'll Learn 🧠
- How to create custom callback functions for handoffs
- How to override tool names and descriptions for handoffs
- How to create a professional customer service system
- How to perform special actions when handoffs occur
- How to build a complete customer service experience with specialized agents

Happy coding! 🎉 