# 🔍 File Search Tool

## 📋 Overview
This example demonstrates how to use the **FileSearchTool** to enable agents to search through files using vector embeddings. The agent can find relevant information from a specified vector store.

## 🎯 Key Concepts

### **FileSearchTool**
- **Purpose**: Enables agents to search through files using semantic search
- **Vector Store**: Uses pre-indexed file embeddings for fast retrieval
- **Max Results**: Configurable limit on number of search results returned
- **Vector Store IDs**: Specifies which vector store to search in

### **Vector Search**
- Files are converted to embeddings and stored in a vector database
- Semantic search finds files based on meaning, not just keywords
- Enables finding relevant information even with different word choices

## 📁 Code Structure

```python
from agents import Agent, FileSearchTool, Runner, set_default_openai_key
from dotenv import load_dotenv
import os
import asyncio

# Environment setup
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
model = os.environ.get("OPENAI_MODEL")

# Agent configuration with FileSearchTool
agent = Agent(
    name="Assistant",
    tools=[
        FileSearchTool(
            max_num_results=3,  # Limit search results
            vector_store_ids=["vs_6859b7221d108191884ab0709e033181"],  # Vector store ID
        ),
    ],
    model=model
)

# Main execution
async def main():
    result = await Runner.run(agent, "What is Current position of Muhammad Usman")
    print(result.final_output)
```

## 🔧 Configuration Options

### **FileSearchTool Parameters**
- `max_num_results`: Maximum number of search results to return (default: 10)
- `vector_store_ids`: List of vector store IDs to search in
- `search_type`: Type of search to perform (semantic, keyword, hybrid)

### **Vector Store Setup**
```python
# Example vector store configuration
FileSearchTool(
    max_num_results=5,
    vector_store_ids=["your_vector_store_id"],
    search_type="semantic"  # or "keyword", "hybrid"
)
```

## 🚀 Usage

### **Basic Usage**
```bash
uv run 1filesearch.py
```

### **Example Queries**
- "What is Current position of Muhammad Usman"
- "Find information about project status"
- "Search for budget reports"
- "Look for meeting notes from last week"

## 🛠️ Customization Ideas

### **1. Multiple Vector Stores**
```python
tools=[
    FileSearchTool(
        max_num_results=3,
        vector_store_ids=["vs_project_files", "vs_documentation", "vs_reports"],
    ),
]
```

### **2. Different Search Types**
```python
# Semantic search (meaning-based)
FileSearchTool(search_type="semantic")

# Keyword search (exact match)
FileSearchTool(search_type="keyword")

# Hybrid search (both semantic and keyword)
FileSearchTool(search_type="hybrid")
```

### **3. Custom Result Processing**
```python
async def main():
    result = await Runner.run(agent, "Search for user information")
    
    # Access individual search results
    for item in result.new_items:
        if hasattr(item, 'output'):
            print(f"Found: {item.output}")
```

## 🔍 How It Works

1. **Query Processing**: User query is converted to embeddings
2. **Vector Search**: System searches vector store for similar embeddings
3. **Result Retrieval**: Top matching files are retrieved
4. **Content Extraction**: Relevant content is extracted from files
5. **Response Generation**: Agent uses retrieved information to answer

## 📊 Vector Store Management

### **Creating Vector Stores**
```python
# Example: Creating a vector store for documents
from agents import create_vector_store

vector_store = await create_vector_store(
    name="project_documents",
    files=["doc1.pdf", "doc2.txt", "doc3.docx"]
)
```

### **Updating Vector Stores**
```python
# Add new files to existing vector store
await vector_store.add_files(["new_document.pdf"])
```

## ⚠️ Important Notes

### **Prerequisites**
- Vector store must be pre-created and populated with file embeddings
- Vector store ID must be valid and accessible
- Files must be properly indexed in the vector store

### **Performance Considerations**
- Larger `max_num_results` values increase response time
- Multiple vector stores may slow down searches
- Semantic search is more computationally intensive than keyword search

### **Security**
- Ensure vector stores contain only authorized files
- Validate vector store IDs before use
- Consider access controls for sensitive documents

## 🐛 Troubleshooting

### **Common Issues**

1. **"Vector store not found"**
   - Verify vector store ID is correct
   - Ensure vector store exists and is accessible

2. **"No results found"**
   - Check if files are properly indexed
   - Try different search terms
   - Verify vector store contains relevant content

3. **"Permission denied"**
   - Check vector store access permissions
   - Verify API key has necessary permissions

### **Debug Mode**
```python
import logging
logging.getLogger("openai.agents").setLevel(logging.DEBUG)
```

## 🔗 Related Examples

- **WebSearchTool**: Search the internet for current information
- **CodeInterpreterTool**: Execute and analyze code
- **CustomFunctionTool**: Create custom search functions

## 📚 Best Practices

1. **Use Descriptive Vector Store Names**: Makes management easier
2. **Limit Search Results**: Balance between completeness and performance
3. **Regular Updates**: Keep vector stores current with new files
4. **Error Handling**: Implement fallbacks for search failures
5. **Security**: Validate all inputs and outputs

## 🎓 Learning Path

1. Start with basic file search
2. Experiment with different search types
3. Learn vector store management
4. Implement custom search logic
5. Build advanced search applications

---

*This example demonstrates the power of semantic file search in AI agents, enabling them to find and use relevant information from large document collections.* 