# 🛡️ Guardrails Example

## What This Code Does (Big Picture)
Imagine having an AI tutor that can detect when students are asking for homework answers instead of learning help! This code shows how to create intelligent guardrails that can analyze user requests and block inappropriate ones, like requests for direct solutions to math problems, coding assignments, or essay writing.

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
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    set_default_openai_key
)
```
The AI assistants need a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Creating Output Models for Guardrail Checks 📋
```python
# Define output models for guardrail checks
class MathHomeworkOutput(BaseModel):
    is_math_homework: bool = Field(..., description="Whether the query appears to be math homework")
    reasoning: str = Field(..., description="Explanation of why this is or isn't math homework")

class CodeAssignmentOutput(BaseModel):
    is_code_assignment: bool = Field(..., description="Whether the query appears to be a coding assignment")
    reasoning: str = Field(..., description="Explanation of why this is or isn't a coding assignment")

class EssayWritingOutput(BaseModel):
    is_essay_request: bool = Field(..., description="Whether the query appears to be asking for an essay")
    reasoning: str = Field(..., description="Explanation of why this is or isn't an essay request")
    subject: Optional[str] = Field(None, description="The subject of the essay if applicable")
```
These create structured output models for different types of guardrail checks:
- `MathHomeworkOutput`: For detecting math homework requests
- `CodeAssignmentOutput`: For detecting coding assignment requests
- `EssayWritingOutput`: For detecting essay writing requests

Each model includes a boolean flag indicating whether the request is inappropriate, reasoning for the decision, and in the case of essays, the subject.

## Step 3: Creating Specialized Guardrail Agents 🕵️‍♂️
```python
# Create specialized guardrail agents
math_guardrail_agent = Agent(
    name="Math Homework Detector",
    instructions="""
    You are a specialized agent that detects if users are asking for help with math homework.
    
    Analyze the input to determine if it's asking for direct solutions to math problems that appear to be homework.
    
    Consider these as math homework:
    - Explicit requests to solve equations or math problems
    - Questions that ask for step-by-step solutions to math problems
    - Requests that use phrases like "solve for x" or similar academic language
    
    Don't consider these as math homework:
    - General questions about math concepts
    - Requests for explanations of mathematical principles
    - Questions about how to approach a type of problem (without asking for the specific solution)
    - Real-world math applications (like calculating a tip or mortgage payment)
    
    Provide clear reasoning for your decision.
    """,
    output_type=MathHomeworkOutput,
)

code_guardrail_agent = Agent(
    name="Code Assignment Detector",
    instructions="""
    You are a specialized agent that detects if users are asking for help with coding assignments.
    
    Analyze the input to determine if it's asking for direct solutions to coding problems that appear to be assignments.
    
    Consider these as code assignments:
    - Explicit requests to write code for specific problems with assignment-like framing
    - Questions that include requirements lists or specifications that sound like coursework
    - Requests that use phrases like "implement a function that..." or similar academic language
    
    Don't consider these as code assignments:
    - General questions about programming concepts
    - Requests for explanations of coding principles
    - Questions about debugging existing code
    - Professional development questions
    
    Provide clear reasoning for your decision.
    """,
    output_type=CodeAssignmentOutput,
)

essay_guardrail_agent = Agent(
    name="Essay Request Detector",
    instructions="""
    You are a specialized agent that detects if users are asking for help writing essays or papers.
    
    Analyze the input to determine if it's asking for direct writing of essays that appear to be academic assignments.
    
    Consider these as essay requests:
    - Explicit requests to write essays, papers, or reports on specific topics
    - Questions that include word counts, formatting requirements, or citation styles
    - Requests that use phrases like "write an essay about..." or similar academic language
    
    Don't consider these as essay requests:
    - Requests for outlines or brainstorming help
    - Questions about essay structure or writing techniques
    - Requests for feedback on existing writing
    - Professional writing assistance (like resume help)
    
    Provide clear reasoning for your decision and identify the subject if it's an essay request.
    """,
    output_type=EssayWritingOutput,
)
```
This creates three specialized agents:
- A math homework detector that identifies requests for direct math solutions
- A code assignment detector that identifies requests for coding assignment solutions
- An essay request detector that identifies requests for writing essays

Each agent is configured with specific instructions about what to consider inappropriate and what's acceptable, along with the appropriate output type.

## Step 4: Creating Guardrail Functions 🛡️
```python
# Define guardrail functions
@input_guardrail
async def math_homework_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: Union[str, List[TResponseInputItem]]
) -> GuardrailFunctionOutput:
    """Detect and block requests for math homework help."""
    result = await Runner.run(math_guardrail_agent, input, context=ctx.context)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework,
        message="I'm sorry, but I can't help with solving math homework problems directly. I'd be happy to explain math concepts or guide you through the problem-solving process instead."
    )

@input_guardrail
async def code_assignment_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: Union[str, List[TResponseInputItem]]
) -> GuardrailFunctionOutput:
    """Detect and block requests for coding assignment solutions."""
    result = await Runner.run(code_guardrail_agent, input, context=ctx.context)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_code_assignment,
        message="I'm sorry, but I can't write code for assignments directly. I'd be happy to explain programming concepts, help debug issues, or guide you through the development process instead."
    )

@input_guardrail
async def essay_writing_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: Union[str, List[TResponseInputItem]]
) -> GuardrailFunctionOutput:
    """Detect and block requests for writing essays."""
    result = await Runner.run(essay_guardrail_agent, input, context=ctx.context)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_essay_request,
        message="I'm sorry, but I can't write essays or papers for academic assignments. I'd be happy to help with brainstorming ideas, creating outlines, or providing feedback on your writing instead."
    )
```
These functions create the actual guardrails:
- Each is decorated with `@input_guardrail` to mark it as a guardrail function
- Each runs its specialized detector agent on the input
- Each returns a `GuardrailFunctionOutput` with:
  - The detailed output from the detector
  - A boolean indicating whether the guardrail should be triggered
  - A helpful message explaining why the request was blocked and offering alternatives

## Step 5: Creating a Tutor Agent with Guardrails 🤖
```python
# Create a main agent with guardrails
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
    input_guardrails=[
        math_homework_guardrail,
        code_assignment_guardrail,
        essay_writing_guardrail,
    ],
)
```
This creates an educational tutor agent that:
- Helps students learn and understand various subjects
- Is configured with all three guardrails to prevent inappropriate requests
- Focuses on explaining concepts rather than giving direct answers

## Step 6: Creating a Function to Test Guardrails 🧪
```python
# Function to test guardrails with various inputs
async def test_guardrails():
    print("=== Testing Guardrails ===\n")
    
    test_cases = [
        {
            "name": "Math Homework",
            "input": "Can you solve this equation for me? 3x + 7 = 22",
            "expected_trigger": True,
            "guardrail_type": "Math Homework"
        },
        {
            "name": "Math Concept",
            "input": "Can you explain how derivatives work in calculus?",
            "expected_trigger": False,
            "guardrail_type": "Math Homework"
        },
        {
            "name": "Code Assignment",
            "input": "Write a Python function that implements a binary search tree with insert, delete, and search operations.",
            "expected_trigger": True,
            "guardrail_type": "Code Assignment"
        },
        {
            "name": "Code Help",
            "input": "I'm getting an IndexError in my Python code. How do I debug this?",
            "expected_trigger": False,
            "guardrail_type": "Code Assignment"
        },
        {
            "name": "Essay Request",
            "input": "Write a 1000-word essay on the causes and effects of climate change. Include at least 5 sources.",
            "expected_trigger": True,
            "guardrail_type": "Essay Request"
        },
        {
            "name": "Essay Help",
            "input": "What's a good structure for an argumentative essay?",
            "expected_trigger": False,
            "guardrail_type": "Essay Request"
        },
        {
            "name": "General Question",
            "input": "What are some good study habits for college students?",
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
            print(f"Response: {result.final_output[:100]}...")
            
            if test_case['expected_trigger']:
                print("WARNING: Expected guardrail to trigger, but it didn't!")
            
        except InputGuardrailTripwireTriggered as e:
            print(f"Result: Guardrail triggered")
            print(f"Message: {e.message}")
            
            if not test_case['expected_trigger']:
                print("WARNING: Guardrail triggered unexpectedly!")
        
        print("\n" + "-" * 50 + "\n")
```
This function:
- Creates a set of test cases covering different scenarios
- Tests each case against the tutor agent
- Checks if the guardrails trigger as expected
- Provides detailed output about each test case

The test cases include both appropriate and inappropriate requests to verify that the guardrails work correctly.

## Step 7: Creating a Simple Guardrail Demo 🔍
```python
# Function to demonstrate a simple guardrail
async def simple_guardrail_demo():
    print("=== Simple Guardrail Demo ===\n")
    
    # Create a simple agent with just the math homework guardrail
    simple_agent = Agent(
        name="Simple Tutor",
        instructions="You are a helpful tutor who assists with educational questions.",
        input_guardrails=[math_homework_guardrail],
    )
    
    # Test with a math homework question
    math_question = "Hello, can you help me solve for x: 2x + 3 = 11?"
    print(f"Testing with: \"{math_question}\"")
    
    try:
        result = await Runner.run(simple_agent, math_question)
        print("Guardrail didn't trip - this is unexpected")
        print(f"Response: {result.final_output}")
    except InputGuardrailTripwireTriggered as e:
        print("Math homework guardrail tripped")
        print(f"Message: {e.message}")
    
    # Test with a legitimate question
    legitimate_question = "Can you explain the concept of photosynthesis?"
    print(f"\nTesting with: \"{legitimate_question}\"")
    
    try:
        result = await Runner.run(simple_agent, legitimate_question)
        print("Guardrail not triggered (as expected)")
        print(f"Response: {result.final_output[:100]}...")
    except InputGuardrailTripwireTriggered as e:
        print("Guardrail triggered unexpectedly")
        print(f"Message: {e.message}")
```
This function demonstrates a simpler version with just one guardrail:
- Creates an agent with only the math homework guardrail
- Tests it with a math homework question (should be blocked)
- Tests it with a legitimate question (should be allowed)
- Shows the different responses in each case

This provides a clearer view of how a single guardrail works in isolation.

## Step 8: Creating an Interactive Mode 💬
```python
# Interactive mode
print("\n=== Interactive Mode ===")
print("Enter questions to test the guardrails, or 'exit' to quit")

while True:
    user_input = input("\nYour question: ")
    if user_input.lower() == 'exit':
        break
    
    try:
        result = await Runner.run(tutor_agent, user_input)
        print("\nResponse:")
        print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("\nGuardrail triggered:")
        print(e.message)
```
This creates an interactive mode where:
- You can enter your own questions to test the guardrails
- You'll see when guardrails are triggered and why
- You'll get normal responses for appropriate questions
- You can type "exit" to quit

## Final Summary 📌
✅ We created output models for different types of guardrail checks
✅ We created specialized agents to detect inappropriate requests
✅ We created guardrail functions that use these agents
✅ We created a tutor agent with multiple guardrails
✅ We tested the guardrails with various inputs
✅ We created a simple demo with a single guardrail
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
   uv run guardrails.py
   ```
4. Try asking different types of questions to see how the guardrails work!

## What You'll Learn 🧠
- How to create specialized detector agents for guardrails
- How to define guardrail functions with the `@input_guardrail` decorator
- How to create structured output models for guardrail checks
- How to apply multiple guardrails to an agent
- How to test guardrails with different types of inputs
- How to handle guardrail exceptions in your code

Happy coding! 🎉 