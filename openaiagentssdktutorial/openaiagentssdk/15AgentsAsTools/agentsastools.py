from agents import Agent, Runner, set_default_openai_key
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)

# Create specialized translation agents
spanish_agent = Agent(
    name="Spanish Translator",
    instructions="""
    You are a professional Spanish translator.
    Translate the user's message to Spanish accurately and naturally.
    Maintain the tone and style of the original message.
    If there are cultural nuances, adapt them appropriately for Spanish-speaking audiences.
    """,
)

french_agent = Agent(
    name="French Translator",
    instructions="""
    You are a professional French translator.
    Translate the user's message to French accurately and naturally.
    Maintain the tone and style of the original message.
    If there are cultural nuances, adapt them appropriately for French-speaking audiences.
    """,
)

german_agent = Agent(
    name="German Translator",
    instructions="""
    You are a professional German translator.
    Translate the user's message to German accurately and naturally.
    Maintain the tone and style of the original message.
    If there are cultural nuances, adapt them appropriately for German-speaking audiences.
    """,
)

# Create an orchestrator agent that uses the translation agents as tools
orchestrator_agent = Agent(
    name="Translation Orchestrator",
    instructions="""
    You are a multilingual translation coordinator. You help users translate text into different languages.
    
    When a user requests a translation:
    1. Identify which language(s) they want the text translated to
    2. Use the appropriate translation tool for each language
    3. Present the translations clearly, labeling each one
    4. If asked for multiple translations, provide all of them
    5. If the target language is unclear, ask for clarification
    
    Be helpful and efficient in coordinating translations.
    """,
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
        german_agent.as_tool(
            tool_name="translate_to_german",
            tool_description="Translate the user's message to German",
        ),
    ],
)

# Create a more complex agent that combines translation with other capabilities
advanced_assistant = Agent(
    name="Multilingual Assistant",
    instructions="""
    You are a helpful assistant that can communicate in multiple languages and help with various tasks.
    
    Your capabilities include:
    1. Answering questions in the user's preferred language
    2. Translating content between languages
    3. Summarizing information
    4. Providing recommendations
    
    Use the appropriate tools based on the user's request. If they ask for translations,
    use the translation tools. For other requests, respond directly.
    
    Always be helpful, accurate, and respectful.
    """,
    tools=[
        orchestrator_agent.as_tool(
            tool_name="translate_content",
            tool_description="Translate content between different languages",
        ),
    ],
)

async def main():
    
    print("=== Basic Translation Example ===")
    print("Query: Say 'Hello, how are you?' in Spanish.")
    
    result = await Runner.run(orchestrator_agent, input="Say 'Hello, how are you?' in Spanish.")
    print("\nResponse:")
    print(result.final_output)
    
    print("\n=== Multiple Languages Example ===")
    print("Query: Translate 'I love artificial intelligence' to Spanish, French, and German.")
    
    result = await Runner.run(orchestrator_agent, input="Translate 'I love artificial intelligence' to Spanish, French, and German.")
    print("\nResponse:")
    print(result.final_output)
    
    print("\n=== Nested Agents Example ===")
    print("Query: I need to write an email in Spanish to my colleague about our project deadline.")
    
    result = await Runner.run(advanced_assistant, input="I need to write an email in Spanish to my colleague about our project deadline.")
    print("\nResponse:")
    print(result.final_output)
    
    # Interactive mode
    print("\n=== Interactive Translation Mode ===")
    print("Type 'exit' to quit")
    
    while True:
        user_input = input("\nYour request: ")
        if user_input.lower() == 'exit':
            break
        
        print("Processing...")
        result = await Runner.run(advanced_assistant, input=user_input)
        print("\nResponse:")
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main()) 