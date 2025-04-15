# 🌊 Streaming Raw Response Example

## What This Code Does (Big Picture)
Imagine watching your robot friend think out loud, seeing its answers appear letter by letter in real-time! This code shows how to get AI responses as they're being generated, instead of waiting for the complete answer.

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
import asyncio
from openai.types.chat import ChatCompletionChunk
from openai.types.chat.chat_completion_chunk import ChoiceDelta
from agents import Agent, Runner, set_default_openai_key
from dotenv import load_dotenv
import os
import time

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
```
The AI assistant needs a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Creating a Joke-Telling AI 🤖
```python
agent = Agent(
    name="Joker",
    instructions="""
    You are a friendly assistant who specializes in telling jokes.
    When asked for jokes, provide clean, family-friendly humor.
    Make your jokes engaging and suitable for all audiences.
    """,
)
```
This creates an AI assistant that specializes in telling jokes.

## Step 3: Running the Agent with Streaming Enabled 🌊
```python
print("\n--- Streaming Jokes Example ---")
print("Asking for 5 jokes...\n")

# Run the agent with streaming enabled
result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")
```
This runs the agent in streaming mode, which means we'll get the response piece by piece as it's generated.

## Step 4: Processing the Streaming Events 📊
```python
# Process the streaming events
print("Response: ", end="", flush=True)
async for event in result.stream_events():
    if event.type == "raw_response_event" and isinstance(event.data, ChatCompletionChunk):
        # Extract the text delta from the event
        for choice in event.data.choices:
            if choice.delta and choice.delta.content:
                print(choice.delta.content, end="", flush=True)
                # Add a small delay to make the streaming more visible
                await asyncio.sleep(0.01)
```
This code:
1. Listens for streaming events from the AI
2. Checks if the event contains new text
3. Prints each piece of text as it arrives
4. Uses `flush=True` to make sure it appears immediately
5. Adds a tiny delay to make the streaming more visible

## Step 5: Creating a Storyteller AI 📚
```python
# Create a storyteller agent
storyteller = Agent(
    name="Storyteller",
    instructions="""
    You are a creative storyteller who crafts engaging short stories.
    Keep your stories concise but captivating, with interesting characters and plots.
    Your stories should have a clear beginning, middle, and end.
    """,
)

# Run the storyteller agent with streaming enabled
result = Runner.run_streamed(storyteller, input="Tell me a short story about a robot learning to paint.")
```
This creates a second AI assistant that specializes in telling short stories, and runs it with streaming enabled.

## Step 6: Measuring Streaming Speed ⏱️
```python
# Process the streaming events with timing information
start_time = time.time()
last_update = start_time
chars_received = 0

print("Response: ", end="", flush=True)
async for event in result.stream_events():
    if event.type == "raw_response_event" and isinstance(event.data, ChatCompletionChunk):
        for choice in event.data.choices:
            if choice.delta and choice.delta.content:
                content = choice.delta.content
                print(content, end="", flush=True)
                
                # Update statistics
                now = time.time()
                chars_received += len(content)
                if now - last_update >= 1.0:  # Update stats every second
                    elapsed = now - start_time
                    chars_per_second = chars_received / elapsed
                    last_update = now

# Print final statistics
total_time = time.time() - start_time
total_chars = chars_received
avg_chars_per_second = total_chars / total_time

print(f"\n\nStreaming Statistics:")
print(f"Total characters: {total_chars}")
print(f"Total time: {total_time:.2f} seconds")
print(f"Average speed: {avg_chars_per_second:.2f} characters per second")
```
This code tracks:
- When the streaming started
- How many characters we've received
- How fast the characters are coming in (characters per second)
- And displays final statistics about the streaming performance

## Step 7: Creating an Interactive Streaming Chat 💬
```python
# Interactive mode with streaming
print("\n--- Interactive Streaming Mode ---")
print("Type 'exit' to quit")

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == 'exit':
        break
    
    print("Assistant: ", end="", flush=True)
    result = Runner.run_streamed(agent, input=user_input)
    
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ChatCompletionChunk):
            for choice in event.data.choices:
                if choice.delta and choice.delta.content:
                    print(choice.delta.content, end="", flush=True)
    print()  # Add a newline after the response
```
This creates an interactive chat where:
- You can type messages and get streaming responses
- You see the AI's answers appear character by character
- The responses are properly formatted with newlines
- You can type "exit" to quit

## Final Summary 📌
✅ We created a joke-telling AI assistant
✅ We created a storytelling AI assistant
✅ We enabled streaming to see responses in real-time
✅ We processed streaming events to display text as it arrives
✅ We measured how fast the streaming responses come in
✅ We created an interactive streaming chat interface

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
   uv run streamingrawresponse.py
   ```
4. Watch as the jokes and stories appear character by character!

## What You'll Learn 🧠
- How to enable streaming for AI responses
- How to process streaming events in real-time
- How to display text character-by-character as it arrives
- How to measure response speed and performance
- How to create an interactive streaming chat
- How to work with different types of streaming agents

Happy coding! 🎉 