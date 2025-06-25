# 🌐 Hosted MCP Tool

## 📋 Overview
This example demonstrates how to use the **HostedMCPTool** to enable agents to connect to remote Model Context Protocol (MCP) servers. The agent can access tools and capabilities provided by external MCP servers over the network.

## 🎯 Key Concepts

### **HostedMCPTool**
- **Purpose**: Connects agents to remote MCP servers
- **Network Access**: Communicates with external MCP services
- **Tool Integration**: Provides access to remote tools and capabilities
- **Protocol Compliance**: Uses standard MCP protocol for communication

### **MCP (Model Context Protocol)**
- **Standard Protocol**: Open protocol for AI model tool integration
- **Remote Services**: Connect to external tools and data sources
- **Tool Discovery**: Automatically discover available tools on server
- **Secure Communication**: Encrypted communication with remote servers

### **Hosted MCP Server**
- **Remote Service**: MCP server running on external infrastructure
- **Tool Provider**: Offers various tools and capabilities
- **Network Endpoint**: Accessible via HTTP/HTTPS URL
- **Authentication**: May require API keys or other credentials

## 📁 Code Structure

```python
import asyncio
from agents import Agent, Runner, set_default_openai_key
from agents.tool import HostedMCPTool, Mcp
from dotenv import load_dotenv
import os

# Environment setup
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
model = os.environ.get("OPENAI_MODEL")

# Configure the Hosted MCP tool
mcp_tool = HostedMCPTool(Mcp({
    'type': 'hosted',
    'url': 'https://example.com',  # Replace with your MCP server URL
}))

# Agent configuration
agent = Agent(
    name="Hosted MCP Agent",
    instructions="You can use the remote MCP server's tools to answer questions.",
    tools=[mcp_tool],
    model=model
)

# Main execution
async def main():
    result = await Runner.run(
        agent,
        input="Use the remote MCP tool to perform a sample action."
    )
    print("🌐 Final Output:\n", result.final_output)
```

## 🔧 Configuration Options

### **HostedMCPTool Setup**
```python
# Basic hosted MCP configuration
HostedMCPTool(Mcp({
    'type': 'hosted',
    'url': 'https://your-mcp-server.com'
}))

# With authentication
HostedMCPTool(Mcp({
    'type': 'hosted',
    'url': 'https://your-mcp-server.com',
    'auth': {
        'type': 'api_key',
        'api_key': 'your-api-key'
    }
}))
```

### **MCP Configuration Types**
```python
# Hosted MCP (remote server)
mcp_config = {
    'type': 'hosted',
    'url': 'https://mcp-server.example.com'
}

# Local MCP (if available)
mcp_config = {
    'type': 'local',
    'path': '/path/to/mcp/server'
}
```

## 🚀 Usage

### **Basic Usage**
```bash
uv run 5hostedmcp.py
```

### **Prerequisites**
- Valid MCP server URL
- Network access to the MCP server
- Proper authentication credentials (if required)
- MCP server must be running and accessible

### **Example Tasks**
- "Use the remote MCP tool to perform a sample action"
- "Connect to the database MCP server and query user data"
- "Use the file system MCP to list directory contents"
- "Access the weather MCP service for current conditions"

## 🛠️ Customization Ideas

### **1. Multiple MCP Servers**
```python
# Connect to multiple MCP servers
database_mcp = HostedMCPTool(Mcp({
    'type': 'hosted',
    'url': 'https://database-mcp.example.com'
}))

weather_mcp = HostedMCPTool(Mcp({
    'type': 'hosted',
    'url': 'https://weather-mcp.example.com'
}))

agent = Agent(
    name="Multi-MCP Agent",
    tools=[database_mcp, weather_mcp],
    model=model
)
```

### **2. Authenticated MCP Connections**
```python
# MCP with API key authentication
authenticated_mcp = HostedMCPTool(Mcp({
    'type': 'hosted',
    'url': 'https://secure-mcp.example.com',
    'auth': {
        'type': 'api_key',
        'api_key': os.environ.get('MCP_API_KEY')
    }
}))
```

### **3. Specialized MCP Agents**
```python
# Database-focused agent
db_agent = Agent(
    name="Database Assistant",
    instructions="You are a database assistant. Use MCP tools to query and manage data.",
    tools=[database_mcp],
    model=model
)

# File system agent
fs_agent = Agent(
    name="File Manager",
    instructions="You are a file system manager. Use MCP tools to manage files and directories.",
    tools=[filesystem_mcp],
    model=model
)
```

## 🔍 How It Works

### **MCP Connection Flow**
1. **Tool Initialization**: HostedMCPTool connects to remote MCP server
2. **Handshake**: Establishes connection and authenticates
3. **Tool Discovery**: Discovers available tools on the server
4. **Tool Registration**: Registers remote tools with the agent
5. **Request Processing**: Agent can use remote tools
6. **Response Handling**: Results returned from remote server

### **Communication Protocol**
```python
# MCP protocol communication
# 1. Connect to server
connection = establish_mcp_connection(url, auth)

# 2. Discover tools
tools = await connection.list_tools()

# 3. Execute tool calls
result = await connection.call_tool(tool_name, parameters)

# 4. Process responses
response = process_mcp_response(result)
```

## 📊 MCP Capabilities

### **Common MCP Server Types**
- **Database Servers**: SQL queries, data management
- **File System Servers**: File operations, directory management
- **API Servers**: External service integration
- **Weather Servers**: Weather data and forecasts
- **News Servers**: News aggregation and search
- **Custom Servers**: Domain-specific tools and data

### **Tool Categories**
- **Data Access**: Query databases, read files
- **Data Modification**: Insert, update, delete operations
- **System Operations**: Process management, system info
- **External APIs**: Third-party service integration
- **Custom Functions**: Domain-specific operations

## ⚠️ Important Notes

### **Prerequisites**
- **MCP Server**: Remote MCP server must be running and accessible
- **Network Access**: Agent must be able to reach the MCP server
- **Authentication**: Proper credentials for the MCP server
- **Protocol Support**: MCP server must support the required protocol version

### **Security Considerations**
- **Network Security**: Use HTTPS for secure communication
- **Authentication**: Implement proper authentication mechanisms
- **Access Control**: Limit access to authorized users and operations
- **Data Privacy**: Ensure sensitive data is properly protected

### **Performance**
- **Network Latency**: Remote calls add network delay
- **Connection Overhead**: Each MCP connection has setup time
- **Bandwidth Usage**: Data transfer between agent and server
- **Server Load**: MCP server capacity and response times

## 🐛 Troubleshooting

### **Common Issues**

1. **"Connection failed"**
   - Check MCP server URL is correct
   - Verify server is running and accessible
   - Check network connectivity and firewall settings

2. **"Authentication failed"**
   - Verify API key or credentials are correct
   - Check authentication method matches server requirements
   - Ensure credentials have proper permissions

3. **"Tool not found"**
   - Check MCP server has the required tools
   - Verify tool names and parameters
   - Check server logs for errors

4. **"Timeout error"**
   - Check network latency and server response times
   - Verify server is not overloaded
   - Consider increasing timeout settings

### **Debug Mode**
```python
# Enable MCP debugging
import logging
logging.getLogger("openai.agents.mcp").setLevel(logging.DEBUG)

# Test connection
try:
    mcp_tool = HostedMCPTool(Mcp({'type': 'hosted', 'url': 'https://example.com'}))
    print("MCP connection successful")
except Exception as e:
    print(f"MCP connection failed: {e}")
```

## 🔗 Related Examples

- **LocalShellTool**: Execute local system commands
- **CodeInterpreterTool**: Run code in sandboxed environment
- **CustomFunctionTool**: Create custom Python functions

## 📚 Best Practices

1. **Use HTTPS**: Always use secure connections for MCP servers
2. **Implement Retry Logic**: Handle network failures gracefully
3. **Cache Results**: Cache frequently accessed data when appropriate
4. **Monitor Performance**: Track response times and error rates
5. **Secure Credentials**: Store API keys securely, not in code

## 🎓 Learning Path

1. **Basic MCP Connection**: Learn to connect to simple MCP servers
2. **Authentication**: Implement secure authentication
3. **Tool Discovery**: Explore available tools on MCP servers
4. **Error Handling**: Handle connection and tool execution errors
5. **Advanced Integration**: Build complex multi-MCP applications

## 🌟 Advanced Use Cases

### **Distributed Data Processing**
```python
# Use multiple MCP servers for distributed processing
result = await Runner.run(agent, """
    Query the database MCP for user data,
    process it with the analytics MCP,
    and store results using the storage MCP
""")
```

### **Real-time Monitoring**
```python
# Monitor multiple systems via MCP
result = await Runner.run(agent, """
    Check system status via the monitoring MCP,
    get weather data from the weather MCP,
    and send alerts via the notification MCP
""")
```

### **Data Pipeline**
```python
# Build data processing pipeline
result = await Runner.run(agent, """
    Extract data from the source MCP,
    transform it using the processing MCP,
    and load it into the destination MCP
""")
```

---

*This example demonstrates how AI agents can leverage remote MCP servers to access external tools and data sources, enabling distributed and scalable AI applications.* 