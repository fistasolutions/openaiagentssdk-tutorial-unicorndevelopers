from agents import Agent, Runner, ModelSettings, function_tool
from dotenv import load_dotenv
from agents import set_default_openai_key
import os

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_model = os.environ.get("OPENAI_MODEL")
set_default_openai_key(openai_api_key)

def get_weather(city):
    return f"The weather in {city} is sunny"

@function_tool
def get_weather(city: str) -> str:
    """Get the current weather in a given city"""
    return f"The weather in {city} is sunny with a temperature of 70 degrees."

weather_haiku_agent = Agent(
    name="Weather Haiku Agent",
    instructions="You create haikus about the weather. Use the weather tool to get information.",
    tools=[get_weather],
)

result = Runner.run_sync(weather_haiku_agent, "What is the weather in Tokyo?")
print(result.final_output)

