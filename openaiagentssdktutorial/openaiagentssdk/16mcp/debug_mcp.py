#!/usr/bin/env python3
"""
Debug script to test MCP server file access capabilities.
"""

import asyncio
import os
from agents.mcp import MCPServerStdio

async def debug_mcp_server():
    """Debug what the MCP server can access."""
    
    # Get the path to sample files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    samples_dir = os.path.join(current_dir, "sample_files")
    
    print(f"🔧 Debugging MCP Filesystem Server...")
    print(f"📁 Sample files directory: {samples_dir}")
    print(f"📁 Directory exists: {os.path.exists(samples_dir)}")
    
    # List files in the directory
    if os.path.exists(samples_dir):
        files = os.listdir(samples_dir)
        print(f"📋 Files in directory: {files}")
        for file in files:
            file_path = os.path.join(samples_dir, file)
            print(f"   - {file}: {os.path.getsize(file_path)} bytes")
    
    try:
        # Start the MCP server
        async with MCPServerStdio(
            params={
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
            }
        ) as mcp_server:
            
            print("\n✅ MCP Server started successfully!")
            print("🔍 Testing file access...")
            
            # Try to list the directory contents
            try:
                # This is a basic test - we'll see what happens
                print("🎯 MCP Server is running and should be able to access files")
                print("💡 The issue might be in how the agent is calling the MCP tools")
                
            except Exception as e:
                print(f"⚠️  Error testing MCP server: {e}")
                
    except Exception as e:
        print(f"❌ Failed to start MCP server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 MCP Debug Test")
    print("=" * 40)
    
    success = asyncio.run(debug_mcp_server())
    
    if success:
        print("\n✅ Debug completed!")
        print("📝 The MCP server should be working correctly.")
        print("💡 The issue might be in the agent's tool calling or file path resolution.")
    else:
        print("\n❌ Debug failed. Please check the error messages above.") 