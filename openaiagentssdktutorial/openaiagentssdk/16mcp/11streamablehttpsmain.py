#!/usr/bin/env python3
"""
Main script for Streamable HTTP MCP Example

This script demonstrates how to connect to a streamable HTTP MCP server
and use an agent to interact with the available tools.
"""

import asyncio
import os
import shutil
import subprocess
import time
from typing import Any
from dotenv import load_dotenv

from agents import Agent, Runner, gen_trace_id, trace, set_default_openai_key
from agents.mcp import MCPServer, MCPServerStreamableHttp
from agents.model_settings import ModelSettings

# Load environment variables
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_model = os.environ.get("OPENAI_MODEL", "gpt-4o")
set_default_openai_key(openai_api_key)

async def run(mcp_server: MCPServer):
    """Run the agent with the MCP server"""
    agent = Agent(
        name="Assistant",
        model=openai_model,
        instructions="Use the tools to answer the questions.",
        mcp_servers=[mcp_server],
        model_settings=ModelSettings(tool_choice="required"),
    )

    # Use the `add` tool to add two numbers
    message = "Add these numbers: 7 and 22."
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    # Run the `get_weather` tool
    message = "What's the weather in Tokyo?"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    # Run the `get_secret_word` tool
    message = "What's the secret word?"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

async def main():
    """Main function to run the streamable HTTP example"""
    async with MCPServerStreamableHttp(
        name="Streamable HTTP Python Server",
        params={
            "url": "http://localhost:8000/mcp",
        },
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="Streamable HTTP Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
            await run(server)

if __name__ == "__main__":
    # Let's make sure the user has uv installed
    if not shutil.which("uv"):
        raise RuntimeError(
            "uv is not installed. Please install it: https://docs.astral.sh/uv/getting-started/installation/"
        )

    # We'll run the Streamable HTTP server in a subprocess. Usually this would be a remote server, but for this
    # demo, we'll run it locally at http://localhost:8000/mcp
    process: subprocess.Popen[Any] | None = None
    try:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        server_file = os.path.join(this_dir, "11streamablehttpserver.py")

        print("Starting Streamable HTTP server at http://localhost:8000/mcp ...")

        # Run `uv run server.py` to start the Streamable HTTP server
        process = subprocess.Popen(["uv", "run", server_file])
        # Give it 3 seconds to start
        time.sleep(3)

        print("Streamable HTTP server started. Running example...\n\n")
    except Exception as e:
        print(f"Error starting Streamable HTTP server: {e}")
        exit(1)

    try:
        asyncio.run(main())
    finally:
        if process:
            process.terminate() 