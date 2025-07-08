#!/usr/bin/env python3
"""
SSE (Server-Sent Events) MCP Server Example

This example demonstrates how to connect to an SSE MCP server and use its tools.
SSE servers provide real-time streaming capabilities for MCP tools.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from openai import OpenAI
from agents.mcp import MCPServerSse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SSEMCPServer:
    """Mock SSE MCP Server for demonstration"""
    
    def __init__(self, port: int = 8080):
        self.port = port
        self.tools = {
            "get_weather": {
                "name": "get_weather",
                "description": "Get current weather for a location",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City name or coordinates"
                        }
                    },
                    "required": ["location"]
                }
            },
            "get_stock_price": {
                "name": "get_stock_price", 
                "description": "Get current stock price for a symbol",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Stock symbol (e.g., AAPL, GOOGL)"
                        }
                    },
                    "required": ["symbol"]
                }
            },
            "stream_data": {
                "name": "stream_data",
                "description": "Stream real-time data updates",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "data_type": {
                            "type": "string",
                            "description": "Type of data to stream (sensor, market, logs)"
                        },
                        "duration": {
                            "type": "integer",
                            "description": "Duration in seconds to stream"
                        }
                    },
                    "required": ["data_type"]
                }
            }
        }
    
    async def start_server(self):
        """Start the mock SSE server"""
        logger.info(f"Starting mock SSE MCP server on port {self.port}")
        # In a real implementation, this would start an actual HTTP server
        # For demo purposes, we'll just simulate the server being ready
        await asyncio.sleep(1)
        logger.info("Mock SSE MCP server is ready")
    
    async def stop_server(self):
        """Stop the mock SSE server"""
        logger.info("Stopping mock SSE MCP server")
        await asyncio.sleep(0.5)

async def demo_sse_mcp_server():
    """Demonstrate SSE MCP server functionality"""
    
    # Initialize the mock SSE server
    sse_server = SSEMCPServer(port=8080)
    await sse_server.start_server()
    
    try:
        # Create SSE MCP server connection
        # Note: In a real scenario, you would connect to an actual SSE server
        # For demo purposes, we'll create a mock connection
        logger.info("Creating SSE MCP server connection...")
        
        # Simulate connecting to the SSE server
        mcp_server = MCPServerSse(
            params={
                "url": f"http://localhost:{sse_server.port}/sse",
                "client_id": "sse-demo-client",
                "client_version": "1.0.0"
            }
        )
        
        # List available tools
        logger.info("Listing available tools...")
        tools = sse_server.tools
        for tool_name, tool_info in tools.items():
            logger.info(f"Tool: {tool_name}")
            logger.info(f"  Description: {tool_info['description']}")
            logger.info(f"  Input Schema: {json.dumps(tool_info['inputSchema'], indent=2)}")
            logger.info("")
        
        # Demonstrate tool usage
        logger.info("Demonstrating tool usage...")
        
        # Weather tool
        weather_result = await simulate_tool_call("get_weather", {"location": "New York"})
        logger.info(f"Weather result: {weather_result}")
        
        # Stock price tool
        stock_result = await simulate_tool_call("get_stock_price", {"symbol": "AAPL"})
        logger.info(f"Stock result: {stock_result}")
        
        # Streaming data tool
        logger.info("Starting data stream...")
        await simulate_streaming_tool("stream_data", {"data_type": "sensor", "duration": 5})
        
        logger.info("SSE MCP server demo completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in SSE MCP server demo: {e}")
    finally:
        await sse_server.stop_server()

async def simulate_tool_call(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate calling a tool on the SSE server"""
    logger.info(f"Calling tool: {tool_name} with arguments: {arguments}")
    
    # Simulate processing time
    await asyncio.sleep(0.5)
    
    # Return mock results based on tool
    if tool_name == "get_weather":
        return {
            "location": arguments["location"],
            "temperature": "72°F",
            "condition": "Partly Cloudy",
            "humidity": "65%",
            "wind_speed": "8 mph"
        }
    elif tool_name == "get_stock_price":
        return {
            "symbol": arguments["symbol"],
            "price": "$150.25",
            "change": "+2.15",
            "change_percent": "+1.45%",
            "volume": "45.2M"
        }
    else:
        return {"status": "success", "message": f"Tool {tool_name} executed successfully"}

async def simulate_streaming_tool(tool_name: str, arguments: Dict[str, Any]):
    """Simulate a streaming tool that sends real-time updates"""
    logger.info(f"Starting stream for tool: {tool_name}")
    
    data_type = arguments.get("data_type", "sensor")
    duration = arguments.get("duration", 5)
    
    start_time = asyncio.get_event_loop().time()
    
    while (asyncio.get_event_loop().time() - start_time) < duration:
        # Simulate real-time data
        if data_type == "sensor":
            data = {
                "timestamp": asyncio.get_event_loop().time(),
                "temperature": 20 + (asyncio.get_event_loop().time() % 10),
                "humidity": 50 + (asyncio.get_event_loop().time() % 20),
                "pressure": 1013 + (asyncio.get_event_loop().time() % 5)
            }
        elif data_type == "market":
            data = {
                "timestamp": asyncio.get_event_loop().time(),
                "price": 100 + (asyncio.get_event_loop().time() % 10),
                "volume": 1000 + int(asyncio.get_event_loop().time() % 500),
                "bid": 99.5 + (asyncio.get_event_loop().time() % 1),
                "ask": 100.5 + (asyncio.get_event_loop().time() % 1)
            }
        else:
            data = {
                "timestamp": asyncio.get_event_loop().time(),
                "message": f"Log entry {int(asyncio.get_event_loop().time())}",
                "level": "INFO"
            }
        
        logger.info(f"Stream data: {json.dumps(data, indent=2)}")
        await asyncio.sleep(1)
    
    logger.info("Stream completed")

async def demo_sse_with_agent():
    """Demonstrate using SSE MCP server with an OpenAI agent"""
    
    logger.info("Setting up SSE MCP server with OpenAI agent...")
    
    # Initialize the mock SSE server
    sse_server = SSEMCPServer(port=8081)
    await sse_server.start_server()
    
    try:
        # Create SSE MCP server connection
        mcp_server = MCPServerSse(
            params={
                "url": f"http://localhost:{sse_server.port}/sse",
                "client_id": "sse-agent-client",
                "client_version": "1.0.0"
            }
        )
        
        # Initialize OpenAI client (you'll need to set OPENAI_API_KEY)
        client = OpenAI()
        
        # Create agent with SSE tools
        logger.info("Creating agent with SSE tools...")
        
        # Simulate agent queries using SSE tools
        queries = [
            "What's the weather like in San Francisco?",
            "Get me the current stock price for Tesla",
            "Start streaming sensor data for 3 seconds"
        ]
        
        for query in queries:
            logger.info(f"\nAgent query: {query}")
            
            # Determine which tool to use based on the query
            if "weather" in query.lower():
                location = "San Francisco" if "san francisco" in query.lower() else "New York"
                result = await simulate_tool_call("get_weather", {"location": location})
                logger.info(f"Agent response: The weather in {location} is {result['temperature']} with {result['condition']} conditions.")
            
            elif "stock" in query.lower() or "tesla" in query.lower():
                symbol = "TSLA" if "tesla" in query.lower() else "AAPL"
                result = await simulate_tool_call("get_stock_price", {"symbol": symbol})
                logger.info(f"Agent response: {symbol} is currently trading at {result['price']} ({result['change']} {result['change_percent']})")
            
            elif "stream" in query.lower() or "sensor" in query.lower():
                logger.info("Agent response: Starting sensor data stream...")
                await simulate_streaming_tool("stream_data", {"data_type": "sensor", "duration": 3})
                logger.info("Agent response: Sensor data stream completed.")
            
            else:
                logger.info("Agent response: I can help you with weather, stock prices, and data streaming. What would you like to know?")
        
        logger.info("SSE agent demo completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in SSE agent demo: {e}")
    finally:
        await sse_server.stop_server()

async def main():
    """Main function to run all SSE demos"""
    logger.info("=== SSE MCP Server Examples ===\n")
    
    # Demo 1: Basic SSE server functionality
    logger.info("1. Basic SSE MCP Server Demo")
    logger.info("=" * 40)
    await demo_sse_mcp_server()
    
    logger.info("\n" + "=" * 50 + "\n")
    
    # Demo 2: SSE with agent integration
    logger.info("2. SSE MCP Server with Agent Integration")
    logger.info("=" * 40)
    await demo_sse_with_agent()
    
    logger.info("\n=== All SSE examples completed! ===")

if __name__ == "__main__":
    asyncio.run(main()) 