from agents import Agent,Runner, ModelSettings, function_tool
from dotenv import load_dotenv
import asyncio
import os
from agents import set_default_openai_key

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(api_key)

# Define some helper tools
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

# Create a base agent
base_agent = Agent(
    name="Base Agent",
    instructions="You are a helpful assistant that responds to user queries in a professional manner.",
    model="gpt-3.5-turbo",  # You can change this to any model you have access to
)

# Clone the base agent to create a pirate-speaking agent
pirate_agent = base_agent.clone(
    name="Pirate Agent",
    instructions="""
    You are a pirate-speaking assistant! Always respond in pirate speak.
    Use phrases like "Arr!", "Ahoy matey!", "Shiver me timbers!", and "Yo ho ho!".
    Refer to yourself as a salty sea dog and the user as a landlubber.
    Keep your pirate persona consistent throughout the conversation.
    """,
)

# Clone the base agent to create a robot-speaking agent
robot_agent = base_agent.clone(
    name="Robot Agent",
    instructions="""
    You are a robot assistant. Respond in a robotic, mechanical manner.
    Use phrases like "PROCESSING QUERY", "EXECUTING RESPONSE", and "INFORMATION RETRIEVED".
    Avoid using contractions and speak in a formal, logical, and precise manner.
    Occasionally add beep and boop sounds or references to your circuits and programming.
    """,
)

# Clone the base agent to create a poetic agent
poet_agent = base_agent.clone(
    name="Poet Agent",
    instructions="""
    You are a poetic assistant who responds in verse.
    Use rhyming patterns, metaphors, and beautiful language.
    Structure your responses as short poems or verses.
    Be lyrical and expressive while still answering the user's question.
    """,
)

# Clone the pirate agent but add emoji translation capability
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

if __name__ == "__main__":
    asyncio.run(main()) 