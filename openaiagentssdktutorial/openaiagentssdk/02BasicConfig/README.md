# ⚙️ Basic Configuration Example

## What This Code Does (Big Picture)
Imagine giving your robot friend a special weather tool so it can check the weather anywhere and then write poems about it! This code creates an AI assistant that can look up weather information and create haikus based on what it finds.

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
from agents import Agent, Runner, ModelSettings, function_tool
from dotenv import load_dotenv
from agents import set_default_openai_key
import asyncio
import os

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(api_key)
```
The AI assistant needs a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Creating a Weather Tool 🌦️
```python
@function_tool
def get_weather(city: str) -> str:
    """Get the current weather in a given city"""
    return f"The weather in {city} is sunny with a temperature of 70 degrees."
```
This creates a special tool that:
- Takes a city name as input
- Returns weather information for that city
- (In a real app, this would connect to a weather service)

## Step 3: Creating a Weather Poet AI 🤖
```python
weather_haiku_agent = Agent(
    name="Weather Haiku Agent",
    instructions="You create haikus about the weather. Use the weather tool to get information.",
    tools=[get_weather],
)
```
This creates an AI assistant that:
- Has a special job: writing haikus about weather
- Knows how to use the weather tool we created
- Will check the weather before writing its poems

## Step 4: Running the Program 🏃‍♂️
```python
async def main():
    result = await Runner.run(weather_haiku_agent, "What is the weather in Tokyo?")
    print(result.final_output)
```
When someone asks about Tokyo's weather:
1. The AI uses the weather tool to check Tokyo's weather
2. It creates a haiku based on the sunny, 70-degree weather
3. It returns the haiku as its response

## Final Step: Starting Everything 🚀
```python
if __name__ == "__main__":
    asyncio.run(main())
```
This starts the whole program and runs the example.

## Final Summary 📌
✅ We created a weather tool that can check weather in any city
✅ We created an AI that knows how to use this tool
✅ We instructed the AI to write haikus about the weather
✅ We asked about Tokyo's weather and got a weather-inspired haiku

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
   uv run basicconfig.py
   ```
4. Try changing the city or adding more weather conditions!

## What You'll Learn 🧠
- How to create function tools for your agents
- How to configure agents with specific instructions
- How to run agents asynchronously
- How to use the OpenAI API with the agents SDK

Happy coding! 🎉 