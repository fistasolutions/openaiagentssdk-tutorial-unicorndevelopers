from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv
import os
import tempfile

# Load environment variables and set up API key
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
from agents import set_default_openai_key
set_default_openai_key(openai_api_key)

async def main():
    # Create a temporary directory for the filesystem MCP server to access
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a sample file in the temporary directory
        with open(os.path.join(temp_dir, "sample.txt"), "w") as f:
            f.write("This is a sample file created for MCP demonstration.\n")
            f.write("The Model Context Protocol allows LLMs to interact with tools like filesystems.\n")
        
        print(f"Created temporary directory at: {temp_dir}")
        
        # Set up the MCP filesystem server
        async with MCPServerStdio(
            params={
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", temp_dir],
            },
            cache_tools_list=True  # Cache the tools list for better performance
        ) as server:
            # Create an agent with access to the MCP server
            agent = Agent(
                name="FileAssistant",
                instructions="You are a helpful assistant with access to a filesystem. Use the provided tools to read files and help the user understand their contents.",
                model="gpt-4o",
                mcp_servers=[server]
            )
            
            # Run the agent with a prompt that requires using the filesystem tools
            result = await Runner.run(
                agent, 
                "Please read the sample.txt file and summarize its contents."
            )
            
            print("\n--- Agent Response ---")
            print(result.final_output)
            
            # Try another operation
            result = await Runner.run(
                agent,
                "List all files in the current directory and tell me what you can do with them."
            )
            
            print("\n--- Agent Response for Directory Listing ---")
            print(result.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 