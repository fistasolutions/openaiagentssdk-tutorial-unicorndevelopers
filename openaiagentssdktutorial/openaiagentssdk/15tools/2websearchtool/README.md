# 🌐 Web Search Tool

## 📋 Overview
This example demonstrates how to use the **WebSearchTool** to enable agents to search the internet for current information. The agent can access real-time web data to answer questions about current events, weather, news, and more.

## 🎯 Key Concepts

### **WebSearchTool**
- **Purpose**: Enables agents to search the web for current information
- **Real-time Data**: Accesses live internet data, not pre-stored information
- **Current Events**: Perfect for questions about recent news, weather, stock prices
- **No Configuration**: Simple setup with default search engine integration

### **Web Search Capabilities**
- Search for current information and news
- Get real-time weather data
- Find latest stock prices and market data
- Access current events and breaking news
- Retrieve up-to-date statistics and facts

## 📁 Code Structure

```python
from agents import Agent, WebSearchTool, Runner, set_default_openai_key
from dotenv import load_dotenv
import os
import asyncio

# Environment setup
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
model = os.environ.get("OPENAI_MODEL")

# Agent configuration with WebSearchTool
agent = Agent(
    name="Assistant",
    tools=[
        WebSearchTool(),  # Simple web search capability
    ],
    model=model
)

# Main execution
async def main():
    result = await Runner.run(agent, "What is weather of Faisalabad today")
    print(result.final_output)
```

## 🔧 Configuration Options

### **WebSearchTool Parameters**
- **Default Configuration**: Works out of the box with no parameters
- **Search Engine**: Uses OpenAI's integrated search capabilities
- **Result Limit**: Automatically optimized for best results
- **Real-time**: Always fetches current information

### **Advanced Configuration**
```python
# Example with custom configuration (if supported)
WebSearchTool(
    max_results=10,  # Number of search results
    search_type="web"  # Type of search
)
```

## 🚀 Usage

### **Basic Usage**
```bash
uv run 2websearchtool.py
```

### **Example Queries**
- "What is weather of Faisalabad today"
- "Latest news about artificial intelligence"
- "Current Bitcoin price"
- "Recent sports scores"
- "Today's stock market performance"
- "Breaking news in technology"

## 🛠️ Customization Ideas

### **1. Specialized Search Agents**
```python
# News-focused agent
news_agent = Agent(
    name="News Assistant",
    instructions="You are a news assistant. Always search for the latest information.",
    tools=[WebSearchTool()],
    model=model
)

# Weather agent
weather_agent = Agent(
    name="Weather Assistant",
    instructions="You are a weather assistant. Provide current weather information.",
    tools=[WebSearchTool()],
    model=model
)
```

### **2. Combined with Other Tools**
```python
agent = Agent(
    name="Research Assistant",
    tools=[
        WebSearchTool(),  # Current information
        FileSearchTool(...),  # Local documents
        CodeInterpreterTool(...),  # Data analysis
    ],
    model=model
)
```

### **3. Custom Search Processing**
```python
async def main():
    result = await Runner.run(agent, "Search for latest AI developments")
    
    # Process search results
    print("Search completed!")
    print(f"Final answer: {result.final_output}")
    
    # Access search metadata if available
    print(f"Search performed at: {result.created_at}")
```

## 🔍 How It Works

1. **Query Analysis**: Agent analyzes user question
2. **Search Request**: WebSearchTool sends search query to search engine
3. **Result Retrieval**: Search engine returns relevant web pages
4. **Content Processing**: Tool extracts and processes web content
5. **Response Generation**: Agent synthesizes information into answer

## 📊 Search Capabilities

### **Types of Information**
- **Current Events**: Latest news and breaking stories
- **Weather Data**: Real-time weather conditions
- **Financial Data**: Stock prices, currency rates, market data
- **Sports**: Live scores, game results, player statistics
- **Technology**: Latest tech news, product releases
- **General Knowledge**: Facts, statistics, definitions

### **Search Quality**
- **Relevance**: Results are ranked by relevance to query
- **Freshness**: Prioritizes recent and current information
- **Accuracy**: Uses reliable sources when possible
- **Completeness**: Provides comprehensive answers

## ⚠️ Important Notes

### **Prerequisites**
- Active internet connection required
- OpenAI API key with web search permissions
- Valid model configuration

### **Rate Limits**
- Web search has rate limits to prevent abuse
- Multiple rapid searches may be throttled
- Consider caching for repeated queries

### **Data Quality**
- Web content varies in accuracy and reliability
- Agent may need to verify information from multiple sources
- Some websites may block automated access

## 🐛 Troubleshooting

### **Common Issues**

1. **"No search results found"**
   - Check internet connection
   - Verify search query is clear and specific
   - Try rephrasing the question

2. **"Search failed"**
   - Check API key permissions
   - Verify rate limits haven't been exceeded
   - Ensure model supports web search

3. **"Outdated information"**
   - Web search provides current data
   - If information seems old, try more specific queries
   - Use date-specific search terms

### **Debug Mode**
```python
import logging
logging.getLogger("openai.agents").setLevel(logging.DEBUG)
```

## 🔗 Related Examples

- **FileSearchTool**: Search local documents and files
- **CodeInterpreterTool**: Analyze and process data
- **ComputerTool**: Interact with web browsers directly

## 📚 Best Practices

1. **Be Specific**: Use clear, specific search queries
2. **Verify Information**: Cross-reference important facts
3. **Use Date Context**: Include time references for current events
4. **Handle Errors**: Implement fallbacks for search failures
5. **Respect Rate Limits**: Don't overwhelm the search service

## 🎓 Learning Path

1. Start with basic web searches
2. Learn to combine with other tools
3. Implement specialized search agents
4. Build comprehensive research assistants
5. Create real-time monitoring systems

## 🌟 Advanced Use Cases

### **Real-time Monitoring**
```python
# Monitor specific topics
async def monitor_topic(topic: str):
    agent = Agent(tools=[WebSearchTool()], model=model)
    result = await Runner.run(agent, f"Latest news about {topic}")
    return result.final_output
```

### **Data Verification**
```python
# Verify information from multiple sources
async def verify_information(claim: str):
    agent = Agent(tools=[WebSearchTool()], model=model)
    result = await Runner.run(agent, f"Verify this claim: {claim}")
    return result.final_output
```

---

*This example demonstrates how AI agents can access real-time information from the web, making them capable of providing current and up-to-date answers to user questions.* 