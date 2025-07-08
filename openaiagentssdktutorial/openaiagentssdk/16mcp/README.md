# 🚀 MCP (Model Context Protocol) Examples Collection

## 📖 Overview

Welcome to the comprehensive **Model Context Protocol (MCP)** examples collection! This directory contains a series of progressively advanced examples that teach you how to use MCP with the OpenAI Agents SDK.

## 🎯 What is MCP?

**Model Context Protocol (MCP)** is a standardized way for AI models to interact with external data sources, tools, and services. Think of it as a "bridge" between your AI agent and the real world.

### Why MCP?

- **🔧 Tool Integration**: Connect to databases, APIs, file systems
- **📊 Data Access**: Read real-time data from various sources  
- **🛡️ Security**: Secure, controlled access to external resources
- **🔄 Standardization**: Consistent interface across different tools

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
   pip install openai-agents python-dotenv mcp requests
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
python mcpbasic.py
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

## 🔍 Key Concepts

### MCP Components

| Component | Role | Example |
|-----------|------|---------|
| **Agent** | AI brain that makes decisions | "I need to read a file to answer this question" |
| **MCP Server** | Tool provider that executes actions | "Here's the content of the file you requested" |
| **Tools** | Functions that perform specific tasks | `read_file()`, `get_weather()`, `analyze_git()` |
| **Transport** | Communication protocol | HTTP, SSE, stdio |

### Tool Filtering Strategies

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **Static** | Security, performance | Only allow read operations |
| **Dynamic** | Context-aware access | Allow write only in specific directories |
| **Role-based** | User permissions | Different tools for different users |

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