# 🛠️ Function Tools Example

## What This Code Does (Big Picture)
Imagine teaching your robot friend how to use different gadgets to help you! This code shows how to create custom tools that your AI assistant can use to get weather information, read files, and analyze data.

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
import json
import asyncio
from typing_extensions import TypedDict, Any
from agents import Agent, FunctionTool, RunContextWrapper, function_tool, set_default_openai_key
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
```
The AI assistant needs a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Creating a Custom Type for Location 📍
```python
# Define a custom type for location
class Location(TypedDict):
    lat: float
    long: float
```
This creates a special template for location information that includes:
- Latitude (a number like 37.7749)
- Longitude (a number like -122.4194)

## Step 3: Creating a Weather Tool 🌦️
```python
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
```
This creates an asynchronous tool that:
- Takes location coordinates as input
- Simulates an API call with a delay
- Returns different weather conditions based on the coordinates
- Uses proper documentation with Args section

## Step 4: Creating a File Reading Tool with Custom Name 📄
```python
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
```
This creates a tool that:
- Has a custom name "fetch_data" instead of "read_file"
- Takes a file path and optional directory as input
- Uses a context parameter for additional information
- Returns different content based on the file extension
- Includes proper documentation with Args section

## Step 5: Creating a Data Analysis Tool 📊
```python
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
```
This creates a tool that:
- Takes text data and an analysis type as input
- Performs different types of analysis based on the specified type
- Returns a dictionary with analysis results
- Includes proper documentation with Args section

## Step 6: Creating a Multi-Tool Assistant 🤖
```python
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
```
This creates an AI assistant that:
- Is named "Tool Assistant"
- Knows how to use all three tools
- Understands when to use each tool based on the task
- Has clear instructions about each tool's purpose

## Step 7: Displaying Tool Information 📋
```python
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
```
This function:
- Loops through all the tools attached to the agent
- Prints detailed information about each tool
- Shows the tool's name, description, and parameter schema
- Formats the parameter schema as readable JSON

## Step 8: Running the Program with Different Requests 🏃‍♂️
```python
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
```
This tests the assistant with different requests:
1. A weather request (uses the fetch_weather tool)
2. A file reading request (uses the fetch_data tool)
3. A text analysis request (uses the analyze_data tool)

## Step 9: Creating an Interactive Mode 💬
```python
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
```
This creates an interactive mode where:
- You can ask the assistant to use any of its tools
- You see the assistant's responses
- You can type "exit" to quit

## Final Summary 📌
✅ We created a custom type for location information
✅ We created an asynchronous weather tool
✅ We created a file reading tool with a custom name
✅ We created a data analysis tool with multiple analysis types
✅ We created an AI assistant that knows how to use all these tools
✅ We displayed detailed information about each tool
✅ We tested the assistant with different types of requests
✅ We added an interactive mode for custom queries

## Try It Yourself! 🚀
1. Install the required packages:
   ```
   uv add openai-agents python-dotenv typing-extensions
   ```
2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Run the program:
   ```
   uv run functiontools.py
   ```
4. Try asking about weather, reading files, and analyzing data with different parameters!

## What You'll Learn 🧠
- How to create custom function tools with TypedDict for complex inputs
- How to create asynchronous tools for API-like operations
- How to override tool names for better clarity
- How to use context parameters in tools
- How to document tools properly with Args sections
- How to create tools that return different data types (strings, dictionaries)
- How to inspect and display tool schemas

Happy coding! 🎉 