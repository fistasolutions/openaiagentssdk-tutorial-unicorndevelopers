# 🤖 Agents As Tools Example

## What This Code Does (Big Picture)
Imagine having a team of robot specialists where one robot can ask another for help with specific tasks! This code shows how to create a system where a translation coordinator can delegate tasks to specialist translators that are experts in different languages.

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
from agents import Agent, Runner, set_default_openai_key
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
```
The AI assistants need a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Creating Specialist Translation Agents 🌍🌎🌏
```python
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
```
This creates three specialist translation agents:
- A Spanish translator who adapts content for Spanish-speaking audiences
- A French translator who adapts content for French-speaking audiences
- A German translator who adapts content for German-speaking audiences

Each translator is instructed to maintain the original tone and style while adapting cultural nuances appropriately.

## Step 3: Creating an Orchestrator Agent That Uses Translators as Tools 🎭
```python
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
```
This creates a translation coordinator that:
- Understands translation requests
- Identifies which language(s) the user wants
- Uses the appropriate translator for each language
- Presents translations clearly with labels
- Handles multiple translation requests
- Asks for clarification if needed

The key innovation here is using the `.as_tool()` method to convert each specialist agent into a tool that the orchestrator can use.

## Step 4: Creating an Advanced Multilingual Assistant 🌐
```python
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
```
This creates an even more advanced assistant that:
- Has multiple capabilities beyond just translation
- Can answer questions, summarize information, and provide recommendations
- Uses the orchestrator agent as a tool for translation requests
- Responds directly for non-translation requests

This demonstrates nested agent-as-tool usage, where the advanced assistant uses the orchestrator, which in turn uses the specialist translators.

## Step 5: Running Basic Translation Examples 🏃‍♂️
```python
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
```
This tests the orchestrator with two different translation requests:
1. A simple request to translate a greeting to Spanish
2. A more complex request to translate a phrase to multiple languages

## Step 6: Testing Nested Agents 🪆
```python
print("\n=== Nested Agents Example ===")
print("Query: I need to write an email in Spanish to my colleague about our project deadline.")

result = await Runner.run(advanced_assistant, input="I need to write an email in Spanish to my colleague about our project deadline.")
print("\nResponse:")
print(result.final_output)
```
This tests the advanced assistant with a request that requires:
1. Understanding the user needs to write an email
2. Recognizing it needs to be in Spanish
3. Using the translation orchestrator tool
4. The orchestrator then using the Spanish translator tool

This demonstrates how agents can be nested to handle complex, multi-step tasks.

## Step 7: Creating an Interactive Mode 💬
```python
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
```
This creates an interactive mode where:
- You can make any request to the advanced assistant
- The assistant decides whether to use its translation capabilities
- You see the assistant's responses
- You can type "exit" to quit

## Final Summary 📌
✅ We created specialist agents for Spanish, French, and German translation
✅ We created an orchestrator agent that uses translators as tools
✅ We created an advanced assistant that uses the orchestrator as a tool
✅ We demonstrated nested agent-as-tool usage for complex tasks
✅ We tested the system with different types of translation requests
✅ We created an interactive mode for making any request

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
   uv run agentsastools.py
   ```
4. Try asking for translations in different languages or making other requests!

## What You'll Learn 🧠
- How to create specialist agents for specific tasks
- How to convert agents into tools using the `.as_tool()` method
- How to create orchestrator agents that delegate to specialists
- How to nest agents for handling complex, multi-step tasks
- How to build a hierarchical system of agents with different responsibilities
- How to combine translation capabilities with other assistant features

Happy coding! 🎉 