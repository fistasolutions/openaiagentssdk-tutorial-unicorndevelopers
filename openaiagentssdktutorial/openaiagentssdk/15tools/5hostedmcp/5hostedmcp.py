import asyncio
from agents import Agent, Runner, set_default_openai_key
from agents.tool import HostedMCPTool, Mcp
from dotenv import load_dotenv
import os

load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
model = os.environ.get("OPENAI_MODEL")

# Configure the Hosted MCP tool (replace the URL with your actual MCP server URL)
mcp_tool = HostedMCPTool(Mcp({
    'type': 'hosted',
    'url': 'https://example.com',  # <-- Replace with your MCP server URL
}))

agent = Agent(
    name="Hosted MCP Agent",
    instructions="You can use the remote MCP server's tools to answer questions.",
    tools=[mcp_tool],
    model=model
)

async def main():
    result = await Runner.run(
        agent,
        input="Use the remote MCP tool to perform a sample action."
    )
    print("🌐 Final Output:\n", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
