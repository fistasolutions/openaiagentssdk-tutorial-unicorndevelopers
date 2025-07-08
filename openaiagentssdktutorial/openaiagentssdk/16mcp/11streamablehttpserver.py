#!/usr/bin/env python3
"""
Streamable HTTP MCP Server

This server provides tools for adding numbers, getting secret words, and weather information.
It runs as a streamable HTTP server that can be connected to by MCP clients.
"""

import random
import requests
from mcp.server import FastMCP

# Create server
mcp = FastMCP("Streamable HTTP Python Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print(f"[debug-server] add({a}, {b})")
    return a + b

@mcp.tool()
def get_secret_word() -> str:
    """Get a random secret word"""
    print("[debug-server] get_secret_word()")
    return random.choice(["apple", "banana", "cherry", "dragon", "elephant", "flamingo"])

@mcp.tool()
def get_current_weather(city: str) -> str:
    """Get current weather for a city"""
    print(f"[debug-server] get_current_weather({city})")
    
    try:
        endpoint = "https://wttr.in"
        response = requests.get(f"{endpoint}/{city}?format=3")
        return response.text
    except Exception as e:
        return f"Error getting weather for {city}: {str(e)}"

if __name__ == "__main__":
    print("Starting Streamable HTTP MCP Server...")
    print("Server will be available at http://localhost:8000/mcp")
    mcp.run(transport="streamable-http") 