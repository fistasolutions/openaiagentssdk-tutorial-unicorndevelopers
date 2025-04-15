# 🌟 Gemini AI Assistant Configuration

## What This Code Does (Big Picture)
This code creates an AI assistant using Google's Gemini 2.0 Flash model through the OpenAI Agents SDK. It demonstrates how to configure and use Gemini as an alternative to OpenAI models, asking it to explain recursion in programming.

Now, let's go step by step!

## Step 1: Importing Required Libraries 📚
```python
import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import asyncio
```
This section imports all the necessary libraries:
- `os` and `dotenv` for environment variable management
- `Agent`, `Runner`, `AsyncOpenAI`, and `OpenAIChatCompletionsModel` from the agents package
- `RunConfig` for configuring the agent run
- `asyncio` for handling asynchronous operations

## Step 2: Setting Up the Magic Key 🗝️
```python
# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")
```
The AI assistant needs a magic key (API key) to work properly.

This code finds the Gemini API key hidden in a secret file (.env), unlocks it, and checks if it's available before proceeding.

## Step 3: Configuring the Gemini Client 🤖
```python
#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)
```
This section:
- Creates a client that connects to Google's Gemini API using OpenAI's format
- Sets up the Gemini 2.0 Flash model
- Configures the run settings for the agent

## Step 4: Creating Your AI Assistant 🧠
```python
async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are helpful Assistent.",
        model=model
    )
```
This creates your AI friend and:
- Gives it a name: "Assistant"
- Tells it how to behave: "Be helpful"
- Sets which AI brain to use: Google's Gemini 2.0 Flash model

Note that this is inside an async function called `main()`, which is necessary for using the async/await pattern.

## Step 5: Asking the AI About Recursion 🔄
```python
    result = await Runner.run(agent, "Tell me about recursion in programming.", run_config=config)
```
This line:
- Sends your question to the AI
- Waits for it to think and respond
- Stores the answer in a variable called `result`

## Step 6: Showing the AI's Answer 📝
```python
    print(result.final_output)
    # Function calls itself,
    # Looping in smaller pieces,
    # Endless by design.
```
This displays the explanation about recursion that the AI provided!

The comments after the print statement are a poetic description of recursion:
- "Function calls itself" - the basic definition of recursion
- "Looping in smaller pieces" - how recursion breaks down problems
- "Endless by design" - the potential for infinite recursion if not properly controlled

## Step 7: Running the Async Code 🚀
```python
if __name__ == "__main__":
    asyncio.run(main())
```
This section:
- Checks if the script is being run directly (not imported)
- Uses `asyncio.run()` to execute the asynchronous `main()` function
- This is necessary because we're using async/await patterns in our code

## Final Summary 📌
✅ We created an AI assistant using Google's Gemini 2.0 Flash model
✅ We configured it to work with the OpenAI Agents SDK
✅ We used asynchronous programming with asyncio
✅ We asked it to explain recursion in programming
✅ We displayed the explanation it created

## Try It Yourself! 🚀
1. Install the required packages:
   ```
   uv add openai-agents python-dotenv
   ```
2. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Run the program:
   ```
   uv run geminiconfig.py
   ```
4. Try changing the question to ask about different programming concepts!

## What You'll Learn 🧠
- How to configure and use Google's Gemini model with the OpenAI Agents SDK
- How to set up an external client for alternative AI models
- How to create an agent with a specific model configuration
- How to run asynchronous agent interactions
- How to use asyncio for handling asynchronous operations

Happy coding! 🎉 