# 🛡️ Output Guardrails Example

## What This Code Does (Big Picture)
Imagine having an AI tutor that can catch itself before giving inappropriate answers! This code shows how to create intelligent output guardrails that analyze the AI's responses before they're sent to the user, blocking responses that contain mathematical solutions, code snippets, or personal information.

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
from pydantic import BaseModel, Field
from typing import List, Optional, Union
import asyncio
import re
from dotenv import load_dotenv
import os
from agents import set_default_openai_key

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    output_guardrail,
    set_default_openai_key
)
```
The AI assistants need a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Creating Output Models for Guardrail Checks 📋
```python
# Define output models for the main agent and guardrail checks
class MessageOutput(BaseModel):
    response: str = Field(..., description="The agent's response to the user")

class MathOutput(BaseModel):
    is_math: bool = Field(..., description="Whether the output contains mathematical solutions")
    reasoning: str = Field(..., description="Explanation of why this does or doesn't contain math")

class CodeOutput(BaseModel):
    contains_code: bool = Field(..., description="Whether the output contains code snippets")
    reasoning: str = Field(..., description="Explanation of why this does or doesn't contain code")

class PersonalInfoOutput(BaseModel):
    contains_personal_info: bool = Field(..., description="Whether the output contains personal information")
    reasoning: str = Field(..., description="Explanation of why this does or doesn't contain personal information")
    info_type: Optional[str] = Field(None, description="Type of personal information detected, if any")
```
These create structured output models for different types of guardrail checks:
- `MessageOutput`: The standard output format for the main agent
- `MathOutput`: For detecting mathematical solutions in responses
- `CodeOutput`: For detecting code snippets in responses
- `PersonalInfoOutput`: For detecting personal information in responses

Each model includes a boolean flag indicating whether the response is inappropriate, reasoning for the decision, and in some cases, additional details.

## Step 3: Creating Specialized Guardrail Agents 🕵️‍♂️
```python
# Create specialized guardrail agents
math_guardrail_agent = Agent(
    name="Math Content Detector",
    instructions="""
    You are a specialized agent that detects if responses contain mathematical solutions.
    
    Analyze the output to determine if it includes direct solutions to math problems.
    
    Consider these as math solutions:
    - Step-by-step solutions to equations
    - Direct answers to math problems (e.g., "x = 4")
    - Calculations with specific numerical answers
    - Worked examples showing how to solve a specific problem
    
    Don't consider these as math solutions:
    - General explanations of mathematical concepts
    - Descriptions of problem-solving approaches without specific solutions
    - Mathematical formulas without applying them to specific problems
    - Historical or contextual information about mathematics
    
    Provide clear reasoning for your decision.
    """,
    output_type=MathOutput,
)

code_guardrail_agent = Agent(
    name="Code Content Detector",
    instructions="""
    You are a specialized agent that detects if responses contain code snippets.
    
    Analyze the output to determine if it includes actual code that could be copied and used.
    
    Consider these as code:
    - Complete functions or methods with implementation details
    - Executable code blocks in any programming language
    - Code snippets that solve specific problems
    - Scripts or commands that can be run directly
    
    Don't consider these as code:
    - Pseudocode that describes an algorithm conceptually
    - Brief syntax examples (e.g., explaining what a for loop looks like)
    - References to coding concepts without implementation
    - File or directory names
    
    Provide clear reasoning for your decision.
    """,
    output_type=CodeOutput,
)

personal_info_guardrail_agent = Agent(
    name="Personal Information Detector",
    instructions="""
    You are a specialized agent that detects if responses contain personal information.
    
    Analyze the output to determine if it includes sensitive personal information that shouldn't be shared.
    
    Consider these as personal information:
    - Names with associated personal details
    - Contact information (phone numbers, email addresses, physical addresses)
    - Financial information (account numbers, credit card details)
    - Government IDs (SSN, passport numbers, driver's license numbers)
    - Health information
    
    Don't consider these as personal information:
    - Generic examples with placeholder data
    - Public information about well-known figures
    - General demographic information without specific identifiers
    - Fictional character information
    
    Provide clear reasoning for your decision and specify the type of personal information if detected.
    """,
    output_type=PersonalInfoOutput,
)
```
This creates three specialized agents:
- A math content detector that identifies mathematical solutions in responses
- A code content detector that identifies code snippets in responses
- A personal information detector that identifies sensitive information in responses

Each agent is configured with specific instructions about what to consider inappropriate and what's acceptable, along with the appropriate output type.

## Step 4: Creating Output Guardrail Functions 🛡️
```python
# Define guardrail functions
@output_guardrail
async def math_output_guardrail(
    ctx: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    """Detect and block responses containing mathematical solutions."""
    result = await Runner.run(math_guardrail_agent, output.response, context=ctx.context)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math,
        message="I can help you understand mathematical concepts, but I'm not able to provide direct solutions to math problems. I'd be happy to explain the approach or guide you through the process instead."
    )

@output_guardrail
async def code_output_guardrail(
    ctx: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    """Detect and block responses containing code snippets."""
    result = await Runner.run(code_guardrail_agent, output.response, context=ctx.context)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.contains_code,
        message="I can explain programming concepts and approaches, but I'm not able to provide complete code solutions. I'd be happy to guide you through the development process or explain specific concepts instead."
    )

@output_guardrail
async def personal_info_output_guardrail(
    ctx: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    """Detect and block responses containing personal information."""
    result = await Runner.run(personal_info_guardrail_agent, output.response, context=ctx.context)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.contains_personal_info,
        message="I've detected that my response might contain personal information, which I should avoid sharing. Let me provide a more general response instead."
    )
```
These functions create the actual output guardrails:
- Each is decorated with `@output_guardrail` to mark it as an output guardrail function
- Each runs its specialized detector agent on the response
- Each returns a `GuardrailFunctionOutput` with:
  - The detailed output from the detector
  - A boolean indicating whether the guardrail should be triggered
  - A helpful message explaining why the response was blocked and offering alternatives

The key difference from input guardrails is that these check the AI's own responses rather than user inputs.

## Step 5: Creating a Tutor Agent with Output Guardrails 🤖
```python
# Create a main agent with output guardrails
tutor_agent = Agent(
    name="Educational Tutor",
    instructions="""
    You are an educational tutor who helps students learn and understand various subjects.
    
    Your role is to:
    1. Explain concepts clearly and thoroughly
    2. Guide students through problem-solving processes
    3. Provide examples to illustrate ideas
    4. Answer questions about academic subjects
    5. Suggest resources for further learning
    
    Always focus on helping students understand the material rather than simply giving them answers.
    Encourage critical thinking and independent problem-solving.
    """,
    output_guardrails=[
        math_output_guardrail,
        code_output_guardrail,
        personal_info_output_guardrail,
    ],
    output_type=MessageOutput,
)
```
This creates an educational tutor agent that:
- Helps students learn and understand various subjects
- Is configured with all three output guardrails to prevent inappropriate responses
- Focuses on explaining concepts rather than giving direct answers
- Uses the `MessageOutput` type for its responses

## Step 6: Creating a Function to Test Output Guardrails 🧪
```python
# Function to test output guardrails with various inputs
async def test_output_guardrails():
    print("=== Testing Output Guardrails ===\n")
    
    test_cases = [
        {
            "name": "Math Solution",
            "input": "How do I solve 2x + 3 = 11?",
            "expected_trigger": True,
            "guardrail_type": "Math Output"
        },
        {
            "name": "Math Concept",
            "input": "What is the quadratic formula used for?",
            "expected_trigger": False,
            "guardrail_type": "Math Output"
        },
        {
            "name": "Code Solution",
            "input": "Write a Python function to find the factorial of a number.",
            "expected_trigger": True,
            "guardrail_type": "Code Output"
        },
        {
            "name": "Code Concept",
            "input": "What is object-oriented programming?",
            "expected_trigger": False,
            "guardrail_type": "Code Output"
        },
        {
            "name": "Personal Information",
            "input": "Can you tell me about John Smith who lives at 123 Main St and has SSN 123-45-6789?",
            "expected_trigger": True,
            "guardrail_type": "Personal Info Output"
        },
        {
            "name": "General Question",
            "input": "What are the main themes in Shakespeare's Hamlet?",
            "expected_trigger": False,
            "guardrail_type": "None"
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"Test {i+1}: {test_case['name']}")
        print(f"Input: \"{test_case['input']}\"")
        print(f"Expected to trigger {test_case['guardrail_type']} guardrail: {test_case['expected_trigger']}")
        
        try:
            result = await Runner.run(tutor_agent, test_case['input'])
            print("Result: Guardrail not triggered")
            print(f"Response: {result.final_output.response[:100]}...")
            
            if test_case['expected_trigger']:
                print("WARNING: Expected guardrail to trigger, but it didn't!")
            
        except OutputGuardrailTripwireTriggered as e:
            print(f"Result: Guardrail triggered")
            print(f"Message: {e.message}")
            
            if not test_case['expected_trigger']:
                print("WARNING: Guardrail triggered unexpectedly!")
        
        print("\n" + "-" * 50 + "\n")
```
This function:
- Creates a set of test cases covering different scenarios
- Tests each case against the tutor agent
- Checks if the output guardrails trigger as expected
- Provides detailed output about each test case

The test cases include both appropriate and inappropriate queries to verify that the output guardrails work correctly.

## Step 7: Creating a Simple Output Guardrail Demo 🔍
```python
# Function to demonstrate a simple output guardrail
async def simple_output_guardrail_demo():
    print("=== Simple Output Guardrail Demo ===\n")
    
    # Create a simple agent with just the math output guardrail
    simple_agent = Agent(
        name="Simple Tutor",
        instructions="You are a helpful tutor who assists with educational questions.",
        output_guardrails=[math_output_guardrail],
        output_type=MessageOutput,
    )
    
    # Test with a math question
    math_question = "Hello, can you help me solve for x: 2x + 3 = 11?"
    print(f"Testing with: \"{math_question}\"")
    
    try:
        result = await Runner.run(simple_agent, math_question)
        print("Guardrail didn't trip - this is unexpected")
        print(f"Response: {result.final_output.response}")
    except OutputGuardrailTripwireTriggered as e:
        print("Math output guardrail tripped")
        print(f"Message: {e.message}")
    
    # Test with a legitimate question
    legitimate_question = "Can you explain the concept of photosynthesis?"
    print(f"\nTesting with: \"{legitimate_question}\"")
    
    try:
        result = await Runner.run(simple_agent, legitimate_question)
        print("Guardrail not triggered (as expected)")
        print(f"Response: {result.final_output.response[:100]}...")
    except OutputGuardrailTripwireTriggered as e:
        print("Guardrail triggered unexpectedly")
        print(f"Message: {e.message}")
```
This function demonstrates a simpler version with just one output guardrail:
- Creates an agent with only the math output guardrail
- Tests it with a math question (should trigger the guardrail)
- Tests it with a legitimate question (should not trigger the guardrail)
- Shows the different responses in each case

This provides a clearer view of how a single output guardrail works in isolation.

## Step 8: Creating an Interactive Mode 💬
```python
# Interactive mode
print("\n=== Interactive Mode ===")
print("Enter questions to test the output guardrails, or 'exit' to quit")

while True:
    user_input = input("\nYour question: ")
    if user_input.lower() == 'exit':
        break
    
    try:
        result = await Runner.run(tutor_agent, user_input)
        print("\nResponse:")
        print(result.final_output.response)
    except OutputGuardrailTripwireTriggered as e:
        print("\nOutput guardrail triggered:")
        print(e.message)
```
This creates an interactive mode where:
- You can enter your own questions to test the output guardrails
- You'll see when guardrails are triggered and why
- You'll get normal responses for appropriate questions
- You can type "exit" to quit

## Final Summary 📌
✅ We created output models for different types of guardrail checks
✅ We created specialized agents to detect inappropriate content in responses
✅ We created output guardrail functions that use these agents
✅ We created a tutor agent with multiple output guardrails
✅ We tested the output guardrails with various inputs
✅ We created a simple demo with a single output guardrail
✅ We created an interactive mode for custom testing

## Try It Yourself! 🚀
1. Install the required packages:
   ```
   uv add openai-agents python-dotenv pydantic
   ```
2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Run the program:
   ```
   uv run outputguardrails.py
   ```
4. Try asking different types of questions to see how the output guardrails work!

## What You'll Learn 🧠
- How to create specialized detector agents for output guardrails
- How to define guardrail functions with the `@output_guardrail` decorator
- How to create structured output models for guardrail checks
- How to apply multiple output guardrails to an agent
- How to test output guardrails with different types of inputs
- How to handle guardrail exceptions in your code
- The difference between input guardrails and output guardrails

Happy coding! 🎉 