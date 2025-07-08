import asyncio
import os
import shutil
import subprocess
import time
from typing import Any
from dotenv import load_dotenv

from agents import Agent, Runner, set_default_openai_key
from agents.mcp import MCPServerSse

# Load environment variables
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_model = os.environ.get("OPENAI_MODEL")
set_default_openai_key(openai_api_key)

# ============================================================================
# MOCK PROMPT SYSTEM (for demonstration since HTTP server might not work)
# ============================================================================

class MockPromptServer:
    """Mock prompt server for demonstration purposes."""
    
    def __init__(self):
        self.prompts = {
            "generate_code_review_instructions": self._code_review_prompt,
            "generate_documentation_instructions": self._documentation_prompt,
            "generate_security_analysis_instructions": self._security_prompt,
        }
    
    def _code_review_prompt(self, focus: str = "general code quality", language: str = "python") -> str:
        return f"""You are a senior {language} code review specialist. Your role is to provide comprehensive code analysis with focus on {focus}.

INSTRUCTIONS:
- Analyze code for quality, security, performance, and best practices
- Provide specific, actionable feedback with examples
- Identify potential bugs, vulnerabilities, and optimization opportunities
- Suggest improvements with code examples when applicable
- Be constructive and educational in your feedback
- Focus particularly on {focus} aspects

RESPONSE FORMAT:
1. Overall Assessment
2. Specific Issues Found
3. Security Considerations
4. Performance Notes
5. Recommended Improvements
6. Best Practices Suggestions"""

    def _documentation_prompt(self, style: str = "comprehensive", audience: str = "developers") -> str:
        return f"""You are a technical documentation specialist. Your role is to create {style} documentation for {audience}.

INSTRUCTIONS:
- Analyze code and create clear, structured documentation
- Focus on {style} coverage of the codebase
- Tailor the documentation for {audience} audience
- Include code examples, explanations, and best practices
- Ensure documentation is maintainable and up-to-date
- Provide actionable insights for improvement

RESPONSE FORMAT:
1. Overview and Purpose
2. Code Structure Analysis
3. Function/Class Documentation
4. Usage Examples
5. Best Practices
6. Recommendations for Improvement"""

    def _security_prompt(self, level: str = "standard", framework: str = "general") -> str:
        return f"""You are a cybersecurity expert specializing in {framework} security analysis. Your role is to perform {level} security assessment.

INSTRUCTIONS:
- Conduct thorough security analysis of the provided code
- Identify potential vulnerabilities and security risks
- Assess compliance with security best practices
- Provide specific remediation recommendations
- Consider {level} security requirements
- Focus on {framework} specific security concerns

RESPONSE FORMAT:
1. Security Assessment Summary
2. Identified Vulnerabilities
3. Risk Analysis
4. Compliance Check
5. Remediation Recommendations
6. Security Best Practices"""

    def get_prompt(self, prompt_name: str, **kwargs) -> str:
        """Get a prompt with the given name and parameters."""
        if prompt_name in self.prompts:
            return self.prompts[prompt_name](**kwargs)
        else:
            return f"You are a helpful assistant. Error: Prompt '{prompt_name}' not found."

    def list_prompts(self):
        """List all available prompts."""
        return {
            "generate_code_review_instructions": "Generate agent instructions for code review tasks",
            "generate_documentation_instructions": "Generate agent instructions for documentation tasks", 
            "generate_security_analysis_instructions": "Generate agent instructions for security analysis tasks"
        }

async def get_instructions_from_prompt(prompt_server: MockPromptServer, prompt_name: str, **kwargs) -> str:
    """Get agent instructions by calling prompt server (user-controlled)"""
    print(f"Getting instructions from prompt: {prompt_name}")

    try:
        instructions = prompt_server.get_prompt(prompt_name, **kwargs)
        print("✅ Generated instructions successfully")
        return instructions
    except Exception as e:
        print(f"❌ Failed to get instructions: {e}")
        return f"You are a helpful assistant. Error: {e}"

async def demo_code_review(prompt_server: MockPromptServer):
    """Demo: Code review with user-selected prompt"""
    print("=" * 60)
    print("DEMO 1: Code Review with Dynamic Instructions")
    print("=" * 60)

    # User explicitly selects prompt and parameters
    instructions = await get_instructions_from_prompt(
        prompt_server,
        "generate_code_review_instructions",
        focus="security vulnerabilities",
        language="python",
    )

    agent = Agent(
        name="Code Reviewer Agent",
        model=openai_model,
        instructions=instructions,  # Instructions from prompt server
    )

    message = """Please review this code:

def process_user_input(user_input):
    command = f"echo {user_input}"
    os.system(command)
    return "Command executed"

"""

    print(f"Running: {message[:60]}...")
    result = await Runner.run(starting_agent=agent, input=message)
    print("🧠 Response:")
    print(result.final_output)

async def demo_document_analysis(prompt_server: MockPromptServer):
    """Demo: Document analysis with different prompt parameters"""
    print("\n" + "=" * 60)
    print("DEMO 2: Document Analysis with Custom Instructions")
    print("=" * 60)

    # Get instructions for document analysis
    instructions = await get_instructions_from_prompt(
        prompt_server,
        "generate_documentation_instructions",
        style="comprehensive",
        audience="developers",
    )

    agent = Agent(
        name="Document Analysis Agent",
        model=openai_model,
        instructions=instructions,
    )

    message = """Please analyze this code for documentation:

def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total

"""

    print(f"Running: {message[:60]}...")
    result = await Runner.run(starting_agent=agent, input=message)
    print("🧠 Response:")
    print(result.final_output)

async def demo_security_analysis(prompt_server: MockPromptServer):
    """Demo: Security analysis with security-focused prompt"""
    print("\n" + "=" * 60)
    print("DEMO 3: Security Analysis with Security Instructions")
    print("=" * 60)

    # Get instructions for security analysis
    instructions = await get_instructions_from_prompt(
        prompt_server,
        "generate_security_analysis_instructions",
        level="high",
        framework="python",
    )

    agent = Agent(
        name="Security Analysis Agent",
        model=openai_model,
        instructions=instructions,
    )

    message = """Please perform a security analysis of this code:

import subprocess

def execute_command(user_input):
    result = subprocess.run(user_input, shell=True, capture_output=True)
    return result.stdout.decode()

"""

    print(f"Running: {message[:60]}...")
    result = await Runner.run(starting_agent=agent, input=message)
    print("🧠 Response:")
    print(result.final_output)

async def show_available_prompts(prompt_server: MockPromptServer):
    """Show available prompts for user selection"""
    print("=" * 60)
    print("AVAILABLE PROMPTS")
    print("=" * 60)

    try:
        prompts = prompt_server.list_prompts()
        print("User can select from these prompts:")
        for i, (name, description) in enumerate(prompts.items(), 1):
            print(f"  {i}. {name} - {description}")
        print()
        return True
    except Exception as e:
        print(f"❌ Error listing prompts: {e}")
        return False

async def main():
    """Main function to run the prompt server example."""
    
    print("🚀 MCP Prompt Server Example")
    print("=" * 60)
    print("📝 Note: Using mock prompt server for demonstration")
    print("💡 In a real scenario, this would connect to an HTTP MCP server")
    print("=" * 60)

    # Create mock prompt server
    prompt_server = MockPromptServer()

    try:
        # Show available prompts
        await show_available_prompts(prompt_server)
        
        # Run demos
        await demo_code_review(prompt_server)
        await demo_document_analysis(prompt_server)
        await demo_security_analysis(prompt_server)

    except Exception as e:
        print(f"\n❌ Error running prompt server example: {e}")
        print("\n💡 Troubleshooting tips:")
        print("  1. Make sure all dependencies are installed")
        print("  2. Check if the OpenAI API key is set correctly")
        print("  3. Verify that the model is available")
        return

    print("\n" + "=" * 60)
    print("✅ Prompt Server Example Completed!")
    print("=" * 60)
    print("\n📚 Key Concepts Demonstrated:")
    print("  • Dynamic instruction generation from prompts")
    print("  • Parameterized prompt templates")
    print("  • Different agent roles based on prompts")
    print("  • Reusable prompt system architecture")

if __name__ == "__main__":
    asyncio.run(main()) 