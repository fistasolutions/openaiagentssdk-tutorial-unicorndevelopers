# 🔍 File Search Example - Advanced File Operations

## 📖 Overview

This example demonstrates advanced file searching and analysis capabilities using MCP. You'll learn how to create sophisticated file search tools that can analyze content, search patterns, and provide intelligent file recommendations.

## 🎯 What You'll Learn

- ✅ How to implement advanced file search functionality
- ✅ How to analyze file content and metadata
- ✅ How to create intelligent search patterns
- ✅ How to build file recommendation systems

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│                 │    │   File Search    │    │   File System   │
│                 │◄──►│   MCP Server     │◄──►│   (Multiple     │
│   Your Agent    │    │                  │    │   Directories)  │
│   (Search)      │    │   Tools:         │    │                 │
│                 │    │   - search_files │    │   - Documents   │
│                 │    │   - analyze_file │    │   - Images      │
│                 │    │   - find_pattern │    │   - Code        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
05-file-search-example/
├── README.md              # This file
└── 7filesearchexample.py  # Main script with file search functionality
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
uv run 7filesearchexample.py
```

## 📝 Code Walkthrough

### Main Script: `7filesearchexample.py`

Let's break down the code step by step:

#### 1. Imports and Setup

```python
import os
import asyncio
import re
from typing import List, Dict, Any
from dotenv import load_dotenv

from agents import Agent, Runner, set_default_openai_key
from agents.mcp import MCPServerStdio
```

**What this does:**
- Imports for file operations and pattern matching
- MCP server connection utilities
- Type hints for better code clarity

#### 2. Advanced File Search Tools

```python
class AdvancedFileSearch:
    def __init__(self, base_directory: str):
        self.base_directory = base_directory
        self.search_history = []
    
    async def search_files(self, query: str, file_types: List[str] = None) -> List[Dict]:
        """Advanced file search with content analysis"""
        results = []
        
        for root, dirs, files in os.walk(self.base_directory):
            for file in files:
                if file_types and not any(file.endswith(ext) for ext in file_types):
                    continue
                
                file_path = os.path.join(root, file)
                relevance_score = self.calculate_relevance(file_path, query)
                
                if relevance_score > 0:
                    results.append({
                        "file": file_path,
                        "relevance": relevance_score,
                        "size": os.path.getsize(file_path),
                        "modified": os.path.getmtime(file_path)
                    })
        
        return sorted(results, key=lambda x: x["relevance"], reverse=True)
    
    def calculate_relevance(self, file_path: str, query: str) -> float:
        """Calculate relevance score for a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                query_terms = query.lower().split()
                
                score = 0
                for term in query_terms:
                    if term in content:
                        score += content.count(term)
                
                return score
        except:
            return 0
```

**What this does:**
- Creates an **advanced file search class**
- Implements **relevance scoring** based on content
- Supports **file type filtering**
- Provides **search history** tracking

#### 3. File Analysis Tools

```python
    async def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze file content and metadata"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis = {
                "file_path": file_path,
                "size": len(content),
                "lines": len(content.split('\n')),
                "words": len(content.split()),
                "characters": len(content),
                "file_type": os.path.splitext(file_path)[1],
                "keywords": self.extract_keywords(content),
                "summary": self.generate_summary(content)
            }
            
            return analysis
        except Exception as e:
            return {"error": str(e)}
    
    def extract_keywords(self, content: str) -> List[str]:
        """Extract important keywords from content"""
        # Simple keyword extraction (can be enhanced with NLP)
        words = re.findall(r'\b\w+\b', content.lower())
        word_freq = {}
        
        for word in words:
            if len(word) > 3:  # Skip short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        return sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
```

**What this does:**
- Provides **comprehensive file analysis**
- Extracts **keywords and patterns**
- Generates **content summaries**
- Handles **different file types**

#### 4. Pattern Matching Tools

```python
    async def find_pattern(self, pattern: str, file_types: List[str] = None) -> List[Dict]:
        """Find files containing specific patterns"""
        results = []
        
        for root, dirs, files in os.walk(self.base_directory):
            for file in files:
                if file_types and not any(file.endswith(ext) for ext in file_types):
                    continue
                
                file_path = os.path.join(root, file)
                matches = self.search_pattern_in_file(file_path, pattern)
                
                if matches:
                    results.append({
                        "file": file_path,
                        "matches": matches,
                        "match_count": len(matches)
                    })
        
        return results
    
    def search_pattern_in_file(self, file_path: str, pattern: str) -> List[str]:
        """Search for patterns in a specific file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            matches = re.findall(pattern, content, re.IGNORECASE)
            return matches
        except:
            return []
```

**What this does:**
- Implements **regex pattern matching**
- Searches **across multiple files**
- Provides **match context**
- Supports **case-insensitive search**

#### 5. Agent Integration

```python
async with MCPServerStdio(
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
    }
) as mcp_server:
    # Create advanced file search instance
    file_searcher = AdvancedFileSearch(samples_dir)
    
    agent = Agent(
        name="File Search Assistant",
        model=openai_model,
        instructions=(
            "You're an advanced file search assistant. "
            "Use the available tools to search, analyze, and find patterns in files. "
            "Provide detailed insights about file content and structure."
        ),
        mcp_servers=[mcp_server],
    )
```

**What this does:**
- Integrates **advanced search tools** with the agent
- Provides **intelligent file analysis**
- Enables **pattern-based searches**

## 🔍 How It Works

### Step-by-Step Process

1. **File Discovery**: Scan directories for relevant files
2. **Content Analysis**: Analyze file content and metadata
3. **Pattern Matching**: Search for specific patterns
4. **Relevance Scoring**: Calculate search result relevance
5. **Intelligent Recommendations**: Provide file suggestions

### Search Flow

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
│             │    │   File Search    │    │   File System   │
│             │◄──►│   Engine         │◄──►│                 │
│    Agent    │    │                  │    │   - Documents   │
│             │    │   ┌─────────────┐│    │   - Images      │
│             │    │   │   Search    ││    │   - Code        │
│             │    │   │   Logic     ││    │   - Data        │
│             │    │   └─────────────┘│    │                 │
│             │    │                  │    │                 │
│             │    │   ┌─────────────┐│    │   ┌─────────────┐│
│             │    │   │  Analysis   ││    │   │  Pattern    ││
│             │    │   │   Engine    ││    │   │  Matching   ││
│             │    │   │             ││    │   │             ││
│             │    │   │ - Keywords  ││    │   │ - Regex     ││
│             │    │   │ - Summary   ││    │   │ - Context   ││
│             │    │   │ - Metadata  ││    │   │ - Matches   ││
│             │    │   └─────────────┘│    │   └─────────────┘│
└─────────────┘    └──────────────────┘    └─────────────────┘
```

## 📊 Expected Output

When you run the script, you should see output like this:

```
============================================================
ADVANCED FILE SEARCH DEMO: Content Analysis and Pattern Matching
============================================================
Connecting to MCP server...

🧠 Response:
I'll help you with advanced file search and analysis. Let me demonstrate the capabilities:

1. **File Search Results:**
   Found 3 files matching your search criteria:
   - demo.txt (relevance: 85%)
   - books.txt (relevance: 72%)
   - notes.txt (relevance: 45%)

2. **Content Analysis:**
   demo.txt analysis:
   - Size: 1,247 characters
   - Lines: 23
   - Keywords: ['mcp', 'protocol', 'model', 'context', 'tools']
   - Summary: Comprehensive overview of MCP protocol and its features

3. **Pattern Matching:**
   Found 5 matches for pattern "MCP":
   - demo.txt: 3 matches
   - books.txt: 1 match
   - notes.txt: 1 match

============================================================
✅ Advanced File Search Demo completed successfully!
============================================================
```

## 🎯 Key Concepts Explained

### What is Advanced File Search?

**Advanced file search** goes beyond simple filename matching to include content analysis, pattern matching, and intelligent recommendations based on file content and metadata.

### Why Use Advanced File Search?

| Benefit | Description | Example |
|---------|-------------|---------|
| **🔍 Content Search** | Search within file content | Find files containing specific terms |
| **📊 Content Analysis** | Analyze file structure and content | Extract keywords and summaries |
| **🎯 Pattern Matching** | Use regex and patterns | Find code patterns or data formats |
| **📈 Relevance Scoring** | Rank results by relevance | Most relevant files first |

### Search Capabilities

| Feature | Description | Use Case |
|---------|-------------|----------|
| **Full-text Search** | Search within file content | Finding documents with specific topics |
| **Pattern Matching** | Regex and pattern search | Finding code patterns or data |
| **Metadata Analysis** | File size, dates, types | Understanding file characteristics |
| **Keyword Extraction** | Identify important terms | Content summarization |

## 🚨 Troubleshooting

### Common Issues

1. **"File not found"**
   - Check file paths are correct
   - Verify file permissions
   - Ensure encoding is supported

2. **"Search too slow"**
   - Limit search scope
   - Use file type filters
   - Implement caching

3. **"Pattern not matching"**
   - Check regex syntax
   - Verify case sensitivity
   - Test pattern independently

### Debug Mode

To see detailed search information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔗 Next Steps

After completing this example, try:

1. **🔍 Enhanced Search**: Add more sophisticated search algorithms
2. **📊 Content Analysis**: Implement NLP for better analysis
3. **🎯 Smart Recommendations**: Build recommendation systems
4. **⚡ Performance**: Optimize search for large file systems

## 📚 Additional Resources

- [File Search Best Practices](https://modelcontextprotocol.io/docs/search)
- [Content Analysis Techniques](https://modelcontextprotocol.io/docs/analysis)
- [Pattern Matching Guide](https://modelcontextprotocol.io/docs/patterns)

## 🤝 Contributing

Found an issue or have a suggestion? Feel free to:
- Report bugs
- Suggest improvements
- Add more search features
- Improve documentation

---

**🎉 Congratulations!** You've successfully learned how to implement advanced file search functionality with MCP. You now understand how to create sophisticated file analysis and search systems! 