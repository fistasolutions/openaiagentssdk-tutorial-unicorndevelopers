# 📊 Agent Visualization with AI Agents

## What This Code Does (Big Picture)
This example demonstrates how to visualize the structure of AI agents, their tools, and handoffs using the visualization capabilities in the OpenAI Agents SDK. It creates a network of specialized agents and generates a graph showing how they're connected.

## Why Visualization Matters 🔍
When building complex AI systems with multiple agents and tools, it can be challenging to understand how everything fits together. Visualization helps you:

- See the overall structure of your agent network
- Understand how agents hand off tasks to each other
- Identify which tools are available to which agents
- Document your agent architecture for others

## Step 1: Setting Up the Environment 🗝️
```python
from agents import Agent, function_tool, Runner
from agents.extensions.visualization import draw_graph
from dotenv import load_dotenv
import os

# Load environment variables and set up API key
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
from agents import set_default_openai_key
set_default_openai_key(openai_api_key)
```
This code:
- Imports the necessary libraries, including the visualization module
- Loads your OpenAI API key from the environment
- Sets up the default key for our agents

## Step 2: Creating Tools for Our Agents 🛠️
```python
@function_tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"The weather in {city} is sunny and 75°F."

@function_tool
def translate_text(text: str, target_language: str) -> str:
    """Simulate translating text to a target language."""
    return f"Translated '{text}' to {target_language} (simulation)"
```
This creates:
- A weather tool that simulates getting weather information
- A translation tool that simulates translating text

## Step 3: Creating Specialized Agents 🤖
```python
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
```
This creates three specialized agents:
- A Spanish-speaking assistant
- A technical expert with translation capabilities
- A weather specialist with access to weather data

## Step 4: Creating a Triage Agent 🔀
```python
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
```
This creates a main agent that:
- Can hand off tasks to specialized agents
- Has access to all tools
- Decides which agent should handle each request

## Step 5: Generating the Visualization 📈
```python
graph = draw_graph(triage_agent, filename="agent_graph.png")
```
This code:
- Creates a visual representation of the agent network
- Saves it as a PNG file named "agent_graph.png"

## Understanding the Visualization
The generated graph includes:
- A start node (__start__) indicating the entry point
- Agents represented as yellow rectangles
- Tools represented as green ellipses
- Directed edges showing connections:
  - Solid arrows for agent-to-agent handoffs
  - Dotted arrows for tool invocations
- An end node (__end__) indicating where execution terminates

## Step 6: Demonstrating the Agents in Action 🚀
```python
# Weather query
weather_query = "What's the weather like in Miami?"
result = Runner.run_sync(triage_agent, weather_query)

# Spanish query
spanish_query = "¿Cómo estás hoy?"
result = Runner.run_sync(triage_agent, spanish_query)

# Technical query
technical_query = "Can you explain how neural networks work?"
result = Runner.run_sync(triage_agent, technical_query)
```
This code:
- Tests the triage agent with different types of queries
- Shows how it routes each query to the appropriate specialized agent

## Try It Yourself! 🚀
1. Install the required packages:
   ```
   uv add "openai-agents[viz]" python-dotenv
   ```
2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Run the program:
   ```
   uv run agentvisualization.py
   ```
4. Check out the generated `agent_graph.png` file to see your agent network!

## Customizing the Visualization
- To view the graph in a separate window: `graph.view()`
- To save in a different format: Change the filename extension (e.g., `agent_graph.svg`)
- To modify the appearance: The visualization uses Graphviz, which has many customization options

## What You'll Learn 🧠
- How to visualize complex agent networks
- How to create specialized agents for different tasks
- How to implement a triage system for routing requests
- How to document your agent architecture visually

Happy visualizing! 🎉 