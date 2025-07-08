# 🔗 Multiple MCP Servers - Connecting to Multiple Data Sources

## 📖 Overview

This example demonstrates how to connect your AI agent to **multiple MCP servers simultaneously**. This is a powerful concept that allows your agent to access different types of data and tools from various sources at the same time.

## 🎯 What You'll Learn

- ✅ How to connect to multiple MCP servers in one agent
- ✅ How to manage different types of tools from different servers
- ✅ How agents can coordinate between multiple data sources
- ✅ Advanced MCP server orchestration

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│                 │    │   Filesystem     │    │   Sample Files  │
│                 │◄──►│   MCP Server     │◄──►│   (demo.txt,    │
│                 │    │                  │    │    books.txt)   │
│                 │    └──────────────────┘    └─────────────────┘
│   Your Agent    │
│   (Client)      │    ┌──────────────────┐    ┌─────────────────┐
│                 │    │   Git MCP        │    │   Git Repository│
│                 │◄──►│   Server         │◄──►│   (Code,        │
│                 │    │                  │    │    Commits)     │
│                 │    └──────────────────┘    └─────────────────┘
└─────────────────┘
```

## 📁 Project Structure

```
02-multiple-mcp-servers/
├── README.md              # This file
└── 4mcpservers.py         # Main script with multiple servers
```

## 🛠️ Prerequisites

Before running this example, make sure you have:

1. **Python 3.8+** installed
2. **OpenAI API Key** set up
3. **Git** installed (for Git MCP server)
4. **Node.js/npm** installed (for MCP servers)
5. **Required packages** installed:
   ```bash
   pip install openai-agents python-dotenv
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
pip install openai-agents python-dotenv
```

### 3. Run the Example

```bash
python 4mcpservers.py
```

## 📝 Code Walkthrough

### Main Script: `4mcpservers.py`

Let's break down the code step by step:

#### 1. Imports and Setup

```python
import os
import asyncio
from dotenv import load_dotenv

from agents import Agent, Runner, set_default_openai_key
from agents.mcp import MCPServerStdio
```

**What this does:**
- Standard imports for async operations and environment management
- MCP server connection utilities

#### 2. Multiple Server Connections

```python
# Path to the directory with sample files for the MCP filesystem
current_dir = os.path.dirname(os.path.abspath(__file__))
samples_dir = os.path.join(current_dir, "sample_files")

# Start multiple MCP servers
async with MCPServerStdio(
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
    }
) as filesystem_server, MCPServerStdio(
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-git"],
    }
) as git_server:
```

**What this does:**
- Creates **two separate MCP server connections**
- `filesystem_server`: Provides file reading capabilities
- `git_server`: Provides Git repository analysis capabilities
- Both servers run simultaneously and independently

#### 3. Agent with Multiple Servers

```python
agent = Agent(
    name="Multi-Source Assistant",
    model=openai_model,
    instructions=(
        "You're a helpful assistant that can read files and analyze Git repositories. "
        "Use the available tools from both servers to provide comprehensive answers. "
        "When asked about files, use the filesystem tools. "
        "When asked about Git repositories, use the Git tools."
    ),
    mcp_servers=[filesystem_server, git_server],  # Multiple servers!
)
```

**What this does:**
- Creates an agent that can access **both servers**
- Provides clear instructions on when to use which tools
- The agent automatically discovers tools from both servers

#### 4. Multi-Source Queries

```python
# Query that uses both servers
comprehensive_query = """
Please do the following:

1. First, read the demo.txt file and explain what MCP is
2. Then, analyze the current Git repository and tell me about recent commits
3. Finally, combine this information to explain how MCP can be used with Git

Please provide detailed answers for each part.
"""

result = await Runner.run(starting_agent=agent, input=comprehensive_query)
```

**What this does:**
- Sends a query that requires data from **both servers**
- The agent intelligently chooses which tools to use
- Combines information from multiple sources

## 🔍 How It Works

### Step-by-Step Process

1. **Server Startup**: Multiple MCP servers start simultaneously
2. **Connection**: Agent connects to all servers
3. **Tool Discovery**: Agent discovers tools from all connected servers
4. **Query Processing**: When you ask a question, the agent:
   - Determines which servers have relevant tools
   - Calls tools from appropriate servers
   - Combines results from multiple sources
   - Provides a comprehensive answer

### Multi-Server Communication Flow

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
│             │    │   Filesystem     │    │   File System   │
│             │◄──►│   MCP Server     │◄──►│   (demo.txt)    │
│             │    │                  │    │                 │
│             │    └──────────────────┘    └─────────────────┘
│    Agent    │
│             │    ┌──────────────────┐    ┌─────────────────┐
│             │    │   Git MCP        │    │   Git Repo      │
│             │◄──►│   Server         │◄──►│   (commits)     │
│             │    │                  │    │                 │
└─────────────┘    └──────────────────┘    └─────────────────┘
```

## 📊 Expected Output

When you run the script, you should see output like this:

```
============================================================
MULTIPLE MCP SERVERS DEMO: File Reading + Git Analysis
============================================================
Running comprehensive demo...

🧠 Response:
I'll help you with that! Let me gather information from both the filesystem and Git repository.

1. **What is MCP (from demo.txt):**
   MCP (Model Context Protocol) is a standardized protocol that enables AI models to interact with external data sources and tools. It provides:
   - File system access
   - Tool integration
   - Real-time data access
   - Secure communication

2. **Git Repository Analysis:**
   Based on the Git repository analysis, I can see:
   - Recent commits include updates to MCP examples
   - The repository contains multiple MCP server implementations
   - There are examples for filesystem, Git, and other MCP servers

3. **Combining MCP with Git:**
   MCP can be used with Git to:
   - Analyze repository history and commits
   - Read and understand code changes
   - Provide insights about development patterns
   - Help with code review and documentation

============================================================
✅ Multiple MCP Servers Demo completed successfully!
============================================================
```

## 🎯 Key Concepts Explained

### Why Multiple Servers?

**Multiple MCP servers** allow your agent to access different types of data and tools simultaneously. This is like giving your agent multiple "superpowers" at once.

### Server Coordination

| Aspect | Single Server | Multiple Servers |
|--------|---------------|------------------|
| **Data Sources** | One type | Multiple types |
| **Tool Variety** | Limited | Extensive |
| **Complexity** | Simple | Advanced |
| **Capabilities** | Basic | Comprehensive |

### Tool Discovery and Selection

When an agent connects to multiple servers:

1. **Discovery Phase**: Agent learns about all available tools
2. **Categorization**: Tools are grouped by server/functionality
3. **Selection**: Agent chooses appropriate tools for each task
4. **Execution**: Tools are called from the correct servers
5. **Integration**: Results are combined into a coherent response

## 🚨 Troubleshooting

### Common Issues

1. **"Git server not found"**
   ```bash
   # Install Git MCP server
   npm install -g @modelcontextprotocol/server-git
   ```

2. **"Multiple server conflicts"**
   - Ensure each server uses different ports
   - Check that server names are unique
   - Verify tool names don't conflict

3. **"Agent confusion about tools"**
   - Provide clear instructions about tool usage
   - Use descriptive tool names
   - Test with simple queries first

### Debug Mode

To see detailed server interactions:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔗 Next Steps

After completing this example, try:

1. **🌐 Web APIs**: Add servers for web services and APIs
2. **🗄️ Databases**: Connect to database MCP servers
3. **📊 Analytics**: Add servers for data analysis tools
4. **🤖 Custom Servers**: Create your own MCP servers

## 📚 Additional Resources

- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- [Git MCP Server](https://github.com/modelcontextprotocol/server-git)
- [Filesystem MCP Server](https://github.com/modelcontextprotocol/server-filesystem)
- [Creating Custom MCP Servers](https://modelcontextprotocol.io/docs/servers)

## 🤝 Contributing

Found an issue or have a suggestion? Feel free to:
- Report bugs
- Suggest improvements
- Add more server examples
- Improve documentation

---

**🎉 Congratulations!** You've successfully learned how to connect your AI agent to multiple MCP servers. You now understand how to create powerful, multi-source AI applications! 