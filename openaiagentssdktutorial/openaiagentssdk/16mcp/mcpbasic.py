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

async def main():
    # Path to the directory with sample files for the MCP filesystem
    current_dir = os.path.dirname(os.path.abspath(__file__))
    samples_dir = os.path.join(current_dir, "sample_files")
    
    # Start the MCP server as subprocess (using npx)
    async with MCPServerStdio(
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
        }
    ) as mcp_server:

        # Create the main agent with MCP server added
        agent = Agent(
            name="File Assistant",
            model=openai_model,
            instructions=(
                "You're a helpful assistant that can read files and answer questions about them. "
                "Use the available tools to read files and provide detailed, helpful responses. "
                "When you read files, remember their content to answer follow-up questions."
            ),
            mcp_servers=[mcp_server],  # Automatically pulls tools from MCP server
        )

        # Single comprehensive demo that reads files and answers questions
        print("=" * 60)
        print("MCP DEMO: Reading Files and Answering Questions")
        print("=" * 60)
        
        comprehensive_query = """
        Please do the following in order:
        
        1. First, read all the files you can access and list them
        2. Then, based on the demo.txt file, explain what MCP is and its key features
        3. Finally, based on the books.txt file, tell me what my #1 favorite book is and why I might like it
        
        Please provide clear, detailed answers for each part.
        """
        
        print(f"Running comprehensive demo...")
        result = await Runner.run(starting_agent=agent, input=comprehensive_query)
        print("\n🧠 Response:")
        print(result.final_output)

        print("\n" + "=" * 60)
        print("✅ MCP Demo completed successfully!")
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
