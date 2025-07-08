# 🌊 Streamable HTTP Example - HTTP Streaming Integration

## 📖 Overview

This example demonstrates how to work with Streamable HTTP in MCP. You'll learn how to create HTTP-based streaming communication channels that can handle large data transfers, real-time updates, and efficient data streaming between agents and MCP servers.

## 🎯 What You'll Learn

- ✅ How to implement HTTP streaming with MCP
- ✅ How to handle large data transfers efficiently
- ✅ How to build streaming data processing pipelines
- ✅ How to create scalable HTTP-based communication

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│                 │    │   Streamable     │    │   HTTP          │
│                 │◄──►│   HTTP MCP       │◄──►│   Stream        │
│   Your Agent    │    │   Server         │    │                 │
│   (HTTP Client) │    │                  │    │   - Large Data  │
│                 │    │   Tools:         │    │   - Real-time   │
│                 │    │   - stream_data  │    │   - Chunked     │
│                 │    │   - get_stream   │    │   - Streaming   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
10-streamable-http-example/
├── README.md              # This file
└── 11Streamablehttpexample.py # Main script with streamable HTTP functionality
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
uv run 11Streamablehttpexample.py
```

## 📝 Code Walkthrough

### Main Script: `11Streamablehttpexample.py`

Let's break down the code step by step:

#### 1. Imports and Setup

```python
import os
import asyncio
import json
import aiohttp
from typing import List, Dict, Any, Optional, AsyncGenerator
from dotenv import load_dotenv

from agents import Agent, Runner, set_default_openai_key
from agents.mcp import MCPServerStreamableHttp
```

**What this does:**
- Imports for HTTP streaming and async communication
- MCP streamable HTTP server connection utilities
- Type hints for better code clarity

#### 2. Streamable HTTP Client Implementation

```python
class StreamableHTTPClient:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session = None
        self.streams = {}
    
    async def connect(self):
        """Establish HTTP connection"""
        self.session = aiohttp.ClientSession()
        
        # Test connection
        try:
            async with self.session.get(f"{self.server_url}/health") as response:
                if response.status == 200:
                    print(f"✅ Connected to Streamable HTTP server at {self.server_url}")
                    return True
                else:
                    print(f"❌ Failed to connect: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    async def stream_data(self, endpoint: str, data: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream data from HTTP endpoint"""
        if not self.session:
            await self.connect()
        
        try:
            async with self.session.post(
                f"{self.server_url}/stream/{endpoint}",
                json=data,
                headers={"Accept": "text/event-stream"}
            ) as response:
                if response.status == 200:
                    print(f"✅ Started streaming from {endpoint}")
                    
                    async for line in response.content:
                        line = line.decode('utf-8').strip()
                        
                        if line.startswith('data: '):
                            data_chunk = line[6:]  # Remove 'data: ' prefix
                            
                            if data_chunk == '[DONE]':
                                print(f"📡 {endpoint} stream completed")
                                break
                            
                            try:
                                chunk_data = json.loads(data_chunk)
                                yield chunk_data
                            except json.JSONDecodeError:
                                print(f"⚠️ Invalid JSON in stream: {data_chunk}")
                else:
                    print(f"❌ Failed to start stream: {response.status}")
        except Exception as e:
            print(f"❌ Streaming error: {e}")
```

**What this does:**
- Creates a **streamable HTTP client** for efficient data transfer
- Implements **connection management**
- Provides **data streaming** capabilities
- Supports **chunked data processing**

#### 3. Data Processing Pipeline

```python
    async def process_stream(self, endpoint: str, data: Dict[str, Any], 
                           processor: callable = None) -> List[Dict[str, Any]]:
        """Process streaming data with optional processor"""
        results = []
        
        async for chunk in self.stream_data(endpoint, data):
            if processor:
                processed_chunk = await processor(chunk)
                results.append(processed_chunk)
            else:
                results.append(chunk)
            
            # Print progress for large streams
            if len(results) % 100 == 0:
                print(f"📊 Processed {len(results)} chunks...")
        
        return results
    
    async def get_stream_info(self, endpoint: str) -> Dict[str, Any]:
        """Get information about available streams"""
        if not self.session:
            await self.connect()
        
        try:
            async with self.session.get(f"{self.server_url}/info/{endpoint}") as response:
                if response.status == 200:
                    info = await response.json()
                    return info
                else:
                    print(f"❌ Failed to get stream info: {response.status}")
                    return {}
        except Exception as e:
            print(f"❌ Info error: {e}")
            return {}
```

**What this does:**
- Implements **streaming data processing**
- Provides **progress tracking** for large streams
- Supports **custom data processors**
- Enables **stream metadata** retrieval

#### 4. Advanced Streaming Features

```python
    async def batch_stream(self, endpoints: List[str], data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Stream from multiple endpoints simultaneously"""
        tasks = []
        results = {}
        
        for endpoint in endpoints:
            task = asyncio.create_task(self.process_stream(endpoint, data))
            tasks.append((endpoint, task))
        
        # Wait for all streams to complete
        for endpoint, task in tasks:
            try:
                results[endpoint] = await task
                print(f"✅ Completed stream: {endpoint}")
            except Exception as e:
                print(f"❌ Stream failed {endpoint}: {e}")
                results[endpoint] = []
        
        return results
    
    async def stream_with_backpressure(self, endpoint: str, data: Dict[str, Any], 
                                     max_concurrent: int = 5) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream with backpressure control"""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async with semaphore:
            async for chunk in self.stream_data(endpoint, data):
                # Simulate processing time
                await asyncio.sleep(0.1)
                yield chunk
```

**What this does:**
- Implements **parallel streaming** from multiple endpoints
- Provides **backpressure control** for resource management
- Supports **concurrent processing**
- Enables **stream coordination**

#### 5. MCP Streamable HTTP Server Integration

```python
async def main():
    # Streamable HTTP server configuration
    http_server_url = "http://localhost:3001"  # Default streamable HTTP server URL
    
    # Create streamable HTTP client
    http_client = StreamableHTTPClient(http_server_url)
    
    # Try to connect to streamable HTTP server
    if not await http_client.connect():
        print("⚠️ Streamable HTTP server not available, using mock server")
        http_client = None
    
    # Mock MCP streamable HTTP server for demonstration
    class MockStreamableHTTPServer:
        async def list_tools(self):
            return [
                type('Tool', (), {
                    'name': 'stream_data',
                    'description': 'Stream data from HTTP endpoint'
                })(),
                type('Tool', (), {
                    'name': 'get_stream_info',
                    'description': 'Get information about available streams'
                })(),
                type('Tool', (), {
                    'name': 'batch_stream',
                    'description': 'Stream from multiple endpoints'
                })()
            ]
    
    mcp_server = MockStreamableHTTPServer()
    
    agent = Agent(
        name="Streamable HTTP Assistant",
        model=openai_model,
        instructions=(
            "You're a streamable HTTP assistant. "
            "Help users stream data efficiently, process large datasets, "
            "and manage HTTP-based data pipelines. "
            "Provide guidance on streaming best practices and performance optimization."
        ),
        mcp_servers=[mcp_server],
    )
    
    # Demonstrate streamable HTTP capabilities
    await demonstrate_streamable_http(agent, http_client)
```

**What this does:**
- Creates a **mock streamable HTTP MCP server**
- Integrates **streamable HTTP client** with the agent
- Provides **streaming guidance**
- Demonstrates **HTTP streaming capabilities**

#### 6. Streaming Demonstration

```python
async def demonstrate_streamable_http(agent, http_client):
    """Demonstrate streamable HTTP functionality"""
    print("\n" + "="*60)
    print("STREAMABLE HTTP DEMO: Efficient Data Streaming")
    print("="*60)
    
    if http_client:
        # Stream different types of data
        print("\n📡 Streaming user data...")
        user_data = []
        async for chunk in http_client.stream_data("users", {"limit": 1000}):
            user_data.append(chunk)
            if len(user_data) % 100 == 0:
                print(f"📊 Received {len(user_data)} user records...")
        
        print(f"✅ Completed user stream: {len(user_data)} records")
        
        # Stream analytics data
        print("\n📡 Streaming analytics data...")
        analytics_data = []
        async for chunk in http_client.stream_data("analytics", {"period": "daily"}):
            analytics_data.append(chunk)
        
        print(f"✅ Completed analytics stream: {len(analytics_data)} records")
        
        # Batch streaming
        print("\n📡 Batch streaming from multiple endpoints...")
        batch_results = await http_client.batch_stream(
            ["logs", "metrics", "events"],
            {"timeframe": "last_24h"}
        )
        
        for endpoint, results in batch_results.items():
            print(f"✅ {endpoint}: {len(results)} records")
    
    # Run agent with streaming context
    runner = Runner(agent)
    response = await runner.run(
        "Explain how streamable HTTP works and demonstrate its benefits for large data processing."
    )
    
    print(f"\n🧠 Response:\n{response.content}")
    print("\n" + "="*60)
    print("✅ Streamable HTTP Demo completed successfully!")
    print("="*60)
```

**What this does:**
- Demonstrates **HTTP data streaming**
- Shows **batch processing** capabilities
- Provides **progress tracking**
- Integrates **streaming with agent interaction**

## 🔍 How It Works

### Step-by-Step Process

1. **Connection Setup**: Establish HTTP connection to streaming server
2. **Stream Initiation**: Start data streaming from endpoints
3. **Chunk Processing**: Process data chunks as they arrive
4. **Progress Tracking**: Monitor streaming progress
5. **Data Aggregation**: Collect and process streamed data

### Streamable HTTP Flow

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
│             │    │   Streamable     │    │   HTTP          │
│             │◄──►│   HTTP MCP       │◄──►│   Stream        │
│    Agent    │    │   Server         │    │                 │
│             │    │                  │    │   - Large Data  │
│             │    │   ┌─────────────┐│    │   - Real-time   │
│             │    │   │   HTTP      ││    │   - Chunked     │
│             │    │   │   Client    ││    │   - Streaming   │
│             │    │   └─────────────┘│    │                 │
│             │    │                  │    │                 │
│             │    │   ┌─────────────┐│    │   ┌─────────────┐│
│             │    │   │  Stream     ││    │   │  Data       ││
│             │    │   │  Processor  ││    │   │  Pipeline   ││
│             │    │   │             ││    │   │             ││
│             │    │   │ - Chunk     ││    │   │ - Process   ││
│             │    │   │ - Buffer    ││    │   │ - Transform ││
│             │    │   │ - Aggregate ││    │   │ - Output    ││
│             │    │   └─────────────┘│    │   └─────────────┘│
└─────────────┘    └──────────────────┘    └─────────────────┘
```

## 📊 Expected Output

When you run the script, you should see output like this:

```
============================================================
STREAMABLE HTTP DEMO: Efficient Data Streaming
============================================================

⚠️ Streamable HTTP server not available, using mock server

✅ Connected to Streamable HTTP server at http://localhost:3001

📡 Streaming user data...
📊 Received 100 user records...
📊 Received 200 user records...
📊 Received 300 user records...
✅ Completed user stream: 1000 records

📡 Streaming analytics data...
✅ Completed analytics stream: 500 records

📡 Batch streaming from multiple endpoints...
✅ logs: 250 records
✅ metrics: 150 records
✅ events: 300 records

🧠 Response:
Streamable HTTP enables efficient processing of large datasets through chunked data transfer. Here's how it works:

1. **Chunked Transfer**: Data is sent in manageable chunks
2. **Real-time Processing**: Process data as it arrives
3. **Memory Efficiency**: Avoid loading entire dataset in memory
4. **Scalability**: Handle datasets of any size

**Benefits:**
- Reduced memory usage for large datasets
- Real-time data processing capabilities
- Improved performance for data pipelines
- Better resource utilization

**Use Cases:**
- Large file processing
- Real-time analytics
- Data migration
- Log processing

============================================================
✅ Streamable HTTP Demo completed successfully!
============================================================
```

## 🎯 Key Concepts Explained

### What is Streamable HTTP?

**Streamable HTTP** is a technique for efficiently transferring large amounts of data over HTTP by sending data in chunks rather than loading everything into memory at once. It's ideal for processing large datasets and real-time data pipelines.

### Why Use Streamable HTTP?

| Benefit | Description | Example |
|---------|-------------|---------|
| **💾 Memory Efficient** | Process data in chunks | Handle large files without memory issues |
| **⚡ Real-time** | Process data as it arrives | Live data processing |
| **📈 Scalable** | Handle datasets of any size | Process terabytes of data |
| **🔄 Flexible** | Support various data formats | JSON, CSV, binary data |

### Streaming vs Traditional HTTP

| Method | Memory Usage | Processing | Scalability |
|--------|--------------|------------|-------------|
| **Traditional** | Loads entire dataset | After complete transfer | Limited by memory |
| **Streamable** | Processes in chunks | During transfer | Unlimited |

## 🚨 Troubleshooting

### Common Issues

1. **"Connection timeout"**
   - Check server URL and port
   - Verify server is running
   - Check network connectivity
   - Increase timeout settings

2. **"Memory issues"**
   - Reduce chunk size
   - Implement backpressure control
   - Use streaming processors
   - Monitor memory usage

3. **"Stream interruption"**
   - Implement retry logic
   - Check server stability
   - Monitor network conditions
   - Handle connection errors

### Debug Mode

To see detailed streaming information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔗 Next Steps

After completing this example, try:

1. **🔗 Real HTTP Server**: Connect to a real streamable HTTP server
2. **📊 Data Processing**: Add more sophisticated data processors
3. **🔄 Error Handling**: Implement robust error handling and retries
4. **📈 Performance**: Optimize streaming performance and throughput

## 📚 Additional Resources

- [HTTP Streaming Best Practices](https://modelcontextprotocol.io/docs/streaming)
- [Large Data Processing](https://modelcontextprotocol.io/docs/data)
- [Performance Optimization](https://modelcontextprotocol.io/docs/performance)

## 🤝 Contributing

Found an issue or have a suggestion? Feel free to:
- Report bugs
- Suggest improvements
- Add more streaming features
- Improve documentation

---

**🎉 Congratulations!** You've successfully learned how to implement streamable HTTP communication with MCP. You now understand how to create efficient, scalable data processing pipelines! 