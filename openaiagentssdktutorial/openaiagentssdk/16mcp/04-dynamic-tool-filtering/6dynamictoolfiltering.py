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

# ============================================================================
# DYNAMIC TOOL FILTERING EXAMPLES
# ============================================================================

def simple_name_filter(tool_name: str) -> bool:
    """Simple filter that only allows tools with specific names."""
    allowed_tools = ["read_file", "list_files"]
    return tool_name in allowed_tools

def prefix_filter(tool_name: str) -> bool:
    """Filter tools based on name prefix."""
    return tool_name.startswith("read_") or tool_name.startswith("list_")

def security_filter(tool_name: str) -> bool:
    """Security-focused filter that blocks potentially dangerous operations."""
    dangerous_tools = ["delete_file", "write_file", "execute_command"]
    return tool_name not in dangerous_tools

# ============================================================================
# CONTEXT-AWARE FILTERING (Conceptual)
# ============================================================================

class ToolFilterContext:
    """Mock ToolFilterContext for demonstration purposes."""
    def __init__(self, agent_name: str, server_name: str):
        self.agent = type('Agent', (), {'name': agent_name})()
        self.server_name = server_name
        self.run_context = None

def context_aware_filter(context: ToolFilterContext, tool_name: str) -> bool:
    """
    Context-aware filter that considers agent and server information.
    This is a conceptual example since ToolFilterContext might not be available.
    """
    # Example: Only allow read operations for 'readonly_agent'
    if context.agent.name == "readonly_agent":
        return tool_name.startswith("read_")
    
    # Example: Allow all operations for 'admin_agent'
    elif context.agent.name == "admin_agent":
        return True
    
    # Default: Allow safe operations only
    else:
        return security_filter(tool_name)

# ============================================================================
# ASYNC FILTERING (Conceptual)
# ============================================================================

async def async_security_filter(tool_name: str) -> bool:
    """
    Async filter that could perform external checks.
    This is a conceptual example.
    """
    # Simulate async operation (e.g., checking permissions from database)
    await asyncio.sleep(0.1)
    
    # Example: Check if tool is in allowed list from external source
    allowed_tools = ["read_file", "list_files", "get_file_info"]
    return tool_name in allowed_tools

# ============================================================================
# MAIN DEMO FUNCTION
# ============================================================================

async def demo_dynamic_filtering():
    """Demonstrate different dynamic filtering approaches."""
    
    print("🔧 Dynamic Tool Filtering Demo")
    print("=" * 50)
    
    # Test different filter functions
    test_tools = ["read_file", "write_file", "delete_file", "list_files", "get_file_info"]
    
    print("\n📋 Testing Different Filter Functions:")
    print("-" * 40)
    
    for tool in test_tools:
        simple_result = simple_name_filter(tool)
        prefix_result = prefix_filter(tool)
        security_result = security_filter(tool)
        
        print(f"Tool: {tool:15} | Simple: {simple_result} | Prefix: {prefix_result} | Security: {security_result}")
    
    # Test context-aware filtering
    print("\n🎭 Testing Context-Aware Filtering:")
    print("-" * 40)
    
    contexts = [
        ToolFilterContext("readonly_agent", "filesystem_server"),
        ToolFilterContext("admin_agent", "filesystem_server"),
        ToolFilterContext("user_agent", "filesystem_server")
    ]
    
    for context in contexts:
        print(f"\nAgent: {context.agent.name}")
        for tool in test_tools:
            result = context_aware_filter(context, tool)
            print(f"  {tool:15} -> {'✅ Allowed' if result else '❌ Blocked'}")
    
    # Test async filtering
    print("\n⚡ Testing Async Filtering:")
    print("-" * 40)
    
    for tool in test_tools:
        result = await async_security_filter(tool)
        print(f"{tool:15} -> {'✅ Allowed' if result else '❌ Blocked'}")

async def main():
    """Main function to run the MCP server with dynamic filtering demonstration."""
    
    # First, demonstrate the filtering concepts
    await demo_dynamic_filtering()
    
    print("\n" + "=" * 50)
    print("🚀 Running MCP Server with Dynamic Filtering")
    print("=" * 50)
    
    # Note: In the current SDK version, tool_filter might not be supported
    # This is a demonstration of how it would work when supported
    
    try:
        # Attempt to use dynamic filtering (may not work in current SDK)
        async with MCPServerStdio(
            params={
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
            }
            # tool_filter=security_filter  # Uncomment when supported
        ) as mcp_server:

            # Create agent with context-aware name
            agent = Agent(
                name="readonly_agent",  # This would affect context-aware filtering
                model=openai_model,
                instructions=(
                    "You're a file assistant with limited permissions. "
                    "You can read files but cannot modify or delete them. "
                    "When you read files, remember their content to answer follow-up questions."
                ),
                mcp_servers=[mcp_server],
            )

            # Comprehensive query to test file access
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
            
    except Exception as e:
        print(f"\n⚠️  Note: Dynamic tool filtering may not be fully supported in this SDK version.")
        print(f"Error: {e}")
        print("\n💡 The filtering demonstration above shows the concept and structure.")
        print("When the SDK supports it, you can uncomment the tool_filter parameter.")

if __name__ == "__main__":
    asyncio.run(main())
