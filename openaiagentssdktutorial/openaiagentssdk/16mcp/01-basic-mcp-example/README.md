# 🚀 Basic MCP Example - Getting Started with Model Context Protocol

## 📖 What is This Example? (Simple Explanation)

This is your **first step** into the world of MCP! Think of this as learning to ride a bicycle - we start with the basics before going on adventures.

### 🎯 Simple Explanation
This example shows you how to make your AI assistant talk to your computer's file system (the place where all your files and folders are stored). It's like teaching your AI to read files from your computer, just like you can open and read documents.

### 🏠 Real-World Analogy
Imagine you have a smart assistant who can help you organize your house, but they can't see what's inside your rooms. MCP is like giving them a special key that lets them look inside your rooms (folders) and tell you what's there (files).

## 📖 Overview

This is your first step into the world of **Model Context Protocol (MCP)** with OpenAI Agents SDK! This example demonstrates how to connect to an MCP server and use it to read files and answer questions.

## 🎯 What You'll Learn (In Simple Terms)

- ✅ How to set up an MCP server connection (like connecting your phone to WiFi)
- ✅ How to create an agent that can use MCP tools (like teaching your assistant new skills)
- ✅ How to read files and answer questions about their content (like having your assistant read books and tell you what they say)
- ✅ Basic MCP server-client communication (like learning how your assistant talks to your computer)

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Your Agent    │◄──►│   MCP Server     │◄──►│  File System    │
│   (Client)      │    │   (Filesystem)   │    │  (Sample Files) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
01-basic-mcp-example/
├── README.md              # This file
├── mcpbasic.py           # Main script
└── sample_files/         # Sample files for the MCP server
    ├── demo.txt          # MCP explanation
    ├── books.txt         # Book recommendations
    └── notes.txt         # Study notes
```

## 🛠️ Prerequisites

Before running this example, make sure you have:

1. **Python 3.8+** installed
2. **OpenAI API Key** set up
3. **Required packages** installed:
   ```bash
   uv add openai-agents python-dotenv
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
uv add openai-agents python-dotenv
```

### 3. Run the Example

```bash
uv run mcpbasic.py
```

## 📝 Code Walkthrough

### Main Script: `mcpbasic.py`

Let's break down the code step by step:

#### 1. Imports and Setup (Like Gathering Your Tools)

```python
import os
import asyncio
from dotenv import load_dotenv

from agents import Agent, Runner, set_default_openai_key
from agents.mcp import MCPServerStdio
```

**What this does (in simple terms):**
- `load_dotenv()`: Loads your secret keys from a file (like opening a safe)
- `set_default_openai_key()`: Sets up your OpenAI API key (like giving your assistant your phone number)
- `MCPServerStdio`: Connects to MCP servers (like the cable that connects your TV to the cable box)

#### 2. MCP Server Connection (Like Connecting to WiFi)

```python
async with MCPServerStdio(
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
    }
) as mcp_server:
```

**What this does (in simple terms):**
- Creates a connection to a filesystem MCP server (like connecting your phone to WiFi)
- Uses `npx` to run the official filesystem server (like downloading and installing an app)
- Points to your `sample_files` directory (like telling your assistant which room to look in)
- Automatically manages the server lifecycle (like having someone turn the lights on and off for you)

#### 3. Agent Creation (Like Hiring an Assistant)

```python
agent = Agent(
    name="File Assistant",
    model=openai_model,
    instructions=(
        "You're a helpful assistant that can read files and answer questions about them. "
        "Use the available tools to read files and provide detailed, helpful responses. "
        "When you read files, remember their content to answer follow-up questions."
    ),
    mcp_servers=[mcp_server],
)
```

**What this does (in simple terms):**
- Creates an AI agent with a specific personality (like hiring someone with a specific job)
- Gives it instructions on how to behave (like giving your new employee a job description)
- Connects it to the MCP server (which provides file-reading tools) (like giving your employee the keys to the office)

#### 4. Running Queries (Like Asking Your Assistant Questions)

```python
comprehensive_query = """
Please do the following in order:

1. First, read all the files you can access and list them
2. Then, based on the demo.txt file, explain what MCP is and its key features
3. Finally, based on the books.txt file, tell me what my #1 favorite book is and why I might like it

Please provide clear, detailed answers for each part.
"""

result = await Runner.run(starting_agent=agent, input=comprehensive_query)
```

**What this does (in simple terms):**
- Sends a complex query to the agent (like asking your assistant to do multiple tasks)
- The agent uses MCP tools to read files (like your assistant opening books to find information)
- Returns a comprehensive response based on file content (like your assistant giving you a detailed report)

## 🔍 How It Works (Simple Steps)

### Step-by-Step Process (Like Making a Phone Call)

1. **Server Startup**: The script starts an MCP filesystem server (like turning on your phone)
2. **Connection**: Your agent connects to the server (like dialing a number)
3. **Tool Discovery**: The agent discovers available file-reading tools (like finding out what apps are available)
4. **Query Processing**: When you ask a question, the agent:
   - Determines which files to read (like deciding which app to use)
   - Uses MCP tools to read the files (like opening an app)
   - Analyzes the content (like reading the information)
   - Provides a comprehensive answer (like telling you what they found)

### MCP Communication Flow

```
┌─────────────┐   1. Initialize    ┌─────────────┐
│    Agent    │ ──────────────────► │ MCP Server  │
│             │                     │             │
│             │   2. List Tools    │             │
│             │ ◄────────────────── │             │
│             │                     │             │
│             │   3. Call Tool     │             │
│             │ ──────────────────► │             │
│             │                     │             │
│             │   4. Tool Result   │             │
│             │ ◄────────────────── │             │
└─────────────┘                     └─────────────┘
```

## 📊 Expected Output

When you run the script, you should see output like this:

```
============================================================
MCP DEMO: Reading Files and Answering Questions
============================================================
Running comprehensive demo...

🧠 Response:
I'll help you with that! Let me start by reading the available files and then provide detailed answers to your questions.

1. **Files Available:**
   - demo.txt: Contains information about MCP (Model Context Protocol)
   - books.txt: Contains book recommendations and favorites
   - notes.txt: Contains study notes

2. **What is MCP and its Key Features:**
   Based on the demo.txt file, MCP (Model Context Protocol) is a protocol that enables AI models to interact with external data sources and tools. Key features include:
   - File system access
   - Tool integration
   - Real-time data access
   - Secure communication

3. **Your #1 Favorite Book:**
   According to books.txt, your #1 favorite book is "The Pragmatic Programmer" because it provides practical programming wisdom and real-world advice that's applicable to any programming language or technology.

============================================================
✅ MCP Demo completed successfully!
============================================================
```

## 🎯 Key Concepts Explained

### What is MCP?

**Model Context Protocol (MCP)** is a standardized way for AI models to interact with external data sources, tools, and services. Think of it as a "bridge" between your AI agent and the real world.

### Why Use MCP?

- **🔧 Tool Integration**: Connect to databases, APIs, file systems
- **📊 Data Access**: Read real-time data from various sources
- **🛡️ Security**: Secure, controlled access to external resources
- **🔄 Standardization**: Consistent interface across different tools

### Agent vs MCP Server

| Component | Role | Example |
|-----------|------|---------|
| **Agent** | AI brain that makes decisions | "I need to read a file to answer this question" |
| **MCP Server** | Tool provider that executes actions | "Here's the content of the file you requested" |

## 🚨 Troubleshooting

### Common Issues

1. **"uv is not installed"**
   ```bash
   # Install uv
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **"OpenAI API key not found"**
   - Make sure your `.env` file exists
   - Verify your API key is correct
   - Check that `python-dotenv` is installed

3. **"MCP server connection failed"**
   - Ensure you have internet connection
   - Check if `npx` is available
   - Verify the sample_files directory exists

### Debug Mode

To see more detailed output, you can modify the script to include debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔗 Next Steps

After completing this example, try:

1. **📁 File Operations**: Modify the sample files and see how the agent responds
2. **🔧 Custom Tools**: Create your own MCP server with custom tools
3. **🌐 Web Integration**: Connect to web APIs and services
4. **🗄️ Database Access**: Read from databases and data stores

## 📚 Additional Resources

- [OpenAI Agents SDK Documentation](https://platform.openai.com/docs/agents)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [MCP Server Examples](https://github.com/modelcontextprotocol/servers)

## 🤝 Contributing

Found an issue or have a suggestion? Feel free to:
- Report bugs
- Suggest improvements
- Add more examples
- Improve documentation

---

**🎉 Congratulations!** You've successfully completed your first MCP example. You now understand how AI agents can interact with external data sources through the Model Context Protocol! 