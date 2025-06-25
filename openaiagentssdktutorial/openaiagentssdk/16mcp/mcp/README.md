# 📦 Model Context Protocol (MCP) Filesystem Server Example

## 📋 Overview
This example demonstrates how to use the **Model Context Protocol (MCP)** to enable an agent to interact with a real filesystem using external tools. The agent connects to a local MCP server (running as a subprocess) and can perform file operations such as reading, listing, and summarizing files.

## 🎯 Key Concepts

### **Model Context Protocol (MCP)**
- **Purpose**: Standardizes how AI models (like LLMs) interact with external tools and environments.
- **MCP Server**: Acts as a bridge between the agent and real-world tools (e.g., filesystem, databases, APIs).
- **Stdio Communication**: The server communicates with the agent over standard input/output (stdio), making it language-agnostic.

### **Filesystem MCP Server**
- **Tooling**: Provides tools for file operations (read, write, list, etc.)
- **Temporary Directory**: Example uses a temporary directory for safe, isolated file operations.
- **Node.js Server**: Uses `npx @modelcontextprotocol/server-filesystem` to launch the server.

### **Agent Integration**
- **mcp_servers Parameter**: Passes the MCP server instance to the agent for tool access.
- **Tool Discovery**: Agent automatically discovers and uses available tools from the MCP server.

## 📁 Code Walkthrough

```python
from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv
import os
import tempfile

# Load environment variables and set up API key
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
from agents import set_default_openai_key
set_default_openai_key(openai_api_key)

async def main():
    # Create a temporary directory for the filesystem MCP server to access
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a sample file in the temporary directory
        with open(os.path.join(temp_dir, "sample.txt"), "w") as f:
            f.write("This is a sample file created for MCP demonstration.\n")
            f.write("The Model Context Protocol allows LLMs to interact with tools like filesystems.\n")
        print(f"Created temporary directory at: {temp_dir}")
        # Set up the MCP filesystem server
        async with MCPServerStdio(
            params={
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", temp_dir],
            },
            cache_tools_list=True  # Cache the tools list for better performance
        ) as server:
            # Create an agent with access to the MCP server
            agent = Agent(
                name="FileAssistant",
                instructions="You are a helpful assistant with access to a filesystem. Use the provided tools to read files and help the user understand their contents.",
                model="gpt-4o",
                mcp_servers=[server]
            )
            # Run the agent with a prompt that requires using the filesystem tools
            result = await Runner.run(
                agent, 
                "Please read the sample.txt file and summarize its contents."
            )
            print("\n--- Agent Response ---")
            print(result.final_output)
            # Try another operation
            result = await Runner.run(
                agent,
                "List all files in the current directory and tell me what you can do with them."
            )
            print("\n--- Agent Response for Directory Listing ---")
            print(result.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## 🚀 How to Run

1. **Install Node.js** (required for the MCP filesystem server):
   ```bash
   # If you don't have Node.js, install it first
   brew install node  # macOS
   sudo apt-get install nodejs npm  # Ubuntu/Debian
   ```
2. **Install the MCP Filesystem Server** (automatically done by npx):
   ```bash
   npx -y @modelcontextprotocol/server-filesystem --help
   ```
3. **Run the Python Example**:
   ```bash
   uv run mcp.py
   ```

## 🛠️ Customization Ideas

### **1. Use a Real Directory**
Instead of a temporary directory, point the server to a real folder:
```python
async with MCPServerStdio(
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/your/folder"],
    },
    cache_tools_list=True
) as server:
    ...
```

### **2. Add More Files**
Create more files in the directory to test advanced file operations (read, write, delete, etc.).

### **3. Use Other MCP Servers**
Try other MCP server types (e.g., database, API, custom tools) by changing the `command` and `args`.

### **4. Change Agent Instructions**
Make the agent a file manager, code reviewer, or data extractor by updating the `instructions` parameter.

## 🔍 How It Works

1. **Temporary Directory**: A safe, isolated directory is created for the demo.
2. **Sample File**: A text file is written for the agent to read and summarize.
3. **MCP Server Launch**: The Node.js MCP server is started as a subprocess, exposing filesystem tools.
4. **Agent Setup**: The agent is given access to the MCP server via the `mcp_servers` parameter.
5. **Tool Use**: The agent receives a prompt, discovers available tools, and uses them to answer the user's request.
6. **Result**: The agent's response is printed, showing its ability to read and summarize files, and list directory contents.

## ⚠️ Notes & Troubleshooting

- **Node.js Required**: The MCP server is a Node.js package. Make sure Node.js is installed.
- **npx Download Delay**: The first run may take longer as npx downloads the server package.
- **Permissions**: Ensure the agent/server has permission to access the target directory.
- **API Key**: Requires a valid OpenAI API key in your environment variables.
- **Model**: Uses `gpt-4o` by default, but you can change the model as needed.

## 🐛 Common Issues

- **"npx: command not found"**: Install Node.js and ensure it's in your PATH.
- **"Permission denied"**: Check directory permissions.
- **"No tools available"**: Ensure the MCP server started correctly and the directory is accessible.
- **API errors**: Check your OpenAI API key and model access.

## 📚 Best Practices

1. **Use Temporary Directories for Testing**: Prevents accidental file changes.
2. **Limit Agent Permissions**: Only expose safe directories/tools.
3. **Monitor Server Output**: Watch for errors from the MCP server subprocess.
4. **Cache Tools List**: Use `cache_tools_list=True` for better performance.
5. **Handle Errors Gracefully**: Add error handling for file and server issues.

## 🎓 Learning Path

1. **Basic File Operations**: Start with reading and listing files.
2. **Advanced Tooling**: Add more complex tools (edit, delete, move files).
3. **Custom MCP Servers**: Build your own MCP-compatible tools.
4. **Multi-Server Integration**: Connect to multiple MCP servers for advanced workflows.

---

*This example shows how to bridge AI agents with real-world tools using the Model Context Protocol, enabling safe, flexible, and powerful integrations with filesystems and beyond.* 