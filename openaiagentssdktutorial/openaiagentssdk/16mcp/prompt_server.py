from mcp.server.fastmcp import FastMCP

# Create server
mcp = FastMCP("Prompt Server")

# Instruction-generating prompts (user-controlled)
@mcp.prompt()
def generate_code_review_instructions(
    focus: str = "general code quality", language: str = "python"
) -> str:
    """Generate agent instructions for code review tasks"""
    print(f"[debug-server] generate_code_review_instructions({focus}, {language})")

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
6. Best Practices Suggestions

Use the available tools to check current time if you need timestamps for your analysis."""

@mcp.prompt()
def generate_documentation_instructions(
    style: str = "comprehensive", audience: str = "developers"
) -> str:
    """Generate agent instructions for documentation tasks"""
    print(f"[debug-server] generate_documentation_instructions({style}, {audience})")

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

@mcp.prompt()
def generate_security_analysis_instructions(
    level: str = "standard", framework: str = "general"
) -> str:
    """Generate agent instructions for security analysis tasks"""
    print(f"[debug-server] generate_security_analysis_instructions({level}, {framework})")

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

if __name__ == "__main__":
    print("🚀 Starting MCP Prompt Server...")
    print("📡 Server will be available at http://localhost:8000/mcp")
    print("🛑 Press Ctrl+C to stop the server")
    mcp.run(transport="streamable-http") 