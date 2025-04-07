# 🌟 Hello World AI Assistant

## What This Code Does (Big Picture)
Imagine having a robot friend who can write poetry! This code creates a simple AI assistant using OpenAI's GPT-4o and asks it to write a haiku poem about recursion in programming.

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
from agents import Agent, Runner
from dotenv import load_dotenv
from agents import set_default_openai_key
import os

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
```
The AI assistant needs a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Creating Your AI Assistant 🤖
```python
agent = Agent(
    name="Assistant", 
    instructions="You are a helpful assistant", 
    model="gpt-4o"
)
```
This creates your AI friend and:
- Gives it a name: "Assistant"
- Tells it how to behave: "Be helpful"
- Sets which AI brain to use: OpenAI's GPT-4o model

## Step 3: Asking the AI to Write a Haiku ✍️
```python
result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
```
This line:
- Sends your question to the AI
- Waits for it to think and create a haiku
- Stores the answer in a variable called `result`

## Step 4: Showing the AI's Answer 📝
```python
print(result.final_output)
```
This displays the haiku that the AI wrote for you!

## Final Summary 📌
✅ We created an AI assistant using OpenAI's GPT-4o
✅ We gave it instructions to be helpful
✅ We asked it to write a haiku about recursion
✅ We displayed the haiku it created

## Try It Yourself! 🚀
1. Install the required packages:
   ```
   uv add openai-agents python-dotenv
   ```
2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Run the program:
   ```
   uv run helloworld.py
   ```
4. Try changing the question to ask for different haikus or other creative writing!

## What You'll Learn 🧠
- How to create a basic AI agent with OpenAI
- How to give it instructions
- How to ask it questions
- How to get its response

Happy coding! 🎉
