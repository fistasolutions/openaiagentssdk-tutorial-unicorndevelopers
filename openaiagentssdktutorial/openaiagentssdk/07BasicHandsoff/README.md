# 🤝 Basic Handoffs Example

## What This Code Does (Big Picture)
Imagine a travel company with different specialists - one for booking flights, another for handling refunds. This code creates a smart receptionist AI that listens to your question and then connects you with the right specialist for help!

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
from agents import Agent, Runner, ModelSettings, function_tool
from dotenv import load_dotenv
import asyncio
import os
from typing import List, Optional
from agents import set_default_openai_key

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(api_key)
```
The AI assistants need a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Creating Tools for the Specialists 🛠️
```python
@function_tool
def get_available_flights(origin: str, destination: str, date: str) -> str:
    """Get available flights between two cities on a specific date"""
    # This is a mock implementation
    flights = [
        {"flight": "AA123", "departure": "08:00", "arrival": "10:30", "price": "$299"},
        {"flight": "DL456", "departure": "12:15", "arrival": "14:45", "price": "$329"},
        {"flight": "UA789", "departure": "16:30", "arrival": "19:00", "price": "$279"}
    ]
    result = f"Available flights from {origin} to {destination} on {date}:\n"   
    for flight in flights:
        result += f"{flight['flight']} - {flight['departure']} to {flight['arrival']} - ${flight['price']}\n"
    return result
```
This tool helps the booking specialist find available flights between cities on a specific date.

```python
@function_tool
def check_refund_eligibility(booking_reference: str) -> str:
    """Check if a flight booking is eligible for a refund"""
    # This is a mock implementation
    refund_policies = {
        "ABC123": {"eligible": True, "refund_amount": "$250", "reason": "Cancellation within 24 hours"},
        "DEF456": {"eligible": False, "reason": "Non-refundable fare"},
        "GHI789": {"eligible": True, "refund_amount": "$150", "reason": "Partial refund due to fare rules"}
    }
    if booking_reference in refund_policies:
        policy = refund_policies[booking_reference] 
        if policy["eligible"]:
            return f"Booking {booking_reference} is eligible for a refund of ${policy['refund_amount']}. The reason for the refund is: {policy['reason']}"
        else:
            return f"Booking {booking_reference} is not eligible for a refund. The reason is: {policy['reason']}"
    else:
        return f"Booking {booking_reference} is not found in our records."
```
This tool helps the refund specialist check if a booking can be refunded based on its reference number.

## Step 3: Creating Specialist Agents 👨‍💼👩‍💼
```python
booking_agent = Agent(
    name="Booking Agent",
    instructions="""
    You are a specialized booking agent for a travel company.
    Help users book flights by collecting necessary information:
    - Origin city
    - Destination city
    - Travel date
    - Number of passengers
    - Class of service (economy, business, first class)
    - Budget (if applicable)
    """,
    tools=[get_available_flights]
)

refund_agent = Agent(
    name="Refund Agent",
    instructions="""
    You are a specialized refund agent for a travel company.
    Help users with refund requests by:
    - Asking for their booking reference
    - Explaining refund policies
    - Checking eligibility using the check_refund_eligibility tool
    
    Be empathetic and clear about the refund process and timelines.
    """,
    tools=[check_refund_eligibility]
)
```
These create two specialist AIs:
- A booking agent who knows how to find flights and collect booking information
- A refund agent who knows how to handle refunds and check eligibility

## Step 4: Creating the Receptionist (Triage Agent) 🧑‍💼
```python
triage_agent = Agent(
    name="Travel Assistant",
    instructions="""
    You are a helpful travel assistant that can help with various travel-related questions.
    
    If the user asks about booking flights or needs help with a new reservation,
    hand off the conversation to the Booking Agent.
    
    If the user asks about refunds, cancellations, or reimbursements,
    hand off the conversation to the Refund Agent.
    
    For general travel questions, answer directly without handing off.
    Be friendly and helpful in all interactions.
    """,
    handoffs=[booking_agent, refund_agent]
)
```
This creates a receptionist AI that:
- Listens to all customer questions first
- Decides which specialist can best help
- Hands off the conversation to that specialist
- Handles general travel questions itself without handing off

## Step 5: Running the Program with Different Questions 🏃‍♂️
```python
async def main():
    # Example conversations
    booking_query = "I need to book a flight from New York to Los Angeles next week"
    refund_query = "I need to cancel my flight and get a refund. My booking reference is ABC123"
    general_query = "What's the weather like in Paris this time of year?"
    
    # Create a runner
    runner = Runner()
    
    # Simulate conversations with different queries
    print("\n--- Booking Query Example ---")
    response = await runner.run(triage_agent, booking_query)
    print(f"Initial Query: {booking_query}")
    print(f"Response: {response.final_output}")
    print(f"Handled by: {response.agent_name if hasattr(response, 'agent_name') else triage_agent.name}")
    
    print("\n--- Refund Query Example ---")
    response = await runner.run(triage_agent, refund_query)
    print(f"Initial Query: {refund_query}")
    print(f"Response: {response.final_output}")
    print(f"Handled by: {response.agent_name if hasattr(response, 'agent_name') else triage_agent.name}")
    
    print("\n--- General Query Example ---")
    response = await runner.run(triage_agent, general_query)
    print(f"Initial Query: {general_query}")
    print(f"Response: {response.final_output}")
    print(f"Handled by: {response.agent_name if hasattr(response, 'agent_name') else triage_agent.name}")
```
This tests the system with different questions:
1. A booking question (should go to the booking agent)
2. A refund question (should go to the refund agent)
3. A general question (triage agent handles it directly)

The code also tracks which agent handled each request.

## Step 6: Interactive Mode 🎮
```python
    # Optional: Interactive mode
    print("\n--- Interactive Mode ---")
    print("Type 'exit' to quit")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
        
        response = await runner.run(triage_agent, user_input)
        agent_name = response.agent_name if hasattr(response, 'agent_name') else triage_agent.name
        print(f"\nAgent ({agent_name}): {response.final_output}")
```
This adds an interactive mode where you can:
- Type your own travel questions
- See which agent responds
- Have a conversation with the system
- Type 'exit' to quit

## Final Summary 📌
✅ We created specialist agents for booking and refunds
✅ We gave each specialist the tools they need
✅ We created a triage agent that directs questions to specialists
✅ We tested the system with different types of questions
✅ We added an interactive mode for real conversations

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
4. Try asking different travel-related questions in the interactive mode!

## What You'll Learn 🧠
- How to create a system of cooperating agents
- How to set up handoffs between agents
- How to create specialist agents with specific tools
- How to track which agent handled a request
- How to build an interactive chat system with multiple agents

Happy coding! 🎉 