from agents import Agent, function_tool, Runner
# try:
#     from agents.extensions.visualization import draw_graph
#     visualization_available = True
# except ImportError:
#     visualization_available = False
from dotenv import load_dotenv
import os

# Load environment variables and set up API key
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
from agents import set_default_openai_key
set_default_openai_key(openai_api_key)

# Define some tools
@function_tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"The weather in {city} is sunny and 75°F."

@function_tool
def translate_text(text: str, target_language: str) -> str:
    """Simulate translating text to a target language."""
    return f"Translated '{text}' to {target_language} (simulation)"

# Create specialized agents
spanish_agent = Agent(
    name="Spanish Assistant",
    instructions="You are a helpful assistant who only speaks Spanish. Always respond in Spanish.",
    model="gpt-4o"
)

technical_agent = Agent(
    name="Technical Expert",
    instructions="You are a technical expert who specializes in explaining complex concepts clearly.",
    model="gpt-4o",
    tools=[translate_text]
)

weather_agent = Agent(
    name="Weather Specialist",
    instructions="You are a weather specialist who provides detailed weather information.",
    model="gpt-4o",
    tools=[get_weather]
)

# Create a main triage agent
triage_agent = Agent(
    name="Triage Assistant",
    instructions="""You are a helpful assistant who routes requests to specialized agents.
    - For weather-related questions, use the Weather Specialist.
    - For technical explanations, use the Technical Expert.
    - For Spanish language requests, use the Spanish Assistant.
    - For general questions, answer directly.""",
    model="gpt-4o",
    handoffs=[spanish_agent, technical_agent, weather_agent],
    tools=[get_weather, translate_text]
)

def main():
    # Skip visualization entirely
    print("Skipping visualization. To enable visualization, install graphviz:")
    print("  pip install graphviz")
    print("  And install the Graphviz software: https://graphviz.org/download/")
    
    # Demonstrate the triage agent in action
    print("\nDemonstrating the triage agent with different queries:")
    
    # Weather query
    weather_query = "What's the weather like in Miami?"
    print(f"\nQuery: {weather_query}")
    result = Runner.run_sync(triage_agent, weather_query)
    print(f"Response: {result.final_output}")
    
    # Spanish query
    spanish_query = "¿Cómo estás hoy?"
    print(f"\nQuery: {spanish_query}")
    result = Runner.run_sync(triage_agent, spanish_query)
    print(f"Response: {result.final_output}")
    
    # Technical query
    technical_query = "Can you explain how neural networks work?"
    print(f"\nQuery: {technical_query}")
    result = Runner.run_sync(triage_agent, technical_query)
    print(f"Response: {result.final_output}")

if __name__ == "__main__":
    main() 