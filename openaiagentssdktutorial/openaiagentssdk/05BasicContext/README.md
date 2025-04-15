# 🧠 Basic Context Example

## What This Code Does (Big Picture)
Imagine having a robot assistant that knows who you are and what you've bought before! This code creates an AI that can give personalized responses based on whether you're a free user or a premium user, and can look up your purchase history.

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
from dataclasses import dataclass
from typing import List, Optional
from agents import Agent, Runner, ModelSettings, function_tool
from agents import set_default_openai_key
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(api_key)
```
The AI assistant needs a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Creating User Information Classes 👤
```python
@dataclass
class Purchase:
    id: str
    name: str
    price: float
    date: str
    
@dataclass
class UserContext:
    uid: str
    is_pro_user: bool
    
    async def fetch_purchases(self) -> List[Purchase]:
        # This is a mock implementation
        # In a real application, this would fetch from a database
        if self.uid == "user123":
            return [
                Purchase(id="p1", name="Basic Plan", price=9.99, date="2023-01-15"),
                Purchase(id="p2", name="Premium Add-on", price=4.99, date="2023-02-20")
            ]
        return []
```
These classes store information about:
- What a user has purchased (name, price, date)
- Who the user is (ID, whether they're a pro user)
- How to look up the user's purchase history

## Step 3: Creating Tools That Use User Information 🛠️
```python
@function_tool
async def get_user_info(context: UserContext) -> str:
    """Get basic information about the current user"""
    user_type = "Pro" if context.is_pro_user else "Free"
    return f"User ID: {context.uid}, Account Type: {user_type}"

@function_tool
async def get_purchase_history(context: UserContext) -> str:
    """Get the purchase history for the current user"""
    purchases = await context.fetch_purchases()
    if not purchases:
        return "No purchase history found."
    
    result = "Purchase History:\n"
    for p in purchases:
        result += f"- {p.name}: ${p.price} on {p.date}\n"
    return result

@function_tool
async def get_personalized_greeting(context: UserContext) -> str:
    """Get a personalized greeting based on user status"""
    if context.is_pro_user:
        return "Welcome back to our premium service! We value your continued support."
    else:
        return "Welcome! Consider upgrading to our Pro plan for additional features."
```
These tools can:
- Look up information about the current user
- Check the user's purchase history
- Provide personalized greetings based on user status
- Use this information to provide personalized responses

## Step 4: Creating a Context-Aware AI Assistant 🤖
```python
user_context_agent = Agent[UserContext](
    name="User Context Agent",
    instructions="""
    You are a helpful assistant that provides personalized responses based on user context.
    Use the available tools to retrieve user information and provide tailored assistance.
    For pro users, offer more detailed information and premium suggestions.
    """,
    tools=[get_user_info, get_purchase_history, get_personalized_greeting],
)
```
This creates an AI assistant that:
- Knows how to use the UserContext information
- Can access user details and purchase history
- Gives different responses to free users vs. pro users

## Step 5: Running the Program with Different Users 🏃‍♂️
```python
async def main():    
    # Create sample users
    pro_user_context = UserContext(uid="user123", is_pro_user=True)
    free_user_context = UserContext(uid="user456", is_pro_user=False)
    
    # Example with pro user
    print("\n--- Pro User Example ---")
    result = await Runner.run(
        user_context_agent, 
        "Tell me about myself and my purchases", 
        context=pro_user_context
    )
    print("Response for Pro User:", result.final_output)
    
    # Example with free user
    print("\n--- Free User Example ---")
    result = await Runner.run(
        user_context_agent, 
        "Tell me about myself and my purchases", 
        context=free_user_context
    )
    print("Response for Free User:", result.final_output)
```
This runs the AI with two different users:
- A pro user who gets premium responses and has purchase history
- A free user who gets standard responses and no purchase history

## Final Summary 📌
✅ We created classes to store user information
✅ We created tools that can access this user information
✅ We created an AI that gives personalized responses based on user type
✅ We tested the AI with both free and pro users

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
   uv run basiccontext.py
   ```
4. Try adding more user information or creating new user types!

## What You'll Learn 🧠
- How to create and use context objects with dataclasses
- How to make async tools that access context information
- How to create agents that give personalized responses
- How to use generic typing with agents (Agent[UserContext])

Happy coding! 🎉 