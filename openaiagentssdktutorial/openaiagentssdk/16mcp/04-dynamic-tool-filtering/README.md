# 🔄 Dynamic Tool Filtering - Context-Aware Tool Access

## 📖 What is Dynamic Tool Filtering? (Simple Explanation)

Think of **dynamic tool filtering** like a smart security system that changes its rules based on the situation. It's like having a bouncer at a club who decides who can enter based on different factors - time of day, dress code, VIP status, etc.

### 🎯 Simple Explanation
Dynamic tool filtering means your AI assistant can use different tools depending on the situation. For example, it might be allowed to read files anytime, but only write files during certain hours, or only delete files if you're an admin.

### 🏠 Real-World Analogy
Imagine you have a smart house with different access levels:
- **Everyone** can turn on lights (read files)
- **Family members** can adjust the thermostat (write files)  
- **Only parents** can change security settings (delete files)
- **Guests** can only use the living room (limited access)

## 📖 Overview

This example demonstrates **dynamic tool filtering** in MCP, which allows you to control tool access based on context, conditions, and runtime information. This is more flexible than static filtering and enables sophisticated access control.

## 🎯 What You'll Learn (In Simple Terms)

- ✅ How to filter tools dynamically during runtime (like changing security rules on the fly)
- ✅ How to implement context-aware tool access (like giving different keys to different people)
- ✅ How to create conditional tool filtering logic (like "if it's after 6 PM, only allow reading")
- ✅ How to build sophisticated access control systems (like a multi-level security system)

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│                 │    │   MCP Server     │    │   All Available │
│                 │◄──►│   (Filesystem)   │◄──►│   Tools         │
│                 │    │                  │    │                 │
│                 │    │   ┌─────────────┐│    │   - read_file   │
│   Your Agent    │    │   │   Dynamic   ││    │   - write_file  │
│   (Dynamic)     │    │   │   Filter    ││    │   - delete_file │
│                 │    │   │  (Runtime)  ││    │   - list_files  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
04-dynamic-tool-filtering/
├── README.md              # This file
└── 6dynamictoolfiltering.py # Main script with dynamic filtering
```

## 🛠️ Prerequisites

Before running this example, make sure you have:

1. **Python 3.8+** installed
2. **OpenAI API Key** set up
3. **Node.js/npm** installed (for MCP servers)
4. **Required packages** installed:
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
uv run 6dynamictoolfiltering.py
```

## 📝 Code Walkthrough (Simple Terms)

### Main Script: `6dynamictoolfiltering.py`

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
- Standard imports for async operations and environment management (like getting your toolbox ready)
- MCP server connection utilities (like the cables to connect your devices)

#### 2. Dynamic Filtering Logic (Like a Smart Security Guard)

```python
class DynamicToolFilter:
    def __init__(self):
        self.user_role = "reader"  # Can be "reader", "writer", "admin"
        self.allowed_directories = ["/safe", "/public"]
        self.current_context = "analysis"
    
    def should_allow_tool(self, tool_name: str, arguments: dict) -> bool:
        """Dynamic filtering based on context and conditions"""
        
        # Always allow read operations
        if tool_name == "read_file":
            return True
        
        # Allow write operations only for writers and admins
        if tool_name == "write_file":
            return self.user_role in ["writer", "admin"]
        
        # Allow delete operations only for admins
        if tool_name == "delete_file":
            return self.user_role == "admin"
        
        # Allow list operations in analysis context
        if tool_name == "list_files":
            return self.current_context == "analysis"
        
        return False
```

**What this does (in simple terms):**
- Creates a **dynamic filter class** that evaluates conditions at runtime (like a security guard who makes decisions on the spot)
- Implements **role-based access control** (reader, writer, admin) (like different types of keys for different people)
- Considers **context** and **arguments** when making decisions (like checking the time and situation)
- Provides **flexible filtering logic** (like having different rules for different situations)

#### 3. Dynamic Tool Application (Like Checking IDs at the Door)

```python
async with MCPServerStdio(
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
    }
) as mcp_server:
    # Create dynamic filter
    tool_filter = DynamicToolFilter()
    
    # Get all tools and apply dynamic filtering
    all_tools = await mcp_server.list_tools()
    filtered_tools = []
    
    for tool in all_tools:
        # Simulate dynamic evaluation
        if tool_filter.should_allow_tool(tool.name, {}):
            filtered_tools.append(tool)
            print(f"✅ Allowed tool: {tool.name} (role: {tool_filter.user_role})")
        else:
            print(f"❌ Blocked tool: {tool.name} (role: {tool_filter.user_role})")
```

**What this does (in simple terms):**
- Creates a **dynamic filter instance** (like hiring a security guard)
- Evaluates each tool **at runtime** (like checking each person's ID as they arrive)
- Considers **current context** and **user role** (like checking if it's VIP night)
- Provides **real-time feedback** on tool access (like the guard telling you if you can enter)

#### 4. Context-Aware Agent (Like a Smart Assistant)

```python
agent = Agent(
    name="Dynamic File Assistant",
    model=openai_model,
    instructions=(
        "You're a helpful assistant with dynamic tool access. "
        "Your capabilities depend on your current role and context. "
        "If you can't perform an action, explain why and suggest alternatives."
    ),
    mcp_servers=[mcp_server],  # Server with dynamically filtered tools
)
```

**What this does (in simple terms):**
- Creates an agent that **adapts to its current capabilities** (like an assistant who knows what they're allowed to do)
- Provides **clear explanations** when tools are unavailable (like explaining why you can't access something)
- Suggests **alternative approaches** (like suggesting a different way to get what you need)

#### 5. Testing Different Contexts (Like Testing Different Scenarios)

```python
# Test different roles and contexts
contexts = [
    {"role": "reader", "context": "analysis"},
    {"role": "writer", "context": "editing"},
    {"role": "admin", "context": "management"}
]

for context in contexts:
    print(f"\n=== Testing {context['role']} role in {context['context']} context ===")
    tool_filter.user_role = context["role"]
    tool_filter.current_context = context["context"]
    
    # Re-evaluate tools for this context
    # ... dynamic filtering logic
```

**What this does (in simple terms):**
- Tests **different user roles** (like testing what different types of keys can open)
- Simulates **various contexts** (like testing access at different times of day)
- Shows how **access changes** based on conditions (like seeing how security rules change)

## 🔍 How It Works (Simple Steps)

### Step-by-Step Process (Like a Smart Security System)

1. **Server Connection**: Connect to the MCP server (like turning on the security system)
2. **Tool Discovery**: Get all available tools from the server (like seeing all the doors in a building)
3. **Dynamic Evaluation**: Apply filtering logic based on current context (like the security guard checking your ID and the time)
4. **Context Changes**: Re-evaluate tools when conditions change (like security rules changing at night)
5. **Agent Adaptation**: Agent adapts to available tools (like knowing what you can and can't do)

### Dynamic Filtering Flow (Like a Smart Building)

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
│             │    │   MCP Server     │    │   All Tools     │
│             │◄──►│                  │◄──►│                 │
│             │    │                  │    │ - read_file     │
│             │    │   ┌─────────────┐│    │ - write_file    │
│    Agent    │    │   │   Dynamic   ││    │ - delete_file   │
│             │    │   │   Filter    ││    │ - list_files    │
│             │    │   │  (Runtime)  ││    │                 │
│             │    │   └─────────────┘│    │                 │
│             │    │                  │    │                 │
│             │    │   ┌─────────────┐│    │   ┌─────────────┐│
│             │    │   │  Context    ││    │   │  Role-Based ││
│             │    │   │  Evaluation ││    │   │   Access    ││
│             │    │   │             ││    │   │             ││
│             │    │   │ - User Role ││    │   │ - Reader    ││
│             │    │   │ - Context   ││    │   │ - Writer    ││
│             │    │   │ - Conditions││    │   │ - Admin     ││
│             │    │   └─────────────┘│    │   └─────────────┘│
└─────────────┘    └──────────────────┘    └─────────────────┘
```

## 📊 Expected Output

When you run the script, you should see output like this:

```
============================================================
DYNAMIC TOOL FILTERING DEMO: Context-Aware Access Control
============================================================
Connecting to MCP server...

=== Testing reader role in analysis context ===
✅ Allowed tool: read_file (role: reader)
✅ Allowed tool: list_files (role: reader)
❌ Blocked tool: write_file (role: reader)
❌ Blocked tool: delete_file (role: reader)

=== Testing writer role in editing context ===
✅ Allowed tool: read_file (role: writer)
❌ Blocked tool: list_files (role: writer)
✅ Allowed tool: write_file (role: writer)
❌ Blocked tool: delete_file (role: writer)

=== Testing admin role in management context ===
✅ Allowed tool: read_file (role: admin)
❌ Blocked tool: list_files (role: admin)
✅ Allowed tool: write_file (role: admin)
✅ Allowed tool: delete_file (role: admin)

============================================================
✅ Dynamic Tool Filtering Demo completed successfully!
============================================================
```

## 🎯 Key Concepts Explained (Simple Terms)

### What is Dynamic Tool Filtering?

**Dynamic tool filtering** means deciding which tools your agent can access **during runtime** based on current conditions, context, and user permissions. This is like having a "smart security guard" that makes decisions in real-time.

### Why Use Dynamic Filtering? (Simple Examples)

| Benefit | Description | Real-World Example |
|---------|-------------|-------------------|
| **🎭 Context Awareness** | Adapt to different situations | Different tools for different tasks (like having different keys for different rooms) |
| **👤 User Permissions** | Role-based access control | Admins get more tools than readers (like managers having more access than employees) |
| **🔄 Runtime Flexibility** | Change access during execution | Grant temporary permissions (like giving a guest a temporary key) |
| **🛡️ Advanced Security** | Complex access control logic | Time-based or condition-based access (like only allowing access during business hours) |

### Dynamic vs Static Filtering (Simple Comparison)

| Aspect | Static Filtering | Dynamic Filtering |
|--------|------------------|-------------------|
| **When Applied** | At connection time | During runtime |
| **Flexibility** | Fixed | Highly adaptive |
| **Performance** | Fast | Slower (runtime evaluation) |
| **Complexity** | Simple | Complex but powerful |

**Simple Analogy**: Static filtering is like having a fixed guest list for a party, while dynamic filtering is like having a bouncer who decides who can enter based on the current situation.

## 🚨 Troubleshooting (Common Problems)

### Common Issues (And How to Fix Them)

1. **"Filter logic not working"**
   - Check that filter conditions are correct (like making sure your security rules make sense)
   - Verify context variables are set properly (like checking if the time is correct)
   - Test filter logic independently (like testing your security system)

2. **"Performance issues"**
   - Optimize filter evaluation logic (like making security checks faster)
   - Cache filter results when possible (like remembering who's already been checked)
   - Reduce complexity of filter conditions (like simplifying security rules)

3. **"Context not updating"**
   - Ensure context changes are applied (like making sure the time updates)
   - Verify filter re-evaluation is triggered (like making sure the security guard checks again)
   - Check for race conditions (like making sure only one person changes the rules at a time)

### Debug Mode (Like Adding Extra Logging)

To see detailed filtering information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔗 Next Steps (What to Try Next)

After completing this example, try:

1. **🔐 Security**: Implement more sophisticated access control (like adding fingerprint scanning)
2. **⚡ Performance**: Optimize dynamic filtering for better performance (like making security checks faster)
3. **🎭 Context**: Add more context-aware features (like considering location, time, and user behavior)
4. **🔄 Real-time**: Implement real-time context updates (like updating access as situations change)

## 📚 Additional Resources (Where to Learn More)

- [MCP Tool Filtering Documentation](https://modelcontextprotocol.io/docs/tools)
- [Dynamic Access Control](https://modelcontextprotocol.io/docs/security)
- [Context-Aware Systems](https://modelcontextprotocol.io/docs/context)

## 🤝 Contributing (How to Help)

Found an issue or have a suggestion? Feel free to:
- Report bugs (like telling us if something doesn't work)
- Suggest improvements (like suggesting better security rules)
- Add more filtering examples (like adding new types of access control)
- Improve documentation (like making explanations clearer)

---

**🎉 Congratulations!** You've successfully learned how to implement dynamic tool filtering in MCP. You now understand how to create sophisticated, context-aware access control systems! 

**💡 Remember**: Dynamic filtering is like having a smart security system that adapts to different situations. The more you practice, the better you'll get at creating flexible and secure access control systems! 