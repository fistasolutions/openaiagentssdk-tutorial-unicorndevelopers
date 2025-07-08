# 💬 Prompts Example - Dynamic Prompt Management

## 📖 Overview

This example demonstrates how to work with prompts in MCP. You'll learn how to create, manage, and use dynamic prompts that can be customized based on context, user preferences, and specific use cases.

## 🎯 What You'll Learn

- ✅ How to create and manage dynamic prompts
- ✅ How to implement prompt templates and variables
- ✅ How to build context-aware prompt systems
- ✅ How to integrate prompts with MCP tools

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│                 │    │   Prompt MCP     │    │   Prompt        │
│                 │◄──►│   Server         │◄──►│   Templates     │
│   Your Agent    │    │                  │    │                 │
│   (Prompt-aware)│    │   Tools:         │    │   - Templates   │
│                 │    │   - list_prompts │    │   - Variables   │
│                 │    │   - get_prompt   │    │   - Context     │
│                 │    │   - create_prompt│    │   - Custom      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
07-prompts-example/
├── README.md              # This file
└── 7prompts.py            # Main script with prompt management functionality
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
uv run 7prompts.py
```

## 📝 Code Walkthrough

### Main Script: `7prompts.py`

Let's break down the code step by step:

#### 1. Imports and Setup

```python
import os
import asyncio
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from agents import Agent, Runner, set_default_openai_key
from agents.mcp import MCPServerStdio
```

**What this does:**
- Imports for prompt management and JSON handling
- MCP server connection utilities
- Type hints for better code clarity

#### 2. Prompt Management System

```python
class PromptManager:
    def __init__(self):
        self.prompts = {
            "code_review": {
                "template": "Review the following code for {language}:\n\n{code}\n\nFocus on: {focus_areas}",
                "variables": ["language", "code", "focus_areas"],
                "description": "Code review prompt with customizable focus areas"
            },
            "documentation": {
                "template": "Create documentation for {component} in {format} format. Include: {sections}",
                "variables": ["component", "format", "sections"],
                "description": "Documentation generation prompt"
            },
            "debugging": {
                "template": "Debug the following {language} code:\n\n{code}\n\nError: {error_message}\n\nProvide step-by-step solution.",
                "variables": ["language", "code", "error_message"],
                "description": "Debugging assistance prompt"
            }
        }
    
    async def list_prompts(self) -> List[Dict[str, Any]]:
        """List all available prompts"""
        return [
            {
                "name": name,
                "description": prompt["description"],
                "variables": prompt["variables"]
            }
            for name, prompt in self.prompts.items()
        ]
    
    async def get_prompt(self, name: str, variables: Dict[str, str] = None) -> str:
        """Get a prompt with optional variable substitution"""
        if name not in self.prompts:
            raise ValueError(f"Prompt '{name}' not found")
        
        prompt = self.prompts[name]
        template = prompt["template"]
        
        if variables:
            # Simple variable substitution
            for var, value in variables.items():
                template = template.replace(f"{{{var}}}", str(value))
        
        return template
```

**What this does:**
- Creates a **prompt management system**
- Implements **template-based prompts**
- Supports **variable substitution**
- Provides **prompt cataloging**

#### 3. Dynamic Prompt Generation

```python
    async def create_prompt(self, template: str, variables: List[str], description: str) -> str:
        """Create a new prompt template"""
        prompt_id = f"custom_{len(self.prompts)}"
        
        self.prompts[prompt_id] = {
            "template": template,
            "variables": variables,
            "description": description
        }
        
        return prompt_id
    
    async def analyze_prompt(self, prompt_text: str) -> Dict[str, Any]:
        """Analyze a prompt for structure and variables"""
        analysis = {
            "length": len(prompt_text),
            "variables": [],
            "sections": [],
            "complexity": "simple"
        }
        
        # Extract variables (simple pattern matching)
        import re
        variables = re.findall(r'\{(\w+)\}', prompt_text)
        analysis["variables"] = list(set(variables))
        
        # Analyze sections
        sections = prompt_text.split('\n\n')
        analysis["sections"] = [s.strip() for s in sections if s.strip()]
        
        # Determine complexity
        if len(analysis["variables"]) > 5 or len(analysis["sections"]) > 3:
            analysis["complexity"] = "complex"
        elif len(analysis["variables"]) > 2 or len(analysis["sections"]) > 1:
            analysis["complexity"] = "moderate"
        
        return analysis
```

**What this does:**
- Enables **dynamic prompt creation**
- Provides **prompt analysis** capabilities
- Implements **complexity assessment**
- Supports **section identification**

#### 4. Context-Aware Prompts

```python
    async def get_contextual_prompt(self, context: Dict[str, Any]) -> str:
        """Generate context-aware prompts"""
        user_role = context.get("role", "developer")
        task_type = context.get("task_type", "general")
        experience_level = context.get("experience", "intermediate")
        
        if task_type == "code_review":
            if experience_level == "beginner":
                return "Please review this code and explain each part in simple terms..."
            elif experience_level == "expert":
                return "Perform a thorough code review focusing on performance, security, and best practices..."
            else:
                return "Review this code for correctness, readability, and potential improvements..."
        
        elif task_type == "debugging":
            return f"As a {user_role}, help debug this issue with {experience_level} level explanations..."
        
        else:
            return "Please help with this task..."
    
    async def optimize_prompt(self, original_prompt: str, feedback: str) -> str:
        """Optimize a prompt based on feedback"""
        # Simple optimization logic
        optimized = original_prompt
        
        if "too vague" in feedback.lower():
            optimized += "\n\nPlease be specific and provide concrete examples."
        
        if "too long" in feedback.lower():
            # Split into shorter sections
            sections = optimized.split('\n\n')
            optimized = '\n\n'.join(sections[:2])  # Keep first two sections
        
        if "missing context" in feedback.lower():
            optimized = "Context: " + optimized
        
        return optimized
```

**What this does:**
- Implements **context-aware prompt generation**
- Provides **prompt optimization** based on feedback
- Supports **role-based customization**
- Enables **experience-level adaptation**

#### 5. MCP Server Integration

```python
async def main():
    # Create prompt manager
    prompt_manager = PromptManager()
    
    # Mock MCP server for prompts
    class MockPromptServer:
        async def list_tools(self):
            return [
                type('Tool', (), {
                    'name': 'list_prompts',
                    'description': 'List all available prompts'
                })(),
                type('Tool', (), {
                    'name': 'get_prompt',
                    'description': 'Get a specific prompt with variables'
                })(),
                type('Tool', (), {
                    'name': 'create_prompt',
                    'description': 'Create a new prompt template'
                })()
            ]
    
    mcp_server = MockPromptServer()
    
    agent = Agent(
        name="Prompt Management Assistant",
        model=openai_model,
        instructions=(
            "You're a prompt management assistant. "
            "Help users create, customize, and optimize prompts for different tasks. "
            "Provide guidance on prompt engineering best practices."
        ),
        mcp_servers=[mcp_server],
    )
    
    # Demonstrate prompt capabilities
    await demonstrate_prompts(agent, prompt_manager)
```

**What this does:**
- Creates a **mock prompt MCP server**
- Integrates **prompt management** with the agent
- Provides **prompt engineering guidance**
- Demonstrates **prompt capabilities**

## 🔍 How It Works

### Step-by-Step Process

1. **Prompt Discovery**: List available prompt templates
2. **Variable Substitution**: Fill in prompt variables
3. **Context Analysis**: Adapt prompts to user context
4. **Prompt Optimization**: Improve prompts based on feedback
5. **Dynamic Generation**: Create new prompts as needed

### Prompt Management Flow

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
│             │    │   Prompt MCP     │    │   Prompt        │
│             │◄──►│   Server         │◄──►│   Templates     │
│    Agent    │    │                  │    │                 │
│             │    │   ┌─────────────┐│    │   - Code Review │
│             │    │   │   Prompt    ││    │   - Documentation│
│             │    │   │   Manager   ││    │   - Debugging   │
│             │    │   └─────────────┘│    │   - Custom      │
│             │    │                  │    │                 │
│             │    │   ┌─────────────┐│    │   ┌─────────────┐│
│             │    │   │  Context    ││    │   │  Variables  ││
│             │    │   │  Engine     ││    │   │  & Templates││
│             │    │   │             ││    │   │             ││
│             │    │   │ - User Role ││    │   │ - Language  ││
│             │    │   │ - Experience││    │   │ - Focus     ││
│             │    │   │ - Task Type ││    │   │ - Format    ││
│             │    │   └─────────────┘│    │   └─────────────┘│
└─────────────┘    └──────────────────┘    └─────────────────┘
```

## 📊 Expected Output

When you run the script, you should see output like this:

```
============================================================
PROMPT MANAGEMENT DEMO: Dynamic Prompt Templates
============================================================

🧠 Response:
I'll help you with prompt management and demonstrate the capabilities:

1. **Available Prompts:**
   - code_review: Code review prompt with customizable focus areas
   - documentation: Documentation generation prompt
   - debugging: Debugging assistance prompt

2. **Prompt Examples:**
   
   **Code Review Prompt:**
   Review the following code for Python:
   
   def calculate_sum(numbers):
       return sum(numbers)
   
   Focus on: performance, readability, error handling

3. **Context-Aware Prompt:**
   As a senior developer, help debug this issue with expert-level explanations...

4. **Prompt Analysis:**
   - Length: 156 characters
   - Variables: ['language', 'code', 'focus_areas']
   - Sections: 3
   - Complexity: moderate

============================================================
✅ Prompt Management Demo completed successfully!
============================================================
```

## 🎯 Key Concepts Explained

### What is Prompt Management?

**Prompt management** involves creating, organizing, and optimizing prompts for different use cases. This includes template-based prompts, variable substitution, and context-aware customization.

### Why Use Prompt Management?

| Benefit | Description | Example |
|---------|-------------|---------|
| **🔄 Reusability** | Use templates across projects | Standard code review prompts |
| **⚙️ Customization** | Adapt prompts to specific needs | Role-based prompt variations |
| **📈 Consistency** | Maintain prompt quality | Standardized templates |
| **🎯 Optimization** | Improve prompts over time | Feedback-based improvements |

### Prompt Capabilities

| Feature | Description | Use Case |
|---------|-------------|----------|
| **Template System** | Reusable prompt templates | Standardized prompts |
| **Variable Substitution** | Dynamic content insertion | Personalized prompts |
| **Context Awareness** | Adapt to user context | Role-based prompts |
| **Optimization** | Improve based on feedback | Continuous improvement |

## 🚨 Troubleshooting

### Common Issues

1. **"Prompt not found"**
   - Check prompt name spelling
   - Verify prompt exists in catalog
   - Use list_prompts to see available options

2. **"Variable substitution failed"**
   - Check variable names match template
   - Ensure all required variables provided
   - Verify variable format

3. **"Context not applied"**
   - Check context parameters
   - Verify context-aware logic
   - Test with different contexts

### Debug Mode

To see detailed prompt information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔗 Next Steps

After completing this example, try:

1. **🎨 Advanced Templates**: Create more sophisticated prompt templates
2. **🤖 AI Optimization**: Use AI to optimize prompts automatically
3. **📊 Analytics**: Track prompt performance and usage
4. **🔗 Integration**: Integrate with other MCP tools

## 📚 Additional Resources

- [Prompt Engineering Best Practices](https://modelcontextprotocol.io/docs/prompts)
- [Template Systems](https://modelcontextprotocol.io/docs/templates)
- [Context-Aware Systems](https://modelcontextprotocol.io/docs/context)

## 🤝 Contributing

Found an issue or have a suggestion? Feel free to:
- Report bugs
- Suggest improvements
- Add more prompt templates
- Improve documentation

---

**🎉 Congratulations!** You've successfully learned how to implement prompt management with MCP. You now understand how to create sophisticated, dynamic prompt systems! 