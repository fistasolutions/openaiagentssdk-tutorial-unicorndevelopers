import os
import asyncio
from dotenv import load_dotenv

from agents import Agent, Runner, set_default_openai_key
from agents.mcp import MCPServerStdio

# Load OpenAI credentials from .env
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_model = os.environ.get("OPENAI_MODEL")
set_default_openai_key(openai_api_key)

# Directory where your sample files are stored for the MCP filesystem server
current_dir = os.path.dirname(os.path.abspath(__file__))
samples_dir = os.path.join(current_dir, "sample_files")

async def main():
    # Launch the MCP Filesystem server as a subprocess
    async with MCPServerStdio(
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
        }
    ) as mcp_server_1:

        # Optional: Add more servers, for example:
        # mcp_server_2 = MCPServerSse(url="https://some-remote-mcp-server")

        # Attach MCP servers to the agent
        agent = Agent(
            name="MultiTool Assistant",
            model=openai_model,
            instructions=(
                "You are a multi-tool assistant. Use the available tools to analyze file content and provide useful insights. "
                "When you read files, remember their content to answer follow-up questions."
            ),
            mcp_servers=[
                mcp_server_1,  # Add additional servers here if needed
            ],
        )

        # Comprehensive query that first explores files and then reads specific content
        query = """
        Please do the following:
        
        1. First, list all the files you can access
        2. Then, read the content of 'demo.txt' and provide a summary
        3. Finally, read 'books.txt' and tell me about the books listed
        
        Please provide clear, detailed responses for each part.
        """

        # Run the agent with MCP tools enabled
        result = await Runner.run(starting_agent=agent, input=query)

        print("\n🧠 Final Output from Agent:")
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
