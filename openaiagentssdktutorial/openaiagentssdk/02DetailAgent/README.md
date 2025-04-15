# 🧩 Detail Agent Example

## What This Code Does (Big Picture)
Imagine having an AI tutor that can check if your question is about homework and then connect you with the right specialist! This code shows how to create a system with guardrails that verify if questions are homework-related, and then routes them to either a math tutor or history tutor based on the subject.

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv
from agents import set_default_openai_key
import os

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
```
The AI assistants need a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Creating a Homework Checker Model 📋
```python
# First we create a special checker that looks at homework questions
class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str
```
This creates a structured output format for our homework checker that includes:
- A boolean flag indicating whether the question is homework-related
- Reasoning that explains why the checker made its decision

## Step 3: Creating a Guardrail Agent to Check Homework 🛡️
```python
guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)
```
This creates an agent specifically designed to analyze questions and determine if they're homework-related, using our structured output format.

## Step 4: Creating Specialist Tutor Agents 👨‍🏫👩‍🏫
```python
# Then we create our specialist tutor agents
math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)
```
This creates two specialized tutor agents:
- A math tutor who explains reasoning step by step
- A history tutor who provides context and explanations for historical events

Each agent has a handoff description that explains when they should be used.

## Step 5: Creating a Homework Guardrail Function 🔍
```python
# This function checks if a question is homework-related
async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )
```
This function:
- Runs the guardrail agent to check if the question is homework-related
- Converts the result to our structured HomeworkOutput format
- Returns a guardrail output that triggers if the question is NOT homework-related
- This ensures that only homework questions are allowed through

## Step 6: Creating a Triage Agent with Guardrails and Handoffs 🧑‍💼
```python
# Finally, we create our main agent that decides which helper to use
triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)
```
This creates our main triage agent that:
- Has access to both specialist tutors through handoffs
- Uses the homework guardrail to verify questions are homework-related
- Can decide which specialist to use based on the question's subject

## Step 7: Running the Program with Different Questions 🏃‍♂️
```python
async def main():
    # First example - homework question about history
    result = await Runner.run(triage_agent, "who was the first president of the united states?")
    print("History question result:", result.final_output)
    
    # This would fail because it is not a homework question
    # result = await Runner.run(triage_agent, "What is life?")
    # print("Philosophy homework result:", result.final_output)

    # Second example - modified to be a homework question about philosophy
    result = await Runner.run(triage_agent, "For my philosophy homework, can you explain how ancient Greek philosophers viewed the meaning of life?")
    print("Philosophy homework result:", result.final_output)
```
This tests the system with different types of questions:
1. A history homework question about the first US president
2. A commented-out example that would fail the guardrail check (not homework)
3. A philosophy homework question that explicitly mentions it's for homework

## Final Summary 📌
✅ We created a structured output model for homework detection
✅ We created a guardrail agent to check if questions are homework-related
✅ We created specialist agents for math and history
✅ We created a guardrail function that only allows homework questions
✅ We created a triage agent that routes to the right specialist
✅ We tested the system with different types of questions

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
   uv run detailagent.py
   ```
4. Try modifying the guardrail to check for different conditions!

## What You'll Learn 🧠
- How to create multiple agents that work together
- How to use guardrails to check inputs and filter out inappropriate questions
- How to make agents hand off tasks to other specialist agents
- How to create structured outputs with Pydantic models
- How to use async functions with AI agents

Happy coding! 🎉 