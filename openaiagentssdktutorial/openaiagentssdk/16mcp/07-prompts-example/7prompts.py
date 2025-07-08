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
# MOCK MCP PROMPTS SYSTEM (for demonstration)
# ============================================================================

class MockPrompt:
    """Mock prompt class for demonstration."""
    def __init__(self, name: str, description: str, template: str):
        self.name = name
        self.description = description
        self.template = template

class MockPromptResult:
    """Mock prompt result class for demonstration."""
    def __init__(self, content: str):
        self.messages = [type('Message', (), {'content': type('Content', (), {'text': content})()})()]

class MockPromptsResult:
    """Mock prompts list result for demonstration."""
    def __init__(self, prompts: list):
        self.prompts = prompts

# ============================================================================
# SAMPLE PROMPTS DATABASE
# ============================================================================

SAMPLE_PROMPTS = {
    "file_analyzer": MockPrompt(
        name="file_analyzer",
        description="Analyze files and provide insights",
        template="""You are a file analysis expert. Your task is to analyze files and provide detailed insights.

Focus areas: {focus_areas}
Analysis depth: {depth}
Output format: {format}

Please analyze the provided files and give comprehensive insights based on the specified focus areas."""
    ),
    
    "code_reviewer": MockPrompt(
        name="code_reviewer", 
        description="Review code for quality and security",
        template="""You are a code review expert specializing in {language} code.

Review focus: {focus}
Code standards: {standards}
Security level: {security_level}

Please review the code thoroughly and provide detailed feedback on code quality, security, and adherence to standards."""
    ),
    
    "document_summarizer": MockPrompt(
        name="document_summarizer",
        description="Summarize documents with specific criteria",
        template="""You are a document summarization expert.

Summary length: {length}
Key points to extract: {key_points}
Target audience: {audience}

Please read the documents and create a comprehensive summary that meets the specified criteria."""
    ),
    
    "data_analyst": MockPrompt(
        name="data_analyst",
        description="Analyze data and provide insights",
        template="""You are a data analysis expert.

Data type: {data_type}
Analysis type: {analysis_type}
Visualization needed: {visualization}

Please analyze the data and provide insights with appropriate visualizations if requested."""
    )
}

# ============================================================================
# MOCK MCP SERVER WITH PROMPTS SUPPORT
# ============================================================================

class MockMCPServerWithPrompts:
    """Mock MCP server that supports prompts for demonstration."""
    
    async def list_prompts(self):
        """List all available prompts."""
        return MockPromptsResult(list(SAMPLE_PROMPTS.values()))
    
    async def get_prompt(self, name: str, arguments: dict = None):
        """Get a specific prompt with optional parameters."""
        if name not in SAMPLE_PROMPTS:
            raise ValueError(f"Prompt '{name}' not found")
        
        prompt = SAMPLE_PROMPTS[name]
        arguments = arguments or {}
        
        # Format the template with provided arguments
        try:
            content = prompt.template.format(**arguments)
        except KeyError as e:
            # Provide default values for missing arguments
            defaults = {
                "focus_areas": "general analysis",
                "depth": "standard",
                "format": "detailed report",
                "language": "general",
                "focus": "code quality",
                "standards": "industry best practices",
                "security_level": "standard",
                "length": "medium",
                "key_points": "main topics",
                "audience": "general",
                "data_type": "text",
                "analysis_type": "descriptive",
                "visualization": "none"
            }
            # Merge provided arguments with defaults
            merged_args = {**defaults, **arguments}
            content = prompt.template.format(**merged_args)
        
        return MockPromptResult(content)

# ============================================================================
# PROMPTS DEMONSTRATION FUNCTIONS
# ============================================================================

async def demonstrate_prompts_listing():
    """Demonstrate listing available prompts."""
    print("📋 Listing Available Prompts")
    print("=" * 50)
    
    mock_server = MockMCPServerWithPrompts()
    
    try:
        prompts_result = await mock_server.list_prompts()
        
        print("Available prompts:")
        for prompt in prompts_result.prompts:
            print(f"  • {prompt.name}: {prompt.description}")
        
        return True
    except Exception as e:
        print(f"Error listing prompts: {e}")
        return False

async def demonstrate_prompt_retrieval():
    """Demonstrate retrieving specific prompts with parameters."""
    print("\n🎯 Retrieving Specific Prompts")
    print("=" * 50)
    
    mock_server = MockMCPServerWithPrompts()
    
    # Test different prompt types with various parameters
    test_cases = [
        {
            "name": "file_analyzer",
            "arguments": {
                "focus_areas": "security, performance, readability",
                "depth": "comprehensive",
                "format": "structured report"
            }
        },
        {
            "name": "code_reviewer",
            "arguments": {
                "language": "Python",
                "focus": "security vulnerabilities",
                "standards": "PEP 8",
                "security_level": "high"
            }
        },
        {
            "name": "document_summarizer",
            "arguments": {
                "length": "concise",
                "key_points": "technical details, conclusions",
                "audience": "developers"
            }
        }
    ]
    
    for case in test_cases:
        try:
            prompt_result = await mock_server.get_prompt(case["name"], case["arguments"])
            instructions = prompt_result.messages[0].content.text
            
            print(f"\n📝 Prompt: {case['name']}")
            print(f"Arguments: {case['arguments']}")
            print(f"Generated Instructions:")
            print("-" * 40)
            print(instructions[:200] + "..." if len(instructions) > 200 else instructions)
            
        except Exception as e:
            print(f"Error retrieving prompt {case['name']}: {e}")

async def demonstrate_agent_with_prompts():
    """Demonstrate using prompts with an actual agent."""
    print("\n🤖 Using Prompts with MCP Agent")
    print("=" * 50)
    
    try:
        # Use the real MCP server for file access
        async with MCPServerStdio(
            params={
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
            }
        ) as mcp_server:

            # Get a prompt for file analysis
            mock_server = MockMCPServerWithPrompts()
            prompt_result = await mock_server.get_prompt(
                "file_analyzer",
                {
                    "focus_areas": "content analysis, structure, key themes",
                    "depth": "detailed",
                    "format": "comprehensive report"
                }
            )
            
            instructions = prompt_result.messages[0].content.text
            
            # Create agent with prompt-generated instructions
            agent = Agent(
                name="File Analysis Expert",
                model=openai_model,
                instructions=instructions,
                mcp_servers=[mcp_server],
            )

            # Test the agent with the prompt-generated instructions
            query = """
            Please analyze the available files and provide insights based on your specialized expertise.
            Focus on content analysis, structure, and key themes as specified in your instructions.
            """

            result = await Runner.run(starting_agent=agent, input=query)

            print("\n🧠 Agent Response with Prompt-Generated Instructions:")
            print(result.final_output)
            
    except Exception as e:
        print(f"\n⚠️  Note: Full prompt integration may not be supported in this SDK version.")
        print(f"Error: {e}")
        print("\n💡 The prompt demonstration above shows the concept and structure.")

# ============================================================================
# MAIN FUNCTION
# ============================================================================

async def main():
    """Main function to demonstrate MCP prompts functionality."""
    
    print("🚀 MCP Prompts Demo")
    print("=" * 60)
    
    # Demonstrate different aspects of prompts
    await demonstrate_prompts_listing()
    await demonstrate_prompt_retrieval()
    await demonstrate_agent_with_prompts()
    
    print("\n" + "=" * 60)
    print("✅ MCP Prompts Demo Complete!")
    print("=" * 60)
    
    print("\n📚 Key Concepts Demonstrated:")
    print("  • Listing available prompts from MCP servers")
    print("  • Retrieving specific prompts with parameters")
    print("  • Using prompt-generated instructions with agents")
    print("  • Dynamic instruction customization")
    print("  • Reusable prompt templates")

if __name__ == "__main__":
    asyncio.run(main()) 