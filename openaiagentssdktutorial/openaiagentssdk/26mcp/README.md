# 🔌 Model Context Protocol (MCP) with AI Agents

## What This Code Does (Big Picture)
This example demonstrates how to use the Model Context Protocol (MCP) to give your AI assistant access to external tools - specifically, a filesystem. The AI can read files, list directories, and interact with the file system just like a helpful assistant with access to your computer!

## What is MCP? 🤔
MCP (Model Context Protocol) is like a universal connector for AI models - similar to how USB-C connects your devices to various peripherals. It provides a standardized way for AI models to access different data sources and tools.

Think of it as giving your AI assistant "superpowers" to interact with the world beyond just text conversations!

## Step 1: Setting Up the Environment 🗝️
```python
from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv
import os
import tempfile

load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
from agents import set_default_openai_key
set_default_openai_key(openai_api_key)
```
This code:
- Imports the necessary libraries
- Loads your OpenAI API key from the environment
- Sets up the default key for our agents

## Step 2: Creating a Temporary Filesystem 📁
```python
with tempfile.TemporaryDirectory() as temp_dir:
    # Create a sample file in the temporary directory
    with open(os.path.join(temp_dir, "sample.txt"), "w") as f:
        f.write("This is a sample file created for MCP demonstration.\n")
        f.write("The Model Context Protocol allows LLMs to interact with tools like filesystems.\n")
```
This creates:
- A temporary directory that will be automatically cleaned up when done
- A sample text file for our AI to read

## Step 3: Setting Up the MCP Server 🖥️
```python
async with MCPServerStdio(
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", temp_dir],
    },
    cache_tools_list=True  # Cache the tools list for better performance
) as server:
    # Rest of the code...
```
This code:
- Creates an MCP server that provides filesystem access
- Points it to our temporary directory
- Enables caching for better performance

## Step 4: Creating an AI Assistant with MCP Tools 🤖
```python
agent = Agent(
    name="FileAssistant",
    instructions="You are a helpful assistant with access to a filesystem. Use the provided tools to read files and help the user understand their contents.",
    model="gpt-4o",
    mcp_servers=[server]
)
```
This creates an AI assistant that:
- Has a name: "FileAssistant"
- Knows it can access files
- Uses OpenAI's GPT-4o model
- Has access to our MCP filesystem server

## Step 5: Running the AI Assistant with File Tasks 🚀
```python
result = await Runner.run(
    agent, 
    "Please read the sample.txt file and summarize its contents."
)

print("\n--- Agent Response ---")
print(result.final_output)
```
This code:
- Asks the AI to read and summarize our sample file
- Prints out the AI's response

## Step 6: Exploring More Capabilities 🔍
```python
result = await Runner.run(
    agent,
    "List all files in the current directory and tell me what you can do with them."
)

print("\n--- Agent Response for Directory Listing ---")
print(result.final_output)
```
This demonstrates:
- The AI can also list directories
- It understands what operations are possible with the files

## Types of MCP Servers 🌐
The MCP specification defines two types of servers:
1. **stdio servers** (used in this example) - run as a subprocess of your application
2. **HTTP over SSE servers** - run remotely, accessed via URL

## Try It Yourself! 🚀
1. Install the required packages:
   ```
   uv add openai-agents python-dotenv
   npm install -g @modelcontextprotocol/server-filesystem
   ```
2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Run the program:
   ```
   uv run mcp.py
   ```
4. Try modifying the prompts to explore different file operations!

## What You'll Learn 🧠
- How to connect AI models to external tools using MCP
- How to give AI assistants access to filesystems
- How to cache tool information for better performance
- How to create more powerful AI applications with external capabilities

Happy coding! 🎉 