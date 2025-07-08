#!/usr/bin/env python3
"""
Streamable HTTP MCP Server Example

This example demonstrates how to connect to a streamable HTTP MCP server and use its tools.
Streamable HTTP servers provide HTTP-based streaming capabilities for MCP tools.
"""

import asyncio
import json
import logging
import aiohttp
from typing import Any, Dict, List, Optional
from openai import OpenAI
from agents.mcp import MCPServerStreamableHttp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StreamableHttpMCPServer:
    """Mock Streamable HTTP MCP Server for demonstration"""
    
    def __init__(self, port: int = 8082):
        self.port = port
        self.tools = {
            "process_document": {
                "name": "process_document",
                "description": "Process and analyze a document with streaming results",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "document_url": {
                            "type": "string",
                            "description": "URL of the document to process"
                        },
                        "analysis_type": {
                            "type": "string",
                            "description": "Type of analysis (sentiment, summary, keywords)"
                        }
                    },
                    "required": ["document_url"]
                }
            },
            "stream_analytics": {
                "name": "stream_analytics",
                "description": "Stream real-time analytics data",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "metric": {
                            "type": "string",
                            "description": "Metric to track (users, sales, performance)"
                        },
                        "interval": {
                            "type": "integer",
                            "description": "Update interval in seconds"
                        }
                    },
                    "required": ["metric"]
                }
            },
            "batch_process": {
                "name": "batch_process",
                "description": "Process multiple items with streaming progress",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "items": {
                            "type": "array",
                            "description": "List of items to process"
                        },
                        "operation": {
                            "type": "string",
                            "description": "Operation to perform (validate, transform, analyze)"
                        }
                    },
                    "required": ["items", "operation"]
                }
            }
        }
    
    async def start_server(self):
        """Start the mock streamable HTTP server"""
        logger.info(f"Starting mock Streamable HTTP MCP server on port {self.port}")
        # In a real implementation, this would start an actual HTTP server
        # For demo purposes, we'll just simulate the server being ready
        await asyncio.sleep(1)
        logger.info("Mock Streamable HTTP MCP server is ready")
    
    async def stop_server(self):
        """Stop the mock streamable HTTP server"""
        logger.info("Stopping mock Streamable HTTP MCP server")
        await asyncio.sleep(0.5)

async def demo_streamable_http_mcp_server():
    """Demonstrate Streamable HTTP MCP server functionality"""
    
    # Initialize the mock streamable HTTP server
    http_server = StreamableHttpMCPServer(port=8082)
    await http_server.start_server()
    
    try:
        # Create Streamable HTTP MCP server connection
        # Note: In a real scenario, you would connect to an actual streamable HTTP server
        # For demo purposes, we'll create a mock connection
        logger.info("Creating Streamable HTTP MCP server connection...")
        
        # Simulate connecting to the streamable HTTP server
        mcp_server = MCPServerStreamableHttp(
            params={
                "url": f"http://localhost:{http_server.port}/stream",
                "client_id": "streamable-http-demo-client",
                "client_version": "1.0.0"
            }
        )
        
        # List available tools
        logger.info("Listing available tools...")
        tools = http_server.tools
        for tool_name, tool_info in tools.items():
            logger.info(f"Tool: {tool_name}")
            logger.info(f"  Description: {tool_info['description']}")
            logger.info(f"  Input Schema: {json.dumps(tool_info['inputSchema'], indent=2)}")
            logger.info("")
        
        # Demonstrate tool usage
        logger.info("Demonstrating tool usage...")
        
        # Document processing tool
        doc_result = await simulate_streamable_tool_call(
            "process_document", 
            {"document_url": "https://example.com/doc.pdf", "analysis_type": "sentiment"}
        )
        logger.info(f"Document processing result: {doc_result}")
        
        # Analytics streaming tool
        logger.info("Starting analytics stream...")
        await simulate_streaming_analytics("stream_analytics", {"metric": "users", "interval": 2})
        
        # Batch processing tool
        batch_result = await simulate_batch_processing(
            "batch_process",
            {
                "items": ["item1", "item2", "item3", "item4", "item5"],
                "operation": "validate"
            }
        )
        logger.info(f"Batch processing result: {batch_result}")
        
        logger.info("Streamable HTTP MCP server demo completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in Streamable HTTP MCP server demo: {e}")
    finally:
        await http_server.stop_server()

async def simulate_streamable_tool_call(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate calling a streamable tool on the HTTP server"""
    logger.info(f"Calling streamable tool: {tool_name} with arguments: {arguments}")
    
    # Simulate processing time
    await asyncio.sleep(1)
    
    # Return mock results based on tool
    if tool_name == "process_document":
        return {
            "document_url": arguments["document_url"],
            "analysis_type": arguments.get("analysis_type", "general"),
            "sentiment_score": 0.75,
            "summary": "This document contains positive content with a sentiment score of 0.75.",
            "keywords": ["positive", "content", "analysis", "document"],
            "processing_time": "1.2s"
        }
    elif tool_name == "batch_process":
        items = arguments.get("items", [])
        operation = arguments.get("operation", "process")
        return {
            "operation": operation,
            "total_items": len(items),
            "processed_items": len(items),
            "success_rate": 1.0,
            "results": [f"{operation}_result_{i}" for i in range(len(items))],
            "processing_time": f"{len(items) * 0.3:.1f}s"
        }
    else:
        return {"status": "success", "message": f"Streamable tool {tool_name} executed successfully"}

async def simulate_streaming_analytics(tool_name: str, arguments: Dict[str, Any]):
    """Simulate a streaming analytics tool that sends real-time updates"""
    logger.info(f"Starting analytics stream for tool: {tool_name}")
    
    metric = arguments.get("metric", "users")
    interval = arguments.get("interval", 2)
    
    start_time = asyncio.get_event_loop().time()
    
    # Stream for 10 seconds
    while (asyncio.get_event_loop().time() - start_time) < 10:
        # Simulate real-time analytics data
        if metric == "users":
            data = {
                "timestamp": asyncio.get_event_loop().time(),
                "active_users": 1000 + int(asyncio.get_event_loop().time() % 500),
                "new_users": 50 + int(asyncio.get_event_loop().time() % 20),
                "session_duration": 300 + int(asyncio.get_event_loop().time() % 120)
            }
        elif metric == "sales":
            data = {
                "timestamp": asyncio.get_event_loop().time(),
                "revenue": 50000 + int(asyncio.get_event_loop().time() % 10000),
                "orders": 100 + int(asyncio.get_event_loop().time() % 50),
                "average_order_value": 500 + int(asyncio.get_event_loop().time() % 100)
            }
        else:
            data = {
                "timestamp": asyncio.get_event_loop().time(),
                "performance_score": 85 + int(asyncio.get_event_loop().time() % 15),
                "response_time": 200 + int(asyncio.get_event_loop().time() % 100),
                "error_rate": 0.1 + (asyncio.get_event_loop().time() % 0.2)
            }
        
        logger.info(f"Analytics stream data: {json.dumps(data, indent=2)}")
        await asyncio.sleep(interval)
    
    logger.info("Analytics stream completed")

async def simulate_batch_processing(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate batch processing with streaming progress updates"""
    logger.info(f"Starting batch processing for tool: {tool_name}")
    
    items = arguments.get("items", [])
    operation = arguments.get("operation", "process")
    
    total_items = len(items)
    processed_items = 0
    
    for i, item in enumerate(items):
        # Simulate processing each item
        await asyncio.sleep(0.3)
        processed_items += 1
        
        # Log progress
        progress = (processed_items / total_items) * 100
        logger.info(f"Batch progress: {progress:.1f}% ({processed_items}/{total_items}) - Processing {item}")
        
        # Simulate some items might fail
        if i == 2:  # Simulate one failure
            logger.warning(f"Item {item} failed processing")
    
    return {
        "operation": operation,
        "total_items": total_items,
        "processed_items": processed_items,
        "success_rate": (processed_items / total_items),
        "results": [f"{operation}_result_{i}" for i in range(processed_items)],
        "processing_time": f"{total_items * 0.3:.1f}s"
    }

async def demo_streamable_http_with_agent():
    """Demonstrate using Streamable HTTP MCP server with an OpenAI agent"""
    
    logger.info("Setting up Streamable HTTP MCP server with OpenAI agent...")
    
    # Initialize the mock streamable HTTP server
    http_server = StreamableHttpMCPServer(port=8083)
    await http_server.start_server()
    
    try:
        # Create Streamable HTTP MCP server connection
        mcp_server = MCPServerStreamableHttp(
            params={
                "url": f"http://localhost:{http_server.port}/stream",
                "client_id": "streamable-http-agent-client",
                "client_version": "1.0.0"
            }
        )
        
        # Initialize OpenAI client (you'll need to set OPENAI_API_KEY)
        client = OpenAI()
        
        # Create agent with streamable HTTP tools
        logger.info("Creating agent with Streamable HTTP tools...")
        
        # Simulate agent queries using streamable HTTP tools
        queries = [
            "Analyze the sentiment of this document: https://example.com/report.pdf",
            "Start streaming user analytics data",
            "Process these items: [file1.txt, file2.txt, file3.txt] with validation"
        ]
        
        for query in queries:
            logger.info(f"\nAgent query: {query}")
            
            # Determine which tool to use based on the query
            if "sentiment" in query.lower() or "analyze" in query.lower():
                result = await simulate_streamable_tool_call(
                    "process_document", 
                    {"document_url": "https://example.com/report.pdf", "analysis_type": "sentiment"}
                )
                logger.info(f"Agent response: Document analysis complete. Sentiment score: {result['sentiment_score']}. Summary: {result['summary']}")
            
            elif "analytics" in query.lower() or "streaming" in query.lower():
                logger.info("Agent response: Starting user analytics stream...")
                await simulate_streaming_analytics("stream_analytics", {"metric": "users", "interval": 1})
                logger.info("Agent response: Analytics stream completed.")
            
            elif "process" in query.lower() or "validation" in query.lower():
                result = await simulate_batch_processing(
                    "batch_process",
                    {
                        "items": ["file1.txt", "file2.txt", "file3.txt"],
                        "operation": "validate"
                    }
                )
                logger.info(f"Agent response: Batch processing complete. Success rate: {result['success_rate']:.1%}. Processed {result['processed_items']} items.")
            
            else:
                logger.info("Agent response: I can help you with document analysis, analytics streaming, and batch processing. What would you like to do?")
        
        logger.info("Streamable HTTP agent demo completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in Streamable HTTP agent demo: {e}")
    finally:
        await http_server.stop_server()

async def demo_http_streaming_comparison():
    """Compare different streaming approaches"""
    
    logger.info("Comparing different streaming approaches...")
    
    # Demo 1: Document processing with streaming
    logger.info("\n1. Document Processing with Streaming")
    logger.info("-" * 40)
    await simulate_streamable_tool_call(
        "process_document",
        {"document_url": "https://example.com/large-doc.pdf", "analysis_type": "summary"}
    )
    
    # Demo 2: Real-time analytics
    logger.info("\n2. Real-time Analytics Streaming")
    logger.info("-" * 40)
    await simulate_streaming_analytics("stream_analytics", {"metric": "sales", "interval": 1})
    
    # Demo 3: Batch processing with progress
    logger.info("\n3. Batch Processing with Progress Updates")
    logger.info("-" * 40)
    await simulate_batch_processing(
        "batch_process",
        {
            "items": [f"data_{i}.json" for i in range(1, 11)],
            "operation": "transform"
        }
    )
    
    logger.info("\nStreaming comparison completed!")

async def main():
    """Main function to run all Streamable HTTP demos"""
    logger.info("=== Streamable HTTP MCP Server Examples ===\n")
    
    # Demo 1: Basic Streamable HTTP server functionality
    logger.info("1. Basic Streamable HTTP MCP Server Demo")
    logger.info("=" * 40)
    await demo_streamable_http_mcp_server()
    
    logger.info("\n" + "=" * 50 + "\n")
    
    # Demo 2: Streamable HTTP with agent integration
    logger.info("2. Streamable HTTP MCP Server with Agent Integration")
    logger.info("=" * 40)
    await demo_streamable_http_with_agent()
    
    logger.info("\n" + "=" * 50 + "\n")
    
    # Demo 3: Streaming comparison
    logger.info("3. Streaming Approaches Comparison")
    logger.info("=" * 40)
    await demo_http_streaming_comparison()
    
    logger.info("\n=== All Streamable HTTP examples completed! ===")

if __name__ == "__main__":
    asyncio.run(main()) 