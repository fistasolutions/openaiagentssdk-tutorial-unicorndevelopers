# 👤 Local Context Example

## What This Code Does (Big Picture)
Imagine having an AI assistant that knows your preferences, subscription status, and purchase history! This code shows how to create agents that can access and update user-specific information, providing personalized responses based on each user's profile and subscription tier.

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
import asyncio
from dataclasses import dataclass
from typing import List, Optional, Dict
import json

from agentswithopenai import Agent, RunContextWrapper, Runner, function_tool, set_default_openai_key
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
```
The AI assistant needs a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Creating a User Information Data Class 📋
```python
# Define a data class to hold user information
@dataclass
class UserInfo:
    name: str
    uid: int
    email: Optional[str] = None
    subscription_tier: str = "free"
    preferences: Dict[str, str] = None
    purchase_history: List[Dict] = None

    def __post_init__(self):
        if self.preferences is None:
            self.preferences = {}
        if self.purchase_history is None:
            self.purchase_history = []
```
This creates a structured data class for user information that includes:
- Basic profile information (name, ID, email)
- Subscription tier (free, basic, premium)
- User preferences (stored as key-value pairs)
- Purchase history (list of purchases with details)

The `__post_init__` method ensures that preferences and purchase history are initialized as empty collections if not provided.

## Step 3: Creating Function Tools That Use Context 🛠️
```python
# Define function tools that use the context
@function_tool
async def fetch_user_profile(wrapper: RunContextWrapper[UserInfo]) -> str:
    """Fetch the user's profile information."""
    user = wrapper.context
    return f"""
User Profile:
- Name: {user.name}
- User ID: {user.uid}
- Email: {user.email or 'Not provided'}
- Subscription: {user.subscription_tier}
"""

@function_tool
async def fetch_user_preferences(wrapper: RunContextWrapper[UserInfo]) -> str:
    """Fetch the user's preferences."""
    user = wrapper.context
    if not user.preferences:
        return "No preferences have been set."
    
    result = "User Preferences:\n"
    for key, value in user.preferences.items():
        result += f"- {key}: {value}\n"
    return result

@function_tool
async def fetch_purchase_history(wrapper: RunContextWrapper[UserInfo]) -> str:
    """Fetch the user's purchase history."""
    user = wrapper.context
    if not user.purchase_history:
        return "No purchase history available."
    
    result = "Purchase History:\n"
    for i, purchase in enumerate(user.purchase_history, 1):
        result += f"{i}. {purchase.get('item', 'Unknown item')} - ${purchase.get('price', 0):.2f} on {purchase.get('date', 'Unknown date')}\n"
    return result

@function_tool
async def update_preference(wrapper: RunContextWrapper[UserInfo], key: str, value: str) -> str:
    """Update a user preference."""
    user = wrapper.context
    user.preferences[key] = value
    return f"Updated preference: {key} = {value}"

@function_tool
async def get_subscription_features(wrapper: RunContextWrapper[UserInfo]) -> str:
    """Get the features available for the user's subscription tier."""
    user = wrapper.context
    
    features = {
        "free": [
            "Basic content access",
            "Limited searches per day",
            "Standard support"
        ],
        "basic": [
            "Full content access",
            "Unlimited searches",
            "Priority email support",
            "Bookmark feature"
        ],
        "premium": [
            "All Basic features",
            "Exclusive premium content",
            "Advanced analytics",
            "24/7 priority support",
            "Offline access",
            "No advertisements"
        ]
    }
    
    tier = user.subscription_tier.lower()
    if tier not in features:
        return f"Unknown subscription tier: {tier}"
    
    result = f"Features for {tier.capitalize()} tier:\n"
    for feature in features[tier]:
        result += f"- {feature}\n"
    return result
```
These functions create tools that:
- Access the user's profile information
- Retrieve the user's preferences
- Show the user's purchase history
- Update the user's preferences
- List features available for the user's subscription tier

Each tool receives a `RunContextWrapper` that contains the user information, allowing the tool to access and modify user data.

## Step 4: Creating an Agent with User Context 🤖
```python
# Create an agent with UserInfo context
user_agent = Agent[UserInfo](
    name="User Context Agent",
    instructions="""
    You are a personalized assistant that provides user-specific information and services.
    
    Use the available tools to:
    - Fetch and display user profile information
    - Show user preferences
    - Display purchase history
    - Update user preferences
    - Provide information about subscription features
    
    Tailor your responses based on the user's subscription tier:
    - For free users: Be helpful but mention premium features they could access by upgrading
    - For basic users: Provide full service and occasionally highlight premium features
    - For premium users: Provide VIP service and acknowledge their premium status
    
    Always be polite, helpful, and personalized in your interactions.
    """,
    tools=[
        fetch_user_profile,
        fetch_user_preferences,
        fetch_purchase_history,
        update_preference,
        get_subscription_features
    ],
)
```
This creates an agent that:
- Is typed with `UserInfo` to specify the context type
- Has access to all the user-specific tools
- Is instructed to provide personalized service based on subscription tier
- Can access and modify user data through the context

## Step 5: Creating Sample Users for Demonstration 👥
```python
# Function to create sample users for demonstration
def create_sample_users() -> Dict[int, UserInfo]:
    users = {}
    
    # Free tier user
    users[1] = UserInfo(
        name="Alex Johnson",
        uid=1,
        email="alex@example.com",
        subscription_tier="free",
        preferences={
            "theme": "light",
            "notifications": "email"
        },
        purchase_history=[]
    )
    
    # Basic tier user
    users[2] = UserInfo(
        name="Sam Rodriguez",
        uid=2,
        email="sam@example.com",
        subscription_tier="basic",
        preferences={
            "theme": "dark",
            "notifications": "push",
            "language": "Spanish"
        },
        purchase_history=[
            {"item": "Basic Subscription", "price": 9.99, "date": "2023-01-15"},
            {"item": "E-book: Beginner's Guide", "price": 4.99, "date": "2023-02-10"}
        ]
    )
    
    # Premium tier user
    users[3] = UserInfo(
        name="Taylor Kim",
        uid=3,
        email="taylor@example.com",
        subscription_tier="premium",
        preferences={
            "theme": "auto",
            "notifications": "all",
            "language": "English",
            "content_filter": "none"
        },
        purchase_history=[
            {"item": "Premium Subscription", "price": 19.99, "date": "2022-11-05"},
            {"item": "Premium Course Bundle", "price": 49.99, "date": "2022-12-20"},
            {"item": "1-on-1 Consultation", "price": 99.99, "date": "2023-03-15"}
        ]
    )
    
    return users
```
This function creates three sample users with different subscription tiers:
- A free tier user with basic preferences and no purchase history
- A basic tier user with some preferences and a few purchases
- A premium tier user with extensive preferences and purchase history

This allows us to demonstrate how the agent provides different experiences based on the user's tier.

## Step 6: Creating a Function to Interact with Users 💬
```python
# Function to interact with a user
async def interact_with_user(user: UserInfo, query: str) -> UserInfo:
    print(f"\n=== Interaction with {user.name} ({user.subscription_tier} tier) ===")
    print(f"User query: {query}")
    
    result = await Runner.run(user_agent, query, context=user)
    
    print(f"Response: {result.final_output}")
    
    # Return the potentially modified user object
    return user
```
This function:
- Takes a user object and a query
- Runs the agent with the user as context
- Displays the agent's response
- Returns the potentially modified user object (if preferences were updated)

The key innovation is passing the user object as the `context` parameter to `Runner.run()`.

## Step 7: Running Interactions for Each User 🏃‍♂️
```python
async def main():
    # Create sample users
    users = create_sample_users()
    
    # Sample queries for different users
    queries = [
        "What's in my user profile?",
        "What are my current preferences?",
        "Show me my purchase history.",
        "What features do I have with my subscription?",
        "Update my theme preference to 'blue'.",
        "What are all my preferences now?"
    ]
    
    # Run interactions for each user with each query
    for uid, user in users.items():
        for query in queries:
            user = await interact_with_user(user, query)
```
This code:
- Creates the sample users
- Defines a set of sample queries to demonstrate different capabilities
- Runs each query for each user to show how responses differ by subscription tier
- Updates the user object after each interaction to maintain state

## Step 8: Creating an Interactive Mode 💬
```python
# Interactive mode
print("\n=== Interactive Mode ===")
print("Select a user to interact with:")
for uid, user in users.items():
    print(f"{uid}: {user.name} ({user.subscription_tier} tier)")

while True:
    try:
        uid_input = input("\nEnter user ID (or 'exit' to quit): ")
        if uid_input.lower() == 'exit':
            break
        
        uid = int(uid_input)
        if uid not in users:
            print(f"User ID {uid} not found. Please try again.")
            continue
        
        query = input("Enter your query: ")
        if query.lower() == 'exit':
            break
        
        users[uid] = await interact_with_user(users[uid], query)
        
    except ValueError:
        print("Please enter a valid user ID.")
    except Exception as e:
        print(f"Error: {e}")
```
This creates an interactive mode where:
- You can select which user to interact with
- You can enter custom queries for that user
- The user's state is maintained between interactions
- You can type "exit" to quit

## Final Summary 📌
✅ We created a data class to store user information
✅ We created function tools that access and modify user context
✅ We created an agent that uses user context for personalized responses
✅ We created sample users with different subscription tiers
✅ We demonstrated how responses differ based on user context
✅ We created an interactive mode for custom interactions

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
   uv run localcontext.py
   ```
4. Try interacting with different users and see how the responses change!

## What You'll Learn 🧠
- How to create typed agents with context
- How to access context in function tools
- How to maintain state between interactions
- How to provide personalized responses based on user data
- How to build a system that handles different user tiers

Happy coding! 🎉 