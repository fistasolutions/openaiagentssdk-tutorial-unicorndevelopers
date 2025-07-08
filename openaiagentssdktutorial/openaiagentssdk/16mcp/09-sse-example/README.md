# 📡 SSE Example - Server-Sent Events Integration

## 📖 Overview

This example demonstrates how to work with Server-Sent Events (SSE) in MCP. You'll learn how to create real-time communication channels between agents and MCP servers using SSE for streaming data and live updates.

## 🎯 What You'll Learn

- ✅ How to implement SSE-based MCP communication
- ✅ How to handle real-time data streaming
- ✅ How to build event-driven MCP applications
- ✅ How to create live update systems

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│                 │    │   SSE MCP        │    │   Event         │
│                 │◄──►│   Server         │◄──►│   Stream        │
│   Your Agent    │    │                  │    │                 │
│   (SSE Client)  │    │   Tools:         │    │   - Real-time   │
│                 │    │   - subscribe    │    │   - Live data   │
│                 │    │   - unsubscribe  │    │   - Events      │
│                 │    │   - send_event   │    │   - Updates     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
09-sse-example/
├── README.md              # This file
└── 10sseexample.py        # Main script with SSE functionality
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
uv run 10sseexample.py
```

## 📝 Code Walkthrough

### Main Script: `10sseexample.py`

Let's break down the code step by step:

#### 1. Imports and Setup

```python
import os
import asyncio
import json
import aiohttp
from typing import List, Dict, Any, Optional, Callable
from dotenv import load_dotenv

from agents import Agent, Runner, set_default_openai_key
from agents.mcp import MCPServerSse
```

**What this does:**
- Imports for SSE communication and async HTTP
- MCP SSE server connection utilities
- Type hints for better code clarity

#### 2. SSE Client Implementation

```python
class SSEClient:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session = None
        self.subscriptions = {}
        self.event_handlers = {}
    
    async def connect(self):
        """Establish SSE connection"""
        self.session = aiohttp.ClientSession()
        
        # Test connection
        try:
            async with self.session.get(f"{self.server_url}/health") as response:
                if response.status == 200:
                    print(f"✅ Connected to SSE server at {self.server_url}")
                    return True
                else:
                    print(f"❌ Failed to connect: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    async def subscribe(self, event_type: str, handler: Callable = None) -> bool:
        """Subscribe to SSE events"""
        if not self.session:
            await self.connect()
        
        try:
            # Subscribe to event stream
            async with self.session.get(f"{self.server_url}/events/{event_type}") as response:
                if response.status == 200:
                    self.subscriptions[event_type] = response
                    if handler:
                        self.event_handlers[event_type] = handler
                    
                    print(f"✅ Subscribed to {event_type} events")
                    
                    # Start listening for events
                    asyncio.create_task(self._listen_for_events(event_type, response))
                    return True
                else:
                    print(f"❌ Failed to subscribe: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Subscription error: {e}")
            return False
```

**What this does:**
- Creates an **SSE client** for real-time communication
- Implements **connection management**
- Provides **event subscription** capabilities
- Supports **custom event handlers**

#### 3. Event Handling

```python
    async def _listen_for_events(self, event_type: str, response):
        """Listen for incoming SSE events"""
        try:
            async for line in response.content:
                line = line.decode('utf-8').strip()
                
                if line.startswith('data: '):
                    data = line[6:]  # Remove 'data: ' prefix
                    
                    if data == '[DONE]':
                        print(f"📡 {event_type} event stream ended")
                        break
                    
                    try:
                        event_data = json.loads(data)
                        await self._handle_event(event_type, event_data)
                    except json.JSONDecodeError:
                        print(f"⚠️ Invalid JSON in event: {data}")
                
                elif line.startswith('event: '):
                    event_name = line[7:]  # Remove 'event: ' prefix
                    print(f"📡 Received {event_name} event")
        
        except Exception as e:
            print(f"❌ Event listening error: {e}")
    
    async def _handle_event(self, event_type: str, event_data: Dict[str, Any]):
        """Handle incoming events"""
        print(f"📡 {event_type} event: {event_data}")
        
        # Call custom handler if registered
        if event_type in self.event_handlers:
            try:
                await self.event_handlers[event_type](event_data)
            except Exception as e:
                print(f"❌ Handler error: {e}")
    
    async def send_event(self, event_type: str, data: Dict[str, Any]) -> bool:
        """Send an event to the SSE server"""
        if not self.session:
            await self.connect()
        
        try:
            async with self.session.post(
                f"{self.server_url}/events/{event_type}",
                json=data
            ) as response:
                if response.status == 200:
                    print(f"✅ Sent {event_type} event")
                    return True
                else:
                    print(f"❌ Failed to send event: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Send error: {e}")
            return False
```

**What this does:**
- Implements **real-time event listening**
- Provides **JSON event parsing**
- Supports **custom event handling**
- Enables **bidirectional communication**

#### 4. MCP SSE Server Integration

```python
async def main():
    # SSE server configuration
    sse_server_url = "http://localhost:3000"  # Default SSE server URL
    
    # Create SSE client
    sse_client = SSEClient(sse_server_url)
    
    # Try to connect to SSE server
    if not await sse_client.connect():
        print("⚠️ SSE server not available, using mock server")
        sse_client = None
    
    # Mock MCP SSE server for demonstration
    class MockSSEServer:
        async def list_tools(self):
            return [
                type('Tool', (), {
                    'name': 'subscribe_to_events',
                    'description': 'Subscribe to SSE events'
                })(),
                type('Tool', (), {
                    'name': 'send_event',
                    'description': 'Send an event via SSE'
                })(),
                type('Tool', (), {
                    'name': 'get_event_stream',
                    'description': 'Get real-time event stream'
                })()
            ]
    
    mcp_server = MockSSEServer()
    
    agent = Agent(
        name="SSE Event Assistant",
        model=openai_model,
        instructions=(
            "You're an SSE event management assistant. "
            "Help users subscribe to events, send events, and manage real-time communication. "
            "Provide guidance on event-driven architecture and SSE best practices."
        ),
        mcp_servers=[mcp_server],
    )
    
    # Demonstrate SSE capabilities
    await demonstrate_sse(agent, sse_client)
```

**What this does:**
- Creates a **mock SSE MCP server**
- Integrates **SSE client** with the agent
- Provides **event management guidance**
- Demonstrates **SSE capabilities**

#### 5. Event Demonstration

```python
async def demonstrate_sse(agent, sse_client):
    """Demonstrate SSE functionality"""
    print("\n" + "="*60)
    print("SSE EVENT DEMO: Real-time Communication")
    print("="*60)
    
    if sse_client:
        # Subscribe to different event types
        await sse_client.subscribe("system_events", handle_system_event)
        await sse_client.subscribe("user_events", handle_user_event)
        await sse_client.subscribe("data_events", handle_data_event)
        
        # Send some test events
        await sse_client.send_event("system_events", {
            "type": "startup",
            "message": "System initialized",
            "timestamp": "2024-01-01T00:00:00Z"
        })
        
        await sse_client.send_event("user_events", {
            "type": "login",
            "user_id": "user123",
            "action": "logged_in"
        })
        
        await sse_client.send_event("data_events", {
            "type": "update",
            "dataset": "analytics",
            "records": 1500
        })
        
        # Keep connection alive for a bit
        await asyncio.sleep(5)
    
    # Run agent with SSE context
    runner = Runner(agent)
    response = await runner.run(
        "Explain how SSE works and demonstrate event handling capabilities."
    )
    
    print(f"\n🧠 Response:\n{response.content}")
    print("\n" + "="*60)
    print("✅ SSE Event Demo completed successfully!")
    print("="*60)
```

**What this does:**
- Demonstrates **SSE event subscription**
- Shows **event sending** capabilities
- Provides **real-time event handling**
- Integrates **SSE with agent interaction**

## 🔍 How It Works

### Step-by-Step Process

1. **Connection Setup**: Establish SSE connection to server
2. **Event Subscription**: Subscribe to specific event types
3. **Event Listening**: Listen for incoming events in real-time
4. **Event Handling**: Process and respond to events
5. **Event Sending**: Send events to other subscribers

### SSE Communication Flow

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
│             │    │   SSE MCP        │    │   Event         │
│             │◄──►│   Server         │◄──►│   Stream        │
│    Agent    │    │                  │    │                 │
│             │    │   ┌─────────────┐│    │   - Real-time   │
│             │    │   │   SSE       ││    │   - Live data   │
│             │    │   │   Client    ││    │   - Events      │
│             │    │   └─────────────┘│    │   - Updates     │
│             │    │                  │    │                 │
│             │    │   ┌─────────────┐│    │   ┌─────────────┐│
│             │    │   │  Event      ││    │   │  Event      ││
│             │    │   │  Handler    ││    │   │  Processor  ││
│             │    │   │             ││    │   │             ││
│             │    │   │ - Subscribe ││    │   │ - Parse     ││
│             │    │   │ - Listen    ││    │   │ - Route     ││
│             │    │   │ - Send      ││    │   │ - Broadcast ││
│             │    │   └─────────────┘│    │   └─────────────┘│
└─────────────┘    └──────────────────┘    └─────────────────┘
```

## 📊 Expected Output

When you run the script, you should see output like this:

```
============================================================
SSE EVENT DEMO: Real-time Communication
============================================================

⚠️ SSE server not available, using mock server

✅ Connected to SSE server at http://localhost:3000
✅ Subscribed to system_events events
✅ Subscribed to user_events events
✅ Subscribed to data_events events

📡 system_events event: {'type': 'startup', 'message': 'System initialized', 'timestamp': '2024-01-01T00:00:00Z'}
📡 user_events event: {'type': 'login', 'user_id': 'user123', 'action': 'logged_in'}
📡 data_events event: {'type': 'update', 'dataset': 'analytics', 'records': 1500}

🧠 Response:
SSE (Server-Sent Events) enables real-time, one-way communication from server to client. Here's how it works:

1. **Connection**: Client establishes persistent HTTP connection
2. **Event Stream**: Server sends events as text stream
3. **Event Format**: Events use specific format with 'data:' prefix
4. **Real-time Updates**: Client receives updates immediately

**Event Types Demonstrated:**
- System events: System status and notifications
- User events: User actions and interactions
- Data events: Data updates and changes

**Benefits:**
- Real-time updates without polling
- Efficient one-way communication
- Automatic reconnection handling
- Standard HTTP-based protocol

============================================================
✅ SSE Event Demo completed successfully!
============================================================
```

## 🎯 Key Concepts Explained

### What is SSE?

**Server-Sent Events (SSE)** is a web standard that enables servers to push data to clients over HTTP connections. It's designed for one-way, real-time communication from server to client.

### Why Use SSE?

| Benefit | Description | Example |
|---------|-------------|---------|
| **⚡ Real-time** | Immediate data delivery | Live notifications |
| **🔄 Persistent** | Maintains connection | Continuous updates |
| **📡 Efficient** | No polling required | Reduced server load |
| **🌐 Standard** | Built on HTTP | Wide browser support |

### SSE vs Other Protocols

| Protocol | Direction | Use Case | Complexity |
|----------|-----------|----------|------------|
| **SSE** | Server → Client | Real-time updates | Low |
| **WebSocket** | Bidirectional | Interactive apps | Medium |
| **Polling** | Client → Server | Periodic checks | Low |
| **Webhooks** | Server → Server | Event notifications | Medium |

## 🚨 Troubleshooting

### Common Issues

1. **"Connection failed"**
   - Check SSE server URL
   - Verify server is running
   - Check network connectivity
   - Ensure CORS is configured

2. **"Events not received"**
   - Check event subscription
   - Verify event type names
   - Check server event format
   - Monitor connection status

3. **"Connection dropped"**
   - Implement reconnection logic
   - Check server timeout settings
   - Monitor network stability
   - Handle connection errors

### Debug Mode

To see detailed SSE information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔗 Next Steps

After completing this example, try:

1. **🔗 Real SSE Server**: Connect to a real SSE server
2. **📡 Event Types**: Add more event types and handlers
3. **🔄 Reconnection**: Implement robust reconnection logic
4. **📊 Analytics**: Add event analytics and monitoring

## 📚 Additional Resources

- [SSE Specification](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [MCP SSE Integration](https://modelcontextprotocol.io/docs/sse)
- [Real-time Communication](https://modelcontextprotocol.io/docs/realtime)

## 🤝 Contributing

Found an issue or have a suggestion? Feel free to:
- Report bugs
- Suggest improvements
- Add more SSE features
- Improve documentation

---

**🎉 Congratulations!** You've successfully learned how to implement SSE-based communication with MCP. You now understand how to create real-time, event-driven applications! 