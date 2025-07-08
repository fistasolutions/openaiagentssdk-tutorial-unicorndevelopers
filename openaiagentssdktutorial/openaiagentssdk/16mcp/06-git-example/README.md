# 🐙 Git Repository Analysis - Version Control Integration

## 📖 Overview

This example demonstrates how to integrate Git repository analysis with MCP. You'll learn how to create tools that can analyze Git repositories, track changes, and provide insights about code evolution and collaboration patterns.

## 🎯 What You'll Learn

- ✅ How to integrate Git operations with MCP
- ✅ How to analyze repository history and changes
- ✅ How to track code evolution and collaboration
- ✅ How to build Git-aware development tools

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│                 │    │   Git MCP        │    │   Git           │
│                 │◄──►│   Server         │◄──►│   Repository    │
│   Your Agent    │    │                  │    │                 │
│   (Git-aware)   │    │   Tools:         │    │   - Commits     │
│                 │    │   - git_status   │    │   - Branches    │
│                 │    │   - git_log      │    │   - Files       │
│                 │    │   - git_diff     │    │   - History     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
06-git-example/
├── README.md              # This file
└── 8gitexample.py         # Main script with Git analysis functionality
```

## 🛠️ Prerequisites

Before running this example, make sure you have:

1. **Python 3.8+** installed
2. **OpenAI API Key** set up
3. **Node.js/npm** installed (for MCP servers)
4. **Git** installed and configured
5. **Required packages** installed:
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
uv run 8gitexample.py
```

## 📝 Code Walkthrough

### Main Script: `8gitexample.py`

Let's break down the code step by step:

#### 1. Imports and Setup

```python
import os
import asyncio
import subprocess
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from agents import Agent, Runner, set_default_openai_key
from agents.mcp import MCPServerStdio
```

**What this does:**
- Imports for Git operations and subprocess management
- MCP server connection utilities
- Type hints for better code clarity

#### 2. Git Analysis Tools

```python
class GitRepositoryAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.git_commands = {
            "uvx": "uvx",
            "npx": "npx"
        }
    
    async def analyze_repository(self) -> Dict[str, Any]:
        """Comprehensive repository analysis"""
        analysis = {
            "repository": self.repo_path,
            "status": await self.get_git_status(),
            "branches": await self.get_branches(),
            "recent_commits": await self.get_recent_commits(),
            "contributors": await self.get_contributors(),
            "file_changes": await self.get_file_changes()
        }
        return analysis
    
    async def get_git_status(self) -> Dict[str, Any]:
        """Get current Git status"""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            status = {
                "clean": result.stdout.strip() == "",
                "modified_files": [],
                "untracked_files": [],
                "staged_files": []
            }
            
            for line in result.stdout.strip().split('\n'):
                if line:
                    status_code = line[:2]
                    filename = line[3:]
                    
                    if status_code.startswith('M'):
                        status["modified_files"].append(filename)
                    elif status_code.startswith('??'):
                        status["untracked_files"].append(filename)
                    elif status_code.startswith('A'):
                        status["staged_files"].append(filename)
            
            return status
        except Exception as e:
            return {"error": str(e)}
```

**What this does:**
- Creates a **Git repository analyzer class**
- Implements **comprehensive Git status checking**
- Provides **detailed file state analysis**
- Handles **different Git states** (modified, untracked, staged)

#### 3. Repository History Analysis

```python
    async def get_recent_commits(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent commit history"""
        try:
            result = subprocess.run(
                ["git", "log", f"--max-count={limit}", "--pretty=format:%H|%an|%ad|%s"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split('|')
                    if len(parts) >= 4:
                        commits.append({
                            "hash": parts[0],
                            "author": parts[1],
                            "date": parts[2],
                            "message": parts[3]
                        })
            
            return commits
        except Exception as e:
            return [{"error": str(e)}]
    
    async def get_contributors(self) -> List[Dict[str, Any]]:
        """Get repository contributors"""
        try:
            result = subprocess.run(
                ["git", "shortlog", "-sn"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            contributors = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        contributors.append({
                            "name": parts[1],
                            "commits": int(parts[0])
                        })
            
            return contributors
        except Exception as e:
            return [{"error": str(e)}]
```

**What this does:**
- Analyzes **commit history** and patterns
- Identifies **contributors** and their activity
- Provides **temporal analysis** of changes
- Tracks **collaboration patterns**

#### 4. Branch and File Analysis

```python
    async def get_branches(self) -> List[Dict[str, Any]]:
        """Get repository branches"""
        try:
            result = subprocess.run(
                ["git", "branch", "-a"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            branches = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    is_current = line.startswith('*')
                    branch_name = line.strip().replace('* ', '')
                    branches.append({
                        "name": branch_name,
                        "current": is_current
                    })
            
            return branches
        except Exception as e:
            return [{"error": str(e)}]
    
    async def get_file_changes(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get recent file changes"""
        try:
            result = subprocess.run(
                ["git", "log", f"--since={days} days ago", "--name-only", "--pretty=format:"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            file_changes = {}
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    file_changes[line.strip()] = file_changes.get(line.strip(), 0) + 1
            
            return [
                {"file": file, "changes": count}
                for file, count in sorted(file_changes.items(), key=lambda x: x[1], reverse=True)
            ]
        except Exception as e:
            return [{"error": str(e)}]
```

**What this does:**
- Analyzes **branch structure** and relationships
- Tracks **file change frequency**
- Identifies **most active files**
- Provides **temporal change patterns**

#### 5. MCP Server Integration

```python
async def main():
    # Try different MCP Git servers
    git_servers = [
        {
            "name": "uvx Git Server",
            "command": "uvx",
            "args": ["-y", "@modelcontextprotocol/server-git", "."]
        },
        {
            "name": "npx Git Server", 
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-git", "."]
        }
    ]
    
    for server_config in git_servers:
        try:
            print(f"\n🔄 Trying {server_config['name']}...")
            
            async with MCPServerStdio(
                params={
                    "command": server_config["command"],
                    "args": server_config["args"],
                }
            ) as mcp_server:
                # Test connection
                tools = await mcp_server.list_tools()
                print(f"✅ Connected to {server_config['name']}")
                print(f"📋 Available tools: {[tool.name for tool in tools]}")
                
                # Create Git analyzer
                git_analyzer = GitRepositoryAnalyzer(".")
                
                agent = Agent(
                    name="Git Repository Assistant",
                    model=openai_model,
                    instructions=(
                        "You're a Git repository analysis assistant. "
                        "Use the available tools to analyze repository status, "
                        "history, and provide insights about code evolution."
                    ),
                    mcp_servers=[mcp_server],
                )
                
                # Run analysis
                await run_agent(agent, git_analyzer)
                break  # Success, exit loop
                
        except Exception as e:
            print(f"❌ Failed to connect to {server_config['name']}: {e}")
            continue
```

**What this does:**
- Tries **multiple MCP Git servers** (uvx and npx)
- Provides **fallback options** for different environments
- Integrates **Git analysis** with MCP tools
- Creates **Git-aware agents**

## 🔍 How It Works

### Step-by-Step Process

1. **Repository Detection**: Identify and validate Git repository
2. **Status Analysis**: Check current repository state
3. **History Analysis**: Analyze commit history and patterns
4. **Contributor Analysis**: Identify team members and activity
5. **File Analysis**: Track file changes and evolution

### Git Analysis Flow

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
│             │    │   Git MCP        │    │   Git           │
│             │◄──►│   Server         │◄──►│   Repository    │
│    Agent    │    │                  │    │                 │
│             │    │   ┌─────────────┐│    │   - Commits     │
│             │    │   │   Git       ││    │   - Branches    │
│             │    │   │   Tools     ││    │   - Files       │
│             │    │   └─────────────┘│    │   - History     │
│             │    │                  │    │                 │
│             │    │   ┌─────────────┐│    │   ┌─────────────┐│
│             │    │   │  Analysis   ││    │   │  History    ││
│             │    │   │   Engine    ││    │   │  Tracking   ││
│             │    │   │             ││    │   │             ││
│             │    │   │ - Status    ││    │   │ - Commits   ││
│             │    │   │ - Branches  ││    │   │ - Authors   ││
│             │    │   │ - Changes   ││    │   │ - Patterns  ││
│             │    │   └─────────────┘│    │   └─────────────┘│
└─────────────┘    └──────────────────┘    └─────────────────┘
```

## 📊 Expected Output

When you run the script, you should see output like this:

```
============================================================
GIT REPOSITORY ANALYSIS DEMO: Version Control Integration
============================================================

🔄 Trying uvx Git Server...
✅ Connected to uvx Git Server
📋 Available tools: ['git_status', 'git_log', 'git_diff', 'git_branch']

🧠 Response:
I'll analyze your Git repository and provide comprehensive insights:

1. **Repository Status:**
   - Clean working directory: ✅
   - Modified files: 2 (main.py, README.md)
   - Untracked files: 1 (new_feature.py)
   - Staged files: 0

2. **Recent Activity:**
   - Last 5 commits:
     * "Add MCP integration" (2 hours ago)
     * "Fix import issues" (1 day ago)
     * "Update documentation" (3 days ago)

3. **Contributors:**
   - John Doe: 15 commits
   - Jane Smith: 8 commits
   - Team Lead: 3 commits

4. **File Changes (Last 30 days):**
   - main.py: 12 changes
   - README.md: 8 changes
   - config.py: 5 changes

============================================================
✅ Git Repository Analysis Demo completed successfully!
============================================================
```

## 🎯 Key Concepts Explained

### What is Git Repository Analysis?

**Git repository analysis** involves examining version control data to understand code evolution, collaboration patterns, and project health. This includes analyzing commits, branches, contributors, and file changes over time.

### Why Use Git Analysis?

| Benefit | Description | Example |
|---------|-------------|---------|
| **📈 Project Health** | Monitor code evolution | Track feature development |
| **👥 Collaboration** | Understand team dynamics | Identify key contributors |
| **🔍 Code Quality** | Analyze change patterns | Detect problematic areas |
| **📊 Metrics** | Generate development metrics | Measure productivity |

### Analysis Capabilities

| Feature | Description | Use Case |
|---------|-------------|----------|
| **Commit Analysis** | Analyze commit history | Understand development timeline |
| **Contributor Tracking** | Monitor team activity | Identify key team members |
| **File Change Tracking** | Track file modifications | Identify most active components |
| **Branch Analysis** | Understand branch structure | Manage feature development |

## 🚨 Troubleshooting

### Common Issues

1. **"Not a Git repository"**
   - Ensure you're in a Git repository
   - Run `git init` if needed
   - Check repository path

2. **"Git server not found"**
   - Install required Git MCP server
   - Try alternative server (uvx vs npx)
   - Check network connectivity

3. **"Permission denied"**
   - Check Git repository permissions
   - Verify user access rights
   - Ensure proper Git configuration

### Debug Mode

To see detailed Git information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔗 Next Steps

After completing this example, try:

1. **📊 Advanced Metrics**: Add more sophisticated Git metrics
2. **🔍 Code Quality**: Implement code quality analysis
3. **📈 Visualization**: Create Git history visualizations
4. **🤖 Automation**: Build automated Git analysis tools

## 📚 Additional Resources

- [Git MCP Server Documentation](https://modelcontextprotocol.io/docs/git)
- [Repository Analysis Best Practices](https://modelcontextprotocol.io/docs/analysis)
- [Version Control Integration](https://modelcontextprotocol.io/docs/vcs)

## 🤝 Contributing

Found an issue or have a suggestion? Feel free to:
- Report bugs
- Suggest improvements
- Add more Git analysis features
- Improve documentation

---

**🎉 Congratulations!** You've successfully learned how to integrate Git repository analysis with MCP. You now understand how to create sophisticated version control analysis tools! 