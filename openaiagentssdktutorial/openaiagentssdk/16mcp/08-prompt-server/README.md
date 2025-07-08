# 🚀 Prompt Server - Centralized Prompt Management

## 📖 Overview

This example demonstrates how to create a centralized prompt server using MCP. You'll learn how to build a server that manages prompts, provides prompt templates, and enables dynamic prompt generation for multiple clients.

## 🎯 What You'll Learn

- ✅ How to create a centralized prompt server
- ✅ How to manage prompt templates and versions
- ✅ How to provide dynamic prompt generation
- ✅ How to build scalable prompt infrastructure

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│                 │    │   Prompt Server  │    │   Prompt        │
│                 │◄──►│   (MCP Server)   │◄──►│   Database      │
│   Your Agent    │    │                  │    │                 │
│   (Client)      │    │   Tools:         │    │   - Templates   │
│                 │    │   - list_prompts │    │   - Versions    │
│                 │    │   - get_prompt   │    │   - Metadata    │
│                 │    │   - create_prompt│    │   - Categories  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
08-prompt-server/
├── README.md              # This file
└── 9promptserver.py       # Main script with prompt server functionality
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
uv run 9promptserver.py
```

## 📝 Code Walkthrough

### Main Script: `9promptserver.py`

Let's break down the code step by step:

#### 1. Imports and Setup

```python
import os
import asyncio
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from agents import Agent, Runner, set_default_openai_key
from agents.mcp import MCPServerStdio
```

**What this does:**
- Imports for server management and data handling
- MCP server connection utilities
- Type hints for better code clarity

#### 2. Prompt Server Implementation

```python
class PromptServer:
    def __init__(self):
        self.prompts = {}
        self.categories = {
            "code_review": "Code review and analysis prompts",
            "documentation": "Documentation generation prompts",
            "debugging": "Debugging and troubleshooting prompts",
            "testing": "Test generation and validation prompts",
            "optimization": "Performance optimization prompts"
        }
        self._initialize_default_prompts()
    
    def _initialize_default_prompts(self):
        """Initialize default prompt templates"""
        default_prompts = {
            "code_review_python": {
                "id": str(uuid.uuid4()),
                "name": "Python Code Review",
                "category": "code_review",
                "template": "Review the following Python code:\n\n{code}\n\nFocus on: {focus_areas}\n\nProvide detailed feedback on:\n- Code quality\n- Performance\n- Security\n- Best practices",
                "variables": ["code", "focus_areas"],
                "version": "1.0",
                "created_at": datetime.now().isoformat(),
                "tags": ["python", "code-review", "quality"]
            },
            "documentation_api": {
                "id": str(uuid.uuid4()),
                "name": "API Documentation",
                "category": "documentation",
                "template": "Create comprehensive API documentation for {api_name}:\n\n{api_description}\n\nInclude:\n- Endpoints and methods\n- Request/response formats\n- Authentication\n- Examples\n- Error handling",
                "variables": ["api_name", "api_description"],
                "version": "1.0",
                "created_at": datetime.now().isoformat(),
                "tags": ["api", "documentation", "swagger"]
            },
            "debugging_error": {
                "id": str(uuid.uuid4()),
                "name": "Error Debugging",
                "category": "debugging",
                "template": "Debug the following error in {language}:\n\nError: {error_message}\n\nCode:\n{code}\n\nProvide:\n- Root cause analysis\n- Step-by-step solution\n- Prevention tips",
                "variables": ["language", "error_message", "code"],
                "version": "1.0",
                "created_at": datetime.now().isoformat(),
                "tags": ["debugging", "error-handling", "troubleshooting"]
            }
        }
        
        for prompt_id, prompt_data in default_prompts.items():
            self.prompts[prompt_id] = prompt_data
```

**What this does:**
- Creates a **centralized prompt server**
- Implements **prompt categorization**
- Provides **default prompt templates**
- Supports **versioning and metadata**

#### 3. Server Operations

```python
    async def list_prompts(self, category: str = None, tags: List[str] = None) -> List[Dict[str, Any]]:
        """List available prompts with optional filtering"""
        filtered_prompts = []
        
        for prompt_id, prompt_data in self.prompts.items():
            # Apply category filter
            if category and prompt_data["category"] != category:
                continue
            
            # Apply tag filter
            if tags and not any(tag in prompt_data["tags"] for tag in tags):
                continue
            
            filtered_prompts.append({
                "id": prompt_id,
                "name": prompt_data["name"],
                "category": prompt_data["category"],
                "description": prompt_data.get("description", ""),
                "version": prompt_data["version"],
                "tags": prompt_data["tags"]
            })
        
        return filtered_prompts
    
    async def get_prompt(self, prompt_id: str, variables: Dict[str, str] = None) -> Dict[str, Any]:
        """Get a specific prompt with optional variable substitution"""
        if prompt_id not in self.prompts:
            raise ValueError(f"Prompt '{prompt_id}' not found")
        
        prompt_data = self.prompts[prompt_id].copy()
        template = prompt_data["template"]
        
        if variables:
            # Validate required variables
            missing_vars = set(prompt_data["variables"]) - set(variables.keys())
            if missing_vars:
                raise ValueError(f"Missing required variables: {missing_vars}")
            
            # Substitute variables
            for var, value in variables.items():
                template = template.replace(f"{{{var}}}", str(value))
            
            prompt_data["rendered_template"] = template
            prompt_data["variables_used"] = variables
        
        return prompt_data
```

**What this does:**
- Implements **prompt listing** with filtering
- Provides **variable validation** and substitution
- Supports **category and tag filtering**
- Returns **comprehensive prompt metadata**

#### 4. Dynamic Prompt Creation

```python
    async def create_prompt(self, name: str, template: str, variables: List[str], 
                           category: str, description: str = "", tags: List[str] = None) -> str:
        """Create a new prompt template"""
        # Validate category
        if category not in self.categories:
            raise ValueError(f"Invalid category: {category}. Available: {list(self.categories.keys())}")
        
        # Generate unique ID
        prompt_id = f"{category}_{name.lower().replace(' ', '_')}_{str(uuid.uuid4())[:8]}"
        
        # Create prompt data
        prompt_data = {
            "id": str(uuid.uuid4()),
            "name": name,
            "category": category,
            "template": template,
            "variables": variables,
            "description": description,
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "tags": tags or []
        }
        
        self.prompts[prompt_id] = prompt_data
        return prompt_id
    
    async def update_prompt(self, prompt_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing prompt"""
        if prompt_id not in self.prompts:
            raise ValueError(f"Prompt '{prompt_id}' not found")
        
        # Update allowed fields
        allowed_updates = ["template", "variables", "description", "tags"]
        for field, value in updates.items():
            if field in allowed_updates:
                self.prompts[prompt_id][field] = value
        
        # Increment version
        current_version = self.prompts[prompt_id]["version"]
        major, minor = map(int, current_version.split("."))
        self.prompts[prompt_id]["version"] = f"{major}.{minor + 1}"
        
        return True
```

**What this does:**
- Enables **dynamic prompt creation**
- Implements **prompt updating** with versioning
- Provides **category validation**
- Supports **metadata management**

#### 5. Advanced Features

```python
    async def search_prompts(self, query: str) -> List[Dict[str, Any]]:
        """Search prompts by name, description, or tags"""
        results = []
        query_lower = query.lower()
        
        for prompt_id, prompt_data in self.prompts.items():
            # Search in name
            if query_lower in prompt_data["name"].lower():
                results.append(prompt_data)
                continue
            
            # Search in description
            if query_lower in prompt_data.get("description", "").lower():
                results.append(prompt_data)
                continue
            
            # Search in tags
            if any(query_lower in tag.lower() for tag in prompt_data["tags"]):
                results.append(prompt_data)
                continue
        
        return results
    
    async def get_prompt_statistics(self) -> Dict[str, Any]:
        """Get server statistics"""
        total_prompts = len(self.prompts)
        categories_count = {}
        tags_count = {}
        
        for prompt_data in self.prompts.values():
            # Count by category
            category = prompt_data["category"]
            categories_count[category] = categories_count.get(category, 0) + 1
            
            # Count by tags
            for tag in prompt_data["tags"]:
                tags_count[tag] = tags_count.get(tag, 0) + 1
        
        return {
            "total_prompts": total_prompts,
            "categories": categories_count,
            "popular_tags": sorted(tags_count.items(), key=lambda x: x[1], reverse=True)[:10],
            "server_uptime": datetime.now().isoformat()
        }
```

**What this does:**
- Implements **prompt search** functionality
- Provides **server statistics**
- Supports **tag-based analysis**
- Enables **usage tracking**

#### 6. MCP Server Integration

```python
async def main():
    # Create prompt server
    prompt_server = PromptServer()
    
    # Mock MCP server for prompt server
    class MockPromptServer:
        def __init__(self, server):
            self.server = server
        
        async def list_tools(self):
            return [
                type('Tool', (), {
                    'name': 'list_prompts',
                    'description': 'List available prompts with optional filtering'
                })(),
                type('Tool', (), {
                    'name': 'get_prompt',
                    'description': 'Get a specific prompt with variable substitution'
                })(),
                type('Tool', (), {
                    'name': 'create_prompt',
                    'description': 'Create a new prompt template'
                })(),
                type('Tool', (), {
                    'name': 'search_prompts',
                    'description': 'Search prompts by query'
                })()
            ]
    
    mcp_server = MockPromptServer(prompt_server)
    
    agent = Agent(
        name="Prompt Server Assistant",
        model=openai_model,
        instructions=(
            "You're a prompt server assistant. "
            "Help users discover, create, and manage prompts. "
            "Provide guidance on prompt organization and best practices."
        ),
        mcp_servers=[mcp_server],
    )
    
    # Demonstrate prompt server capabilities
    await demonstrate_prompt_server(agent, prompt_server)
```

**What this does:**
- Creates a **mock prompt server MCP server**
- Integrates **prompt server** with the agent
- Provides **prompt management guidance**
- Demonstrates **server capabilities**

## 🔍 How It Works

### Step-by-Step Process

1. **Server Initialization**: Set up prompt database and categories
2. **Prompt Discovery**: List and search available prompts
3. **Template Retrieval**: Get prompts with variable substitution
4. **Dynamic Creation**: Create new prompt templates
5. **Version Management**: Track prompt versions and updates

### Prompt Server Flow

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
│             │    │   Prompt Server  │    │   Prompt        │
│             │◄──►│   (MCP Server)   │◄──►│   Database      │
│    Agent    │    │                  │    │                 │
│             │    │   ┌─────────────┐│    │   - Templates   │
│             │    │   │   Prompt    ││    │   - Versions    │
│             │    │   │   Manager   ││    │   - Metadata    │
│             │    │   └─────────────┘│    │   - Categories  │
│             │    │                  │    │                 │
│             │    │   ┌─────────────┐│    │   ┌─────────────┐│
│             │    │   │  Search &   ││    │   │  Statistics ││
│             │    │   │  Filter     ││    │   │  & Analytics││
│             │    │   │             ││    │   │             ││
│             │    │   │ - Query     ││    │   │ - Usage     ││
│             │    │   │ - Category  ││    │   │ - Popular   ││
│             │    │   │ - Tags      ││    │   │ - Trends    ││
│             │    │   └─────────────┘│    │   └─────────────┘│
└─────────────┘    └──────────────────┘    └─────────────────┘
```

## 📊 Expected Output

When you run the script, you should see output like this:

```
============================================================
PROMPT SERVER DEMO: Centralized Prompt Management
============================================================

🧠 Response:
I'll help you with the prompt server and demonstrate its capabilities:

1. **Available Prompts:**
   - code_review_python: Python Code Review (v1.0)
   - documentation_api: API Documentation (v1.0)
   - debugging_error: Error Debugging (v1.0)

2. **Categories:**
   - code_review: Code review and analysis prompts
   - documentation: Documentation generation prompts
   - debugging: Debugging and troubleshooting prompts

3. **Prompt Example (Python Code Review):**
   Review the following Python code:
   
   def calculate_fibonacci(n):
       if n <= 1:
           return n
       return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
   
   Focus on: performance, readability, error handling
   
   Provide detailed feedback on:
   - Code quality
   - Performance
   - Security
   - Best practices

4. **Server Statistics:**
   - Total prompts: 3
   - Categories: {'code_review': 1, 'documentation': 1, 'debugging': 1}
   - Popular tags: [('python', 1), ('code-review', 1), ('api', 1)]

============================================================
✅ Prompt Server Demo completed successfully!
============================================================
```

## 🎯 Key Concepts Explained

### What is a Prompt Server?

A **prompt server** is a centralized system that manages, stores, and serves prompt templates. It provides a unified interface for accessing prompts across multiple applications and enables collaborative prompt development.

### Why Use a Prompt Server?

| Benefit | Description | Example |
|---------|-------------|---------|
| **🏢 Centralization** | Single source of truth for prompts | Consistent prompts across teams |
| **🔄 Reusability** | Share prompts across projects | Standard templates for common tasks |
| **📈 Versioning** | Track prompt evolution | Maintain prompt history |
| **🔍 Discovery** | Search and filter prompts | Find relevant prompts quickly |

### Server Capabilities

| Feature | Description | Use Case |
|---------|-------------|----------|
| **Template Management** | Store and organize prompt templates | Centralized prompt library |
| **Variable Substitution** | Dynamic prompt generation | Personalized prompts |
| **Search & Filter** | Find relevant prompts | Prompt discovery |
| **Version Control** | Track prompt changes | Prompt evolution |

## 🚨 Troubleshooting

### Common Issues

1. **"Prompt not found"**
   - Check prompt ID spelling
   - Verify prompt exists in server
   - Use list_prompts to see available options

2. **"Invalid category"**
   - Check category name spelling
   - Use available categories from server
   - Create new category if needed

3. **"Missing variables"**
   - Check required variables
   - Provide all necessary parameters
   - Verify variable names match template

### Debug Mode

To see detailed server information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔗 Next Steps

After completing this example, try:

1. **🗄️ Database Integration**: Connect to a real database
2. **🔐 Authentication**: Add user authentication and permissions
3. **📊 Analytics**: Implement usage analytics and metrics
4. **🤝 Collaboration**: Add multi-user prompt editing

## 📚 Additional Resources

- [Prompt Server Architecture](https://modelcontextprotocol.io/docs/server)
- [Centralized Prompt Management](https://modelcontextprotocol.io/docs/management)
- [Prompt Versioning](https://modelcontextprotocol.io/docs/versioning)

## 🤝 Contributing

Found an issue or have a suggestion? Feel free to:
- Report bugs
- Suggest improvements
- Add more server features
- Improve documentation

---

**🎉 Congratulations!** You've successfully learned how to create a centralized prompt server with MCP. You now understand how to build scalable prompt management infrastructure! 