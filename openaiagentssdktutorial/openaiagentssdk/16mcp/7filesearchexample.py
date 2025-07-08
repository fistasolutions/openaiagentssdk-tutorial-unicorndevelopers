import asyncio
import os
import shutil
from dotenv import load_dotenv

from agents import Agent, Runner, set_default_openai_key
from agents.mcp import MCPServerStdio

# Load environment variables
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_model = os.environ.get("OPENAI_MODEL")
set_default_openai_key(openai_api_key)

async def run(mcp_server):
    """Run the file search example with the MCP server."""
    
    agent = Agent(
        name="File Search Assistant",
        model=openai_model,
        instructions="Use the tools to read the filesystem and answer questions based on those files. "
                    "When you read files, remember their content to answer follow-up questions.",
        mcp_servers=[mcp_server],
    )

    # Demo 1: List the files it can read
    print("=" * 60)
    print("DEMO 1: Listing Available Files")
    print("=" * 60)
    message = "Read the files and list them."
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print("🧠 Response:")
    print(result.final_output)

    # Demo 2: Ask about books
    print("\n" + "=" * 60)
    print("DEMO 2: Finding Favorite Book")
    print("=" * 60)
    message = "What is my #1 favorite book?"
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print("🧠 Response:")
    print(result.final_output)

    # Demo 3: Ask a question that reads then reasons
    print("\n" + "=" * 60)
    print("DEMO 3: Book Recommendations")
    print("=" * 60)
    message = "Look at my favorite books. Suggest one new book that I might like based on my reading preferences."
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print("🧠 Response:")
    print(result.final_output)

    # Demo 4: Analyze project notes
    print("\n" + "=" * 60)
    print("DEMO 4: Project Analysis")
    print("=" * 60)
    message = "Read the notes.txt file and tell me what has been completed and what the next steps are for this project."
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print("🧠 Response:")
    print(result.final_output)

async def main():
    """Main function to run the file search example."""
    
    # Check if npx is available
    if not shutil.which("npx"):
        raise RuntimeError("npx is not installed. Please install it with `npm install -g npx`.")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    samples_dir = os.path.join(current_dir, "sample_files")

    print("🚀 MCP File Search Example")
    print("=" * 60)
    print(f"📁 Sample files directory: {samples_dir}")
    print("=" * 60)

    async with MCPServerStdio(
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
        }
    ) as server:
        print("✅ MCP Filesystem Server started successfully!")
        print("🔍 Server is ready to handle file operations")
        print()
        
        await run(server)

    print("\n" + "=" * 60)
    print("✅ File Search Example Completed!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 