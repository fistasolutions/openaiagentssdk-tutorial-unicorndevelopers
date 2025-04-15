import json
import asyncio
from typing_extensions import TypedDict, Any
from agents import Agent, FunctionTool, RunContextWrapper, function_tool, set_default_openai_key
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)

# Define a custom type for location
class Location(TypedDict):
    lat: float
    long: float

# Define an asynchronous function tool for fetching weather
@function_tool  
async def fetch_weather(location: Location) -> str:
    """Fetch the weather for a given location.

    Args:
        location: The location to fetch the weather for.
    """
    # In real life, we'd fetch the weather from a weather API
    print(f"Fetching weather for location: {location}")
    # Simulate API call delay
    await asyncio.sleep(1)
    
    # Simple logic to generate different weather based on latitude
    if location["lat"] > 0:
        return "sunny" if location["long"] > 0 else "cloudy"
    else:
        return "rainy" if location["long"] > 0 else "snowy"

# Define a function tool with a custom name
@function_tool(name_override="fetch_data")  
def read_file(ctx: RunContextWrapper[Any], path: str, directory: str | None = None) -> str:
    """Read the contents of a file.

    Args:
        path: The path to the file to read.
        directory: The directory to read the file from.
    """
    # In real life, we'd read the file from the file system
    print(f"Reading file: {path} from directory: {directory or 'current'}")
    
    # Simple mock implementation
    if path.endswith(".txt"):
        return "This is a text file content."
    elif path.endswith(".json"):
        return '{"key": "value", "number": 42}'
    elif path.endswith(".csv"):
        return "id,name,value\n1,item1,100\n2,item2,200"
    else:
        return f"<contents of {path}>"

# Define a more complex function tool that processes data
@function_tool
def analyze_data(data: str, analysis_type: str) -> dict:
    """Analyze the provided data.
    
    Args:
        data: The data to analyze.
        analysis_type: The type of analysis to perform (summary, detailed, or statistical).
    """
    print(f"Analyzing data with analysis type: {analysis_type}")
    
    # Simple mock implementation
    if analysis_type == "summary":
        return {"result": "Data summary", "length": len(data), "type": "summary"}
    elif analysis_type == "detailed":
        return {"result": "Detailed analysis", "words": len(data.split()), "type": "detailed"}
    elif analysis_type == "statistical":
        return {"result": "Statistical analysis", "characters": len(data), "type": "statistical"}
    else:
        return {"error": "Unknown analysis type"}

# Create an agent with the function tools
agent = Agent(
    name="Tool Assistant",
    instructions="""
    You are an assistant that can help with various tasks using tools.
    - Use the fetch_weather tool to get weather information for a location
    - Use the fetch_data tool to read files
    - Use the analyze_data tool to analyze data
    
    Be helpful and use the appropriate tool for each task.
    """,
    tools=[fetch_weather, read_file, analyze_data],  
)

# Print information about the tools
def print_tool_info():
    print("=== Function Tools Information ===\n")
    for tool in agent.tools:
        if isinstance(tool, FunctionTool):
            print(f"Tool Name: {tool.name}")
            print(f"Description: {tool.description}")
            print("Parameters Schema:")
            print(json.dumps(tool.params_json_schema, indent=2))
            print()

async def main():
    
    # Print tool information
    print_tool_info()
    
    # Example queries that use the tools
    queries = [
        "What's the weather like at latitude 37.7749 and longitude -122.4194?",
        "Can you read the file 'data.json' from the 'reports' directory?",
        "Analyze this data: 'Sales increased by 15% in Q2 2023' with a detailed analysis."
    ]
    
    # Run the agent with each query
    from agents import Runner
    
    for i, query in enumerate(queries):
        print(f"\n=== Query {i+1}: {query} ===")
        result = await Runner.run(agent, query)
        print("\nResponse:")
        print(result.final_output)
    
    # Interactive mode
    print("\n=== Interactive Mode ===")
    print("Type 'exit' to quit")
    
    while True:
        user_input = input("\nYour query: ")
        if user_input.lower() == 'exit':
            break
        
        result = await Runner.run(agent, user_input)
        print("\nResponse:")
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main()) 