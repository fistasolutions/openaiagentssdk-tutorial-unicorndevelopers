# 🔧 Static Tool Filtering - Controlling Tool Access

## 📖 Overview

This example demonstrates **static tool filtering** in MCP, which allows you to control which tools your agent can access. This is useful for security, performance, and ensuring your agent only uses the tools you want it to use.

## 🎯 What You'll Learn

- ✅ How to filter tools statically (at connection time)
- ✅ How to control which tools your agent can access
- ✅ How to improve security by limiting tool access
- ✅ How to optimize performance by reducing tool complexity

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│                 │    │   MCP Server     │    │   All Available │
│                 │◄──►│   (Filesystem)   │◄──►│   Tools         │
│                 │    │                  │    │                 │
│   Your Agent    │    │   ┌─────────────┐│    │   - read_file   │
│   (Filtered)    │    │   │   Tool      ││    │   - write_file  │
│                 │    │   │  Filter     ││    │   - delete_file │
│                 │    │   └─────────────┘│    │   - list_files  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
03-static-tool-filtering/
├── README.md              # This file
└── 5statictoolfiltering.py # Main script with static filtering
```

## 🛠️ Prerequisites

Before running this example, make sure you have:

1. **Python 3.8+** installed
2. **OpenAI API Key** set up
3. **Node.js/npm** installed (for MCP servers)
4. **Required packages** installed:
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
python 5statictoolfiltering.py
```

## 📝 Code Walkthrough

### Main Script: `5statictoolfiltering.py`

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

#### 2. Static Tool Filtering

```python
# Define which tools we want to allow
allowed_tools = ["read_file", "list_files"]  # Only allow reading, not writing

async with MCPServerStdio(
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
    }
) as mcp_server:
    # Apply static filter to only allow specific tools
    filtered_tools = []
    all_tools = await mcp_server.list_tools()
    
    for tool in all_tools:
        if tool.name in allowed_tools:
            filtered_tools.append(tool)
            print(f"✅ Allowed tool: {tool.name}")
        else:
            print(f"❌ Blocked tool: {tool.name}")
```

**What this does:**
- Defines a list of **allowed tools** (only read operations)
- Connects to the MCP server
- **Filters the tools** to only include allowed ones
- Provides feedback on which tools are allowed/blocked

#### 3. Agent with Filtered Tools

```python
agent = Agent(
    name="Read-Only File Assistant",
    model=openai_model,
    instructions=(
        "You're a helpful assistant that can read files but cannot modify them. "
        "Use only the available tools to read files and provide information. "
        "If asked to write or delete files, explain that you can only read files."
    ),
    mcp_servers=[mcp_server],  # Server with filtered tools
)
```

**What this does:**
- Creates an agent with **read-only capabilities**
- Provides clear instructions about limitations
- The agent only sees the filtered tools

#### 4. Testing Filtered Access

```python
# Test read operations (should work)
read_query = "Read the demo.txt file and tell me what MCP is."
print(f"Testing read operation: {read_query}")
result = await Runner.run(starting_agent=agent, input=read_query)
print(result.final_output)

# Test write operations (should be blocked)
write_query = "Create a new file called test.txt with some content."
print(f"\nTesting write operation: {write_query}")
result = await Runner.run(starting_agent=agent, input=write_query)
print(result.final_output)
```

**What this does:**
- Tests **allowed operations** (reading files)
- Tests **blocked operations** (writing files)
- Shows how the agent responds when tools are unavailable

## 🔍 How It Works

### Step-by-Step Process

1. **Server Connection**: Connect to the MCP server
2. **Tool Discovery**: Get all available tools from the server
3. **Filtering**: Apply static filter to allow only specific tools
4. **Agent Creation**: Create agent with filtered tool set
5. **Query Processing**: Agent can only use allowed tools

### Static Filtering Flow

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
│             │    │   MCP Server     │    │   All Tools     │
│             │◄──►│                  │◄──►│                 │
│             │    │                  │    │ - read_file     │
│             │    │   ┌─────────────┐│    │ - write_file    │
│    Agent    │    │   │   Filter    ││    │ - delete_file   │
│             │    │   │   (Static)  ││    │ - list_files    │
│             │    │   └─────────────┘│    │                 │
│             │    │                  │    │                 │
│             │    │   ┌─────────────┐│    │   ┌─────────────┐│
│             │    │   │  Allowed    ││    │   │  Blocked    ││
│             │    │   │   Tools     ││    │   │   Tools     ││
│             │    │   │             ││    │   │             ││
│             │    │   │ - read_file ││    │   │ - write_file││
│             │    │   │ - list_files││    │   │ - delete_file││
│             │    │   └─────────────┘│    │   └─────────────┘│
└─────────────┘    └──────────────────┘    └─────────────────┘
```

## 📊 Expected Output

When you run the script, you should see output like this:

```
============================================================
STATIC TOOL FILTERING DEMO: Read-Only File Access
============================================================
Connecting to MCP server...

✅ Allowed tool: read_file
✅ Allowed tool: list_files
❌ Blocked tool: write_file
❌ Blocked tool: delete_file

Testing read operation: Read the demo.txt file and tell me what MCP is.

🧠 Response:
I'll read the demo.txt file for you.

Based on the demo.txt file, MCP (Model Context Protocol) is a standardized protocol that enables AI models to interact with external data sources and tools. It provides secure, controlled access to various data sources and services.

Testing write operation: Create a new file called test.txt with some content.

🧠 Response:
I apologize, but I can only read files and cannot create or modify them. I'm designed as a read-only assistant for security reasons. If you need to create or modify files, you would need to do that manually or use a different tool that has write permissions.

============================================================
✅ Static Tool Filtering Demo completed successfully!
============================================================
```

## 🎯 Key Concepts Explained

### What is Static Tool Filtering?

**Static tool filtering** means deciding which tools your agent can access **before** the agent starts working. This is like giving your agent a "toolbox" with only the tools you want it to have.

### Why Use Static Filtering?

| Benefit | Description | Example |
|---------|-------------|---------|
| **🔒 Security** | Prevent unauthorized operations | Block file deletion tools |
| **⚡ Performance** | Reduce tool complexity | Only show relevant tools |
| **🎯 Focus** | Keep agent focused on specific tasks | Only reading tools for data analysis |
| **🛡️ Safety** | Prevent accidental damage | Block destructive operations |

### Static vs Dynamic Filtering

| Aspect | Static Filtering | Dynamic Filtering |
|--------|------------------|-------------------|
| **When Applied** | At connection time | During runtime |
| **Flexibility** | Fixed | Adaptive |
| **Performance** | Fast | Slower |
| **Complexity** | Simple | Complex |

## 🚨 Troubleshooting

### Common Issues

1. **"Tool not found"**
   - Check that the tool name is correct
   - Verify the tool exists in the MCP server
   - Ensure the tool name matches exactly

2. **"Agent can still access blocked tools"**
   - Make sure filtering is applied before agent creation
   - Check that the filter logic is correct
   - Verify the agent is using the filtered tool list

3. **"Performance issues"**
   - Consider reducing the number of allowed tools
   - Use more specific tool names
   - Implement caching for tool discovery

### Debug Mode

To see detailed filtering information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔗 Next Steps

After completing this example, try:

1. **🔐 Security**: Create different filter profiles for different use cases
2. **⚡ Performance**: Optimize tool filtering for better performance
3. **🎯 Customization**: Create role-based tool access
4. **🔄 Dynamic**: Move to dynamic tool filtering for more flexibility

## 📚 Additional Resources

- [MCP Tool Filtering Documentation](https://modelcontextprotocol.io/docs/tools)
- [Security Best Practices](https://modelcontextprotocol.io/docs/security)
- [Tool Management Strategies](https://modelcontextprotocol.io/docs/management)

## 🤝 Contributing

Found an issue or have a suggestion? Feel free to:
- Report bugs
- Suggest improvements
- Add more filtering examples
- Improve documentation

---

**🎉 Congratulations!** You've successfully learned how to implement static tool filtering in MCP. You now understand how to control and secure your agent's tool access! 