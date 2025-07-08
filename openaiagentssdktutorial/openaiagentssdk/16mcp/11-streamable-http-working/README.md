# 🌐 Working Streamable HTTP MCP Example - Complete Server-Client Setup

## 📖 Overview

This is a **complete, working example** of a Streamable HTTP MCP server and client setup. You'll learn how to create your own MCP server with custom tools and connect to it using the OpenAI Agents SDK.

## 🎯 What You'll Learn

- ✅ How to create a custom MCP server with FastMCP
- ✅ How to implement custom tools (add, weather, secret word)
- ✅ How to connect to a streamable HTTP MCP server
- ✅ How to run server and client in a complete workflow
- ✅ Real-world MCP server-client communication

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│                 │    │   Custom MCP     │    │   External      │
│                 │◄──►│   Server         │◄──►│   Services      │
│   Your Agent    │    │   (FastMCP)      │    │                 │
│   (Client)      │    │                  │    │ - Weather API   │
│                 │    │   Tools:         │    │ - Random Data   │
│                 │    │   - add()        │    │                 │
│                 │    │   - weather()    │    │                 │
│                 │    │   - secret()     │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
11-streamable-http-working/
├── README.md                    # This file
├── 11streamablehttpserver.py   # Custom MCP server
└── 11streamablehttpsmain.py    # Client script
```

## 🛠️ Prerequisites

Before running this example, make sure you have:

1. **Python 3.8+** installed
2. **OpenAI API Key** set up
3. **Required packages** installed:
   ```bash
   uv add openai-agents python-dotenv mcp requests
   ```

## 🔧 Setup Instructions

### 1. Environment Setup

Create a `.env` file in this directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
```

### 2. Install Dependencies

```bash
uv add openai-agents python-dotenv mcp requests
```

### 3. Run the Complete Example

```bash
uv run 11streamablehttpsmain.py
```

This will:
- Start the custom MCP server automatically
- Connect the agent to the server
- Run multiple test queries
- Clean up resources when done

## 📝 Code Walkthrough

### Server Script: `11streamablehttpserver.py`

Let's break down the server code:

#### 1. Server Setup

```python
import random
import requests
from mcp.server import FastMCP

# Create server
mcp = FastMCP("Streamable HTTP Python Server")
```

**What this does:**
- Imports required libraries for server functionality
- Creates a FastMCP server instance
- Sets the server name for identification

#### 2. Custom Tools

```python
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print(f"[debug-server] add({a}, {b})")
    return a + b

@mcp.tool()
def get_secret_word() -> str:
    """Get a random secret word"""
    print("[debug-server] get_secret_word()")
    return random.choice(["apple", "banana", "cherry", "dragon", "elephant", "flamingo"])

@mcp.tool()
def get_current_weather(city: str) -> str:
    """Get current weather for a city"""
    print(f"[debug-server] get_current_weather({city})")
    
    try:
        endpoint = "https://wttr.in"
        response = requests.get(f"{endpoint}/{city}?format=3")
        return response.text
    except Exception as e:
        return f"Error getting weather for {city}: {str(e)}"
```

**What this does:**
- `@mcp.tool()`: Decorator that registers functions as MCP tools
- `add()`: Simple arithmetic tool for adding numbers
- `get_secret_word()`: Returns random words from a predefined list
- `get_current_weather()`: Connects to wttr.in API for real weather data

#### 3. Server Startup

```python
if __name__ == "__main__":
    print("Starting Streamable HTTP MCP Server...")
    print("Server will be available at http://localhost:8000/mcp")
    mcp.run(transport="streamable-http")
```

**What this does:**
- Starts the server on port 8000
- Uses streamable HTTP transport
- Provides clear startup messages

### Client Script: `11streamablehttpsmain.py`

Let's break down the client code:

#### 1. Environment and Imports

```python
import asyncio
import os
import shutil
import subprocess
import time
from typing import Any
from dotenv import load_dotenv

from agents import Agent, Runner, gen_trace_id, trace, set_default_openai_key
from agents.mcp import MCPServer, MCPServerStreamableHttp
from agents.model_settings import ModelSettings

# Load environment variables
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_model = os.environ.get("OPENAI_MODEL", "gpt-4o")
set_default_openai_key(openai_api_key)
```

**What this does:**
- Sets up environment variables and API keys
- Imports all necessary components
- Configures the OpenAI client

#### 2. Agent Function

```python
async def run(mcp_server: MCPServer):
    """Run the agent with the MCP server"""
    agent = Agent(
        name="Assistant",
        instructions="Use the tools to answer the questions.",
        mcp_servers=[mcp_server],
        model_settings=ModelSettings(tool_choice="required"),
    )

    # Use the `add` tool to add two numbers
    message = "Add these numbers: 7 and 22."
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    # Run the `get_weather` tool
    message = "What's the weather in Tokyo?"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    # Run the `get_secret_word` tool
    message = "What's the secret word?"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)
```

**What this does:**
- Creates an agent with the MCP server
- Runs three different test queries
- Demonstrates each tool's functionality

#### 3. Server Management

```python
if __name__ == "__main__":
    # Let's make sure the user has uv installed
    if not shutil.which("uv"):
        raise RuntimeError(
            "uv is not installed. Please install it: https://docs.astral.sh/uv/getting-started/installation/"
        )

    # We'll run the Streamable HTTP server in a subprocess
    process: subprocess.Popen[Any] | None = None
    try:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        server_file = os.path.join(this_dir, "11streamablehttpserver.py")

        print("Starting Streamable HTTP server at http://localhost:8000/mcp ...")

        # Run `uv run server.py` to start the Streamable HTTP server
        process = subprocess.Popen(["uv", "run", server_file])
        # Give it 3 seconds to start
        time.sleep(3)

        print("Streamable HTTP server started. Running example...\n\n")
    except Exception as e:
        print(f"Error starting Streamable HTTP server: {e}")
        exit(1)

    try:
        asyncio.run(main())
    finally:
        if process:
            process.terminate()
```

**What this does:**
- Checks for required dependencies (uv)
- Starts the server as a subprocess
- Manages server lifecycle
- Ensures proper cleanup

## 🔍 How It Works

### Step-by-Step Process

1. **Server Startup**: The main script starts the MCP server
2. **Server Initialization**: FastMCP server starts on port 8000
3. **Client Connection**: Agent connects to the server
4. **Tool Discovery**: Agent discovers the three available tools
5. **Query Processing**: Agent uses tools to answer questions
6. **Cleanup**: Server is terminated when done

### Communication Flow

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
│             │    │   Custom MCP     │    │   External      │
│             │◄──►│   Server         │◄──►│   APIs          │
│    Agent    │    │   (Port 8000)    │    │                 │
│             │    │                  │    │ - wttr.in       │
│             │    │   Tools:         │    │ - Random        │
│             │    │   - add()        │    │   Generator     │
│             │    │   - weather()    │    │                 │
│             │    │   - secret()     │    │                 │
└─────────────┘    └──────────────────┘    └─────────────────┘
```

## 📊 Expected Output

When you run the script, you should see output like this:

```
Starting Streamable HTTP server at http://localhost:8000/mcp ...
Starting Streamable HTTP MCP Server...
Server will be available at http://localhost:8000/mcp
INFO:     Started server process [35008]
INFO:     Waiting for application startup.
StreamableHTTP session manager started
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
Streamable HTTP server started. Running example...

View trace: https://platform.openai.com/traces/trace?trace_id=trace_a747a5ea039046f181ff8d5ce73f9b3d

Running: Add these numbers: 7 and 22.
[debug-server] add(7, 22)
The sum of 7 and 22 is 29.

Running: What's the weather in Tokyo?
[debug-server] get_current_weather(Tokyo)
The current weather in Tokyo is 27°C with occasional showers (🌦).

Running: What's the secret word?
[debug-server] get_secret_word()
The secret word is **banana**.
```

## 🎯 Key Concepts Explained

### What is FastMCP?

**FastMCP** is a Python framework for creating MCP servers quickly and easily. It provides decorators and utilities to turn Python functions into MCP tools.

### Streamable HTTP Transport

**Streamable HTTP** is a transport protocol for MCP that allows:
- Real-time communication
- HTTP-based connections
- Streaming responses
- Web-friendly integration

### Tool Registration

The `@mcp.tool()` decorator:
- Registers a function as an MCP tool
- Automatically handles parameter validation
- Provides tool metadata to clients
- Enables remote function calls

## 🚨 Troubleshooting

### Common Issues

1. **"uv is not installed"**
   ```bash
   # Install uv
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **"Server connection failed"**
   - Check if port 8000 is available
   - Ensure all dependencies are installed
   - Verify the server file path is correct

3. **"Weather API not working"**
   - Check internet connection
   - Verify wttr.in is accessible
   - The server includes error handling for API failures

### Debug Mode

To see detailed server interactions:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔗 Next Steps

After completing this example, try:

1. **🔧 Custom Tools**: Add your own tools to the server
2. **🌐 Web Integration**: Connect to more external APIs
3. **🗄️ Database**: Add database access tools
4. **🤖 AI Services**: Integrate with other AI services

## 📚 Additional Resources

- [FastMCP Documentation](https://modelcontextprotocol.io/docs/servers/fastmcp)
- [MCP Server Examples](https://github.com/modelcontextprotocol/servers)
- [Streamable HTTP Specification](https://modelcontextprotocol.io/docs/transports/streamable-http)

## 🤝 Contributing

Found an issue or have a suggestion? Feel free to:
- Report bugs
- Suggest improvements
- Add more tools to the server
- Improve documentation

---

**🎉 Congratulations!** You've successfully created a complete, working MCP server-client setup. You now understand how to build custom MCP servers and integrate them with AI agents! 