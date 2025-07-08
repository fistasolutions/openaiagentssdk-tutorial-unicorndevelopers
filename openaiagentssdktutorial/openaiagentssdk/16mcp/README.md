# 🚀 MCP (Model Context Protocol) Examples Collection

## 📖 Overview

Welcome to the comprehensive **Model Context Protocol (MCP)** examples collection! This directory contains a series of progressively advanced examples that teach you how to use MCP with the OpenAI Agents SDK.

## 🎯 What is MCP? (Simple Explanation)

**Model Context Protocol (MCP)** is like a "universal translator" that helps AI agents talk to different tools and services. Think of it as a standard language that lets your AI assistant connect to databases, file systems, APIs, and other tools without needing to learn each one's specific way of communicating.

### 🎯 Simple Analogy
Imagine you're traveling to different countries where people speak different languages. Instead of learning every language, you have a universal translator (MCP) that can communicate with everyone. Similarly, MCP helps AI agents work with any tool or service using one common language.

### Why Do We Need MCP?

- **🔧 Tool Integration**: Connect to databases, APIs, file systems (like giving your AI access to your computer)
- **📊 Data Access**: Read real-time data from various sources (like letting your AI check the weather or read files)
- **🛡️ Security**: Secure, controlled access to external resources (like giving your AI a key card with limited access)
- **🔄 Standardization**: Consistent interface across different tools (like having one remote control for all your devices)

## 📚 Examples Overview

| # | Example | Description | Difficulty |
|---|---------|-------------|------------|
| 01 | [Basic MCP Example](./01-basic-mcp-example/) | Connect to filesystem MCP server | 🌱 Beginner |
| 02 | [Multiple MCP Servers](./02-multiple-mcp-servers/) | Connect to multiple servers simultaneously | 🌿 Intermediate |
| 03 | [Static Tool Filtering](./03-static-tool-filtering/) | Control which tools your agent can access | 🌿 Intermediate |
| 04 | [Dynamic Tool Filtering](./04-dynamic-tool-filtering/) | Filter tools based on context and conditions | 🌳 Advanced |
| 05 | [File Search Example](./05-file-search-example/) | Advanced file searching and analysis | 🌿 Intermediate |
| 06 | [Git Example](./06-git-example/) | Git repository analysis and management | 🌿 Intermediate |
| 07 | [Prompts Example](./07-prompts-example/) | Working with MCP prompt servers | 🌿 Intermediate |
| 08 | [Prompt Server](./08-prompt-server/) | Creating custom prompt servers | 🌳 Advanced |
| 09 | [SSE Example](./09-sse-example/) | Server-Sent Events MCP servers | 🌳 Advanced |
| 10 | [Streamable HTTP Example](./10-streamable-http-example/) | HTTP-based streaming MCP servers | 🌳 Advanced |
| 11 | [Working Streamable HTTP](./11-streamable-http-working/) | Complete server-client setup | 🌿 Intermediate |

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│                 │    │   MCP Servers    │    │   Data Sources  │
│                 │    │                  │    │                 │
│   Your Agent    │◄──►│   - Filesystem   │◄──►│   - Files       │
│   (Client)      │    │   - Git          │    │   - Repositories│
│                 │    │   - Database     │    │   - APIs        │
│                 │    │   - Custom       │    │   - Services    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🛠️ Prerequisites

Before running any examples, make sure you have:

1. **Python 3.8+** installed
2. **OpenAI API Key** set up
3. **Node.js/npm** installed (for some MCP servers)
4. **Git** installed (for Git examples)
5. **Required packages** installed:
   ```bash
   uv add openai-agents python-dotenv mcp requests
   ```

## 🔧 Quick Start

### 1. Environment Setup

Create a `.env` file in this directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
```

### 2. Start with Basic Example

```bash
cd 01-basic-mcp-example
uv run mcpbasic.py
```

### 3. Explore Other Examples

Each example directory contains:
- `README.md` - Detailed explanation and walkthrough
- Python scripts - Working code examples
- Sample files (where applicable)

## 📖 Learning Path

### 🌱 Beginner Level
Start here if you're new to MCP:

1. **[01-basic-mcp-example](./01-basic-mcp-example/)** - Learn the fundamentals
2. **[02-multiple-mcp-servers](./02-multiple-mcp-servers/)** - Connect to multiple sources
3. **[03-static-tool-filtering](./03-static-tool-filtering/)** - Control tool access

### 🌿 Intermediate Level
Build on your foundation:

4. **[05-file-search-example](./05-file-search-example/)** - Advanced file operations
5. **[06-git-example](./06-git-example/)** - Git repository integration
6. **[07-prompts-example](./07-prompts-example/)** - Working with prompts
7. **[11-streamable-http-working](./11-streamable-http-working/)** - Complete server setup

### 🌳 Advanced Level
Master advanced concepts:

8. **[04-dynamic-tool-filtering](./04-dynamic-tool-filtering/)** - Context-aware filtering
9. **[08-prompt-server](./08-prompt-server/)** - Custom prompt servers
10. **[09-sse-example](./09-sse-example/)** - Real-time streaming
11. **[10-streamable-http-example](./10-streamable-http-example/)** - HTTP streaming

## 🔍 Key Concepts (Simple Terms)

### MCP Components - Think of it like a Restaurant

| Component | What it is | Simple Example |
|-----------|------------|----------------|
| **Agent** | The customer (AI brain) | "I want to order food" |
| **MCP Server** | The restaurant (tool provider) | "Here's your food" |
| **Tools** | The menu items (functions) | `read_file()`, `get_weather()`, `analyze_git()` |
| **Transport** | How you communicate (phone, app, in-person) | HTTP, SSE, stdio |

### 🍕 Real-World Example
- **Agent**: "I need to know what's in my documents folder"
- **MCP Server**: "I'll check your documents folder for you"
- **Tool**: `list_files()` - lists all files in a folder
- **Transport**: HTTP - like using a website to order food

### Tool Filtering Strategies - Think of it like Security Levels

| Strategy | When to Use | Simple Example |
|----------|-------------|----------------|
| **Static** | Security, performance | Only allow read operations (like a library - you can read books but not write in them) |
| **Dynamic** | Context-aware access | Allow write only in specific directories (like a hotel - you can use your room but not other rooms) |
| **Role-based** | User permissions | Different tools for different users (like a school - teachers have different access than students) |

## 🚨 Common Issues & Solutions

### 1. "OpenAI API key not found"
```bash
# Create .env file
echo "OPENAI_API_KEY=your_key_here" > .env
```

### 2. "uv is not installed"
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. "MCP server connection failed"
- Check if required dependencies are installed
- Verify server is running on correct port
- Ensure firewall allows connections

### 4. "Tool not found"
- Check tool names match exactly
- Verify MCP server provides the expected tools
- Review server documentation

## 📊 Example Outputs

Each example includes:
- ✅ Expected output samples
- ✅ Step-by-step walkthroughs
- ✅ Troubleshooting guides
- ✅ Code explanations

## 🔗 Additional Resources

- [OpenAI Agents SDK Documentation](https://platform.openai.com/docs/agents)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- [FastMCP Documentation](https://modelcontextprotocol.io/docs/servers/fastmcp)

## 🤝 Contributing

Found an issue or have a suggestion? Feel free to:
- Report bugs
- Suggest improvements
- Add more examples
- Improve documentation

## 📝 License

This collection is part of the OpenAI Agents SDK tutorial series.

---

**🎉 Ready to start?** Choose an example from the table above and begin your MCP journey!

**💡 Pro Tip**: Start with the basic example and work your way up. Each example builds on the concepts from the previous ones. 