# 🔄 Basic Dynamic Instructions Example

## What This Code Does (Big Picture)
Imagine having an AI teacher that changes how it explains things based on whether you're a beginner, intermediate, or expert! This code creates an AI assistant that adjusts its language, detail level, and examples based on who it's talking to.

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
from agents import Agent, Runner, ModelSettings, function_tool, RunContextWrapper
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List
import asyncio
import os
import random
from agents import set_default_openai_key

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(api_key)
```
The AI assistant needs a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Creating a User Profile Class 👤
```python
@dataclass
class UserContext:
    name: str
    language: str
    interests: List[str]
    experience_level: str  # "beginner", "intermediate", or "expert"
```
This creates a template for storing information about users:
- Their name
- What language they speak
- What topics they're interested in
- Their experience level (beginner, intermediate, or expert)

## Step 3: Creating Dynamic Instructions Function 📝
```python
def dynamic_instructions(
    context: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    user = context.context
    
    # Base instructions that apply to everyone
    base_instructions = f"""
    The user's name is {user.name}. They prefer communication in {user.language}.
    Their experience level is: {user.experience_level}.
    Their interests include: {', '.join(user.interests)}.
    
    Tailor your responses to match their experience level and interests.
    """
    
    # Add specific instructions based on experience level
    if user.experience_level == "beginner":
        base_instructions += """
        Use simple explanations and avoid technical jargon.
        Provide step-by-step guidance and offer encouragement.
        """
    elif user.experience_level == "intermediate":
        base_instructions += """
        You can use some technical terms but explain complex concepts.
        Provide more detailed information and some advanced tips.
        """
    elif user.experience_level == "expert":
        base_instructions += """
        You can use technical language freely.
        Focus on advanced techniques and in-depth analysis.
        Be concise and precise in your explanations.
        """
    
    # Add language-specific instructions
    if user.language != "English":
        base_instructions += f"""
        Respond in {user.language} when possible.
        Use simple sentence structures for clarity.
        """
    
    return base_instructions
```
This function:
- Takes user information as input
- Creates custom instructions based on that user
- Adds different instructions for beginners, intermediates, and experts
- Includes language-specific instructions for non-English speakers
- Returns personalized instructions for the AI

## Step 4: Creating a Recommendation Tool 🛠️
```python
@function_tool
def get_recommendation(topic: str, experience_level: str) -> str:
    """Get a personalized recommendation on a specific topic based on experience level"""
    recommendations = {
        "programming": {
            "beginner": "Try starting with Python - it's beginner-friendly and versatile.",
            "intermediate": "Consider learning a framework like Django or Flask for web development.",
            "expert": "Explore advanced topics like concurrency, metaprogramming, or contributing to open source."
        },
        "cooking": {
            "beginner": "Start with simple recipes that have few ingredients and steps.",
            "intermediate": "Try experimenting with different cuisines and techniques.",
            "expert": "Consider molecular gastronomy or advanced baking techniques."
        },
        "photography": {
            "beginner": "Learn the basics of composition and lighting with your smartphone.",
            "intermediate": "Experiment with manual settings on a DSLR or mirrorless camera.",
            "expert": "Try specialized techniques like astrophotography or advanced post-processing."
        }
    }
    
    if topic.lower() in recommendations:
        if experience_level.lower() in recommendations[topic.lower()]:
            return recommendations[topic.lower()][experience_level.lower()]
    
    return f"I don't have specific recommendations for {topic} at {experience_level} level yet."
```
This tool provides different recommendations based on:
- What topic the user is interested in (programming, cooking, photography)
- What experience level they have (beginner, intermediate, expert)
- Returns appropriate recommendations or a fallback message if none exist

## Step 5: Creating the Dynamic AI Assistant 🤖
```python
dynamic_agent = Agent[UserContext](
    name="Personalized Assistant",
    instructions=dynamic_instructions,
    tools=[get_recommendation],
)
```
This creates an AI assistant that:
- Uses the dynamic_instructions function to get custom instructions
- Can access the user's profile information
- Uses the recommendation tool to give personalized suggestions

## Step 6: Running the Program with Different Users 🏃‍♂️
```python
async def main():
    # Create different user contexts
    beginner_user = UserContext(
        name="Alex",
        language="English",
        interests=["programming", "cooking", "hiking"],
        experience_level="beginner"
    )
    
    intermediate_user = UserContext(
        name="Maria",
        language="Spanish",
        interests=["photography", "travel", "music"],
        experience_level="intermediate"
    )
    
    expert_user = UserContext(
        name="Dr. Chen",
        language="English",
        interests=["quantum physics", "mathematics", "programming"],
        experience_level="expert"
    )
    
    runner = Runner()
    
    # Example queries
    general_query = "Can you help me learn something new?"
    specific_query = "I want to improve my programming skills"
    
    # Test with different user contexts
    print("\n--- Beginner User Example ---")
    result = await runner.run(dynamic_agent, general_query, context=beginner_user)
    print(f"Query: {general_query}")
    print(f"Response for {beginner_user.name} (Beginner):")
    print(result.final_output)
    
    print("\n--- Intermediate User Example ---")
    result = await runner.run(dynamic_agent, general_query, context=intermediate_user)
    print(f"Query: {general_query}")
    print(f"Response for {intermediate_user.name} (Intermediate):")
    print(result.final_output)
    
    print("\n--- Expert User Example ---")
    result = await runner.run(dynamic_agent, specific_query, context=expert_user)
    print(f"Query: {specific_query}")
    print(f"Response for {expert_user.name} (Expert):")
    print(result.final_output)
```
This tests the AI with different types of users:
1. A beginner who gets simple explanations without jargon
2. An intermediate user who gets some technical terms with explanations
3. An expert who gets advanced information with technical terms

## Step 7: Interactive Mode with User Switching 🎮
```python
    # Interactive mode with random user selection
    print("\n--- Interactive Mode ---")
    print("Type 'exit' to quit")
    
    users = [beginner_user, intermediate_user, expert_user]
    current_user = random.choice(users)
    print(f"Current user: {current_user.name} ({current_user.experience_level})")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'switch user':
            current_user = random.choice(users)
            print(f"Switched to user: {current_user.name} ({current_user.experience_level})")
            continue
        
        response = await runner.run(dynamic_agent, user_input, context=current_user)
        print(f"\nAgent to {current_user.name}: {response.final_output}")
```
This adds an interactive mode where you can:
- Chat with the AI as different users
- Type 'switch user' to randomly change to a different user profile
- See how the AI adapts its responses to each user
- Type 'exit' to quit

## Final Summary 📌
✅ We created a way to store information about different users
✅ We created a function that generates custom instructions based on the user
✅ We created an AI that adapts its responses to match the user's level and language
✅ We created a recommendation tool that gives personalized suggestions
✅ We tested the AI with beginners, intermediates, and experts
✅ We added an interactive mode with user switching

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
   uv run basicdynamicinstructions.py
   ```
4. Try the interactive mode and switch between different user profiles!

## What You'll Learn 🧠
- How to create dynamic instructions that change based on context
- How to store and use user information with dataclasses
- How to personalize AI responses for different experience levels
- How to handle multiple languages in your AI assistant
- How to use conditional logic to modify agent behavior
- How to build an interactive system with user profile switching

Happy coding! 🎉 