import asyncio
import shutil
import os
from dotenv import load_dotenv

from agents import Agent, Runner, set_default_openai_key
from agents.mcp import MCPServerStdio

# Load environment variables
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_model = os.environ.get("OPENAI_MODEL")
set_default_openai_key(openai_api_key)

async def run(mcp_server, directory_path: str):
    """Run the Git analysis example with the MCP server."""
    
    agent = Agent(
        name="Git Repository Assistant",
        model=openai_model,
        instructions=f"Answer questions about the git repository at {directory_path}. "
                    "Use the git tools to analyze the repository and provide detailed insights. "
                    "When you analyze the repository, remember the information to answer follow-up questions.",
        mcp_servers=[mcp_server],
    )

    # Demo 1: Find most frequent contributor
    print("=" * 60)
    print("DEMO 1: Most Frequent Contributor")
    print("=" * 60)
    message = "Who's the most frequent contributor?"
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print("🧠 Response:")
    print(result.final_output)

    # Demo 2: Summarize last change
    print("\n" + "=" * 60)
    print("DEMO 2: Last Repository Change")
    print("=" * 60)
    message = "Summarize the last change in the repository."
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print("🧠 Response:")
    print(result.final_output)

    # Demo 3: Repository overview
    print("\n" + "=" * 60)
    print("DEMO 3: Repository Overview")
    print("=" * 60)
    message = "Provide an overview of the repository including recent commits, contributors, and project structure."
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print("🧠 Response:")
    print(result.final_output)

    # Demo 4: Branch analysis
    print("\n" + "=" * 60)
    print("DEMO 4: Branch Analysis")
    print("=" * 60)
    message = "List all branches and show the latest commit on each branch."
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print("🧠 Response:")
    print(result.final_output)

async def main():
    """Main function to run the Git analysis example."""
    
    # Check if uvx is available
    if not shutil.which("uvx"):
        print("⚠️  uvx is not installed. Installing mcp-server-git via npx instead...")
        use_npx = True
    else:
        use_npx = False

    print("🚀 MCP Git Repository Analysis Example")
    print("=" * 60)
    
    # Ask the user for the directory path
    directory_path = input("Please enter the path to the git repository: ").strip()
    
    # Validate the directory path
    if not os.path.exists(directory_path):
        print(f"❌ Error: Directory '{directory_path}' does not exist.")
        return
    
    if not os.path.isdir(directory_path):
        print(f"❌ Error: '{directory_path}' is not a directory.")
        return
    
    # Check if it's a git repository
    git_dir = os.path.join(directory_path, ".git")
    if not os.path.exists(git_dir):
        print(f"❌ Error: '{directory_path}' is not a git repository (no .git directory found).")
        return
    
    print(f"✅ Git repository found at: {directory_path}")
    print("=" * 60)

    try:
        if use_npx:
            # Use npx as fallback
            async with MCPServerStdio(
                params={
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-git", directory_path],
                }
            ) as server:
                print("✅ MCP Git Server started successfully via npx!")
                print("🔍 Server is ready to analyze git repository")
                print()
                
                await run(server, directory_path)
        else:
            # Use uvx as intended
            async with MCPServerStdio(
                params={
                    "command": "uvx", 
                    "args": ["mcp-server-git", directory_path]
                }
            ) as server:
                print("✅ MCP Git Server started successfully via uvx!")
                print("🔍 Server is ready to analyze git repository")
                print()
                
                await run(server, directory_path)

    except Exception as e:
        print(f"\n❌ Error starting MCP Git server: {e}")
        print("\n💡 Troubleshooting tips:")
        print("  1. Make sure the directory is a valid git repository")
        print("  2. Try installing uvx: pip install uvx")
        print("  3. Or use npx: npm install -g npx")
        return

    print("\n" + "=" * 60)
    print("✅ Git Repository Analysis Completed!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 