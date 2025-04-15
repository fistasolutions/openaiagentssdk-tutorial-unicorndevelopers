# 🧬 Basic Cloning Example

## What This Code Does (Big Picture)
Imagine creating different versions of your robot friend - one that talks like a pirate, another that speaks like a robot, and a third that writes poetry! This code shows how to create variations of an AI assistant with different personalities and abilities.

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
from agents import Agent, Runner, ModelSettings, function_tool
from dotenv import load_dotenv
import asyncio
import os
from agents import set_default_openai_key

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(api_key)
```
The AI assistants need a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Creating an Emoji Translation Tool 🔧
```python
@function_tool
def translate_to_emoji(text: str) -> str:
    """Translate text to emoji (mock implementation)"""
    emoji_map = {
        "happy": "😊",
        "sad": "😢",
        "love": "❤️",
        "cool": "😎",
        "food": "🍔",
        "drink": "🍹",
        "travel": "✈️",
        "music": "🎵",
        "book": "📚",
        "computer": "💻"
    }
    
    result = []
    for word in text.lower().split():
        # Remove punctuation
        word = word.strip(".,!?;:")
        if word in emoji_map:
            result.append(emoji_map[word])
        else:
            result.append(word)
    
    return " ".join(result)
```
This tool converts certain words to emoji symbols, which we'll use for one of our special agents.

## Step 3: Creating the Base Agent 🤖
```python
base_agent = Agent(
    name="Base Agent",
    instructions="You are a helpful assistant that responds to user queries in a professional manner.",
    model="gpt-3.5-turbo",  # You can change this to any model you have access to
)
```
This creates our standard, professional AI assistant that will be the starting point for all our variations.

## Step 4: Creating a Pirate-Speaking Agent 🏴‍☠️
```python
pirate_agent = base_agent.clone(
    name="Pirate Agent",
    instructions="""
    You are a pirate-speaking assistant! Always respond in pirate speak.
    Use phrases like "Arr!", "Ahoy matey!", "Shiver me timbers!", and "Yo ho ho!".
    Refer to yourself as a salty sea dog and the user as a landlubber.
    Keep your pirate persona consistent throughout the conversation.
    """,
)
```
This creates a copy of our base agent but changes its instructions to make it talk like a pirate.

## Step 5: Creating a Robot-Speaking Agent 🤖
```python
robot_agent = base_agent.clone(
    name="Robot Agent",
    instructions="""
    You are a robot assistant. Respond in a robotic, mechanical manner.
    Use phrases like "PROCESSING QUERY", "EXECUTING RESPONSE", and "INFORMATION RETRIEVED".
    Avoid using contractions and speak in a formal, logical, and precise manner.
    Occasionally add beep and boop sounds or references to your circuits and programming.
    """,
)
```
This creates another copy of our base agent but makes it talk like a robot with mechanical phrases and formal language.

## Step 6: Creating a Poetic Agent 📝
```python
poet_agent = base_agent.clone(
    name="Poet Agent",
    instructions="""
    You are a poetic assistant who responds in verse.
    Use rhyming patterns, metaphors, and beautiful language.
    Structure your responses as short poems or verses.
    Be lyrical and expressive while still answering the user's question.
    """,
)
```
This creates a third copy that responds with poetic language, rhymes, and verses.

## Step 7: Creating an Emoji Pirate Agent 🏴‍☠️😊
```python
emoji_pirate_agent = pirate_agent.clone(
    name="Emoji Pirate Agent",
    instructions="""
    You are a pirate-speaking assistant who loves emojis! Always respond in pirate speak.
    Use phrases like "Arr!", "Ahoy matey!", "Shiver me timbers!", and "Yo ho ho!".
    Refer to yourself as a salty sea dog and the user as a landlubber.
    
    Additionally, use the translate_to_emoji tool to add relevant emojis to your responses.
    Keep your pirate persona consistent throughout the conversation.
    """,
    tools=[translate_to_emoji],
)
```
This creates a special agent that:
- Is based on the pirate agent (not the base agent)
- Adds the emoji translation tool
- Combines pirate speech with emoji usage

## Step 8: Running the Program with Different Agents 🏃‍♂️
```python
async def main():
    runner = Runner()
    
    # Test query to demonstrate different agent personalities
    test_query = "Tell me about the weather today"
    
    # Test each agent with the same query
    print("\n--- Base Agent Response ---")
    result = await runner.run(base_agent, test_query)
    print(result.final_output)
    
    print("\n--- Pirate Agent Response ---")
    result = await runner.run(pirate_agent, test_query)
    print(result.final_output)
    
    print("\n--- Robot Agent Response ---")
    result = await runner.run(robot_agent, test_query)
    print(result.final_output)
    
    print("\n--- Poet Agent Response ---")
    result = await runner.run(poet_agent, test_query)
    print(result.final_output)
    
    print("\n--- Emoji Pirate Agent Response ---")
    result = await runner.run(emoji_pirate_agent, test_query)
    print(result.final_output)
```
This tests all our different agents with the same question about the weather to see how they respond differently based on their unique personalities.

## Step 9: Interactive Mode with Agent Switching 🎮
```python
    # Interactive mode
    print("\n--- Interactive Mode ---")
    print("Available agents: base, pirate, robot, poet, emoji-pirate")
    print("Type 'exit' to quit or 'switch [agent]' to change agents")
    
    current_agent = base_agent
    current_agent_name = "base"
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
        elif user_input.lower().startswith('switch '):
            agent_choice = user_input.lower().split('switch ')[1].strip()
            if agent_choice == 'base':
                current_agent = base_agent
                current_agent_name = "base"
            elif agent_choice == 'pirate':
                current_agent = pirate_agent
                current_agent_name = "pirate"
            elif agent_choice == 'robot':
                current_agent = robot_agent
                current_agent_name = "robot"
            elif agent_choice == 'poet':
                current_agent = poet_agent
                current_agent_name = "poet"
            elif agent_choice == 'emoji-pirate':
                current_agent = emoji_pirate_agent
                current_agent_name = "emoji-pirate"
            else:
                print(f"Unknown agent: {agent_choice}")
                continue
            
            print(f"Switched to {current_agent_name} agent")
            continue
        
        response = await runner.run(current_agent, user_input)
        print(f"\n{current_agent_name.capitalize()} Agent: {response.final_output}")
```
This adds an interactive mode where you can:
- Chat with any of the agents
- Switch between different agent personalities using the 'switch' command
- Experience how each agent responds differently to the same questions
- Type 'exit' to quit

## Final Summary 📌
✅ We created a base agent with professional behavior
✅ We cloned it to create agents with different personalities (pirate, robot, poet)
✅ We created a special tool for emoji translation
✅ We created an agent that combines pirate speech with emoji usage
✅ We tested all agents with the same question to see their different styles
✅ We added an interactive mode to chat with and switch between agents

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
   uv run basiccloning.py
   ```
4. Try the interactive mode and switch between different agent personalities!

## What You'll Learn 🧠
- How to clone agents to create variations with different personalities
- How to add tools to cloned agents
- How to build on existing agents to create new ones
- How to create an interactive system with multiple agent personalities
- How to maintain the base functionality while changing the communication style

Happy coding! 🎉 