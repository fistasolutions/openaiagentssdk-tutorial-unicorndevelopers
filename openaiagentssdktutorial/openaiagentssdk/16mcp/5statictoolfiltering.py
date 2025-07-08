import os
import asyncio
from dotenv import load_dotenv

from agents import Agent, Runner, set_default_openai_key
from agents.mcp import MCPServerStdio

# Load environment variables
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_model = os.environ.get("OPENAI_MODEL")
set_default_openai_key(openai_api_key)

# Directory containing sample files
current_dir = os.path.dirname(os.path.abspath(__file__))
samples_dir = os.path.join(current_dir, "sample_files")

async def main():
    # Use MCPServerStdio as an async context manager
    async with MCPServerStdio(
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
        }
    ) as mcp_server:

        # Agent setup
        agent = Agent(
            name="Filtered Tool Assistant",
            model=openai_model,
            instructions=(
                "You're a file assistant. You can read or write files. "
                "When you read files, remember their content to answer follow-up questions."
            ),
            mcp_servers=[mcp_server],
        )

        # Comprehensive query that first explores files and then reads specific content
        query = """
        Please do the following:
        
        1. First, list all the files you can access
        2. Then, read the content of 'demo.txt' and show me its content
        3. Finally, read 'books.txt' and tell me about the books listed
        
        Please provide clear, detailed responses for each part.
        """

        result = await Runner.run(starting_agent=agent, input=query)

        print("\n🧠 Final Output from Agent:")
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
