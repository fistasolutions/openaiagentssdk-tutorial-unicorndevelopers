# 🌊 Streaming Responses with `run_streamed()`

## 📚 Overview

This tutorial demonstrates how to use streaming responses with AI agents using the `Runner.run_streamed()` method. Streaming allows you to receive and display the agent's response in real-time as it's being generated, providing a more interactive and engaging user experience.

## 🔍 Key Concepts Explained

### 🌊 What is Streaming?

- **Real-time**: Responses appear as they're generated, not all at once
- **Interactive**: Users see progress and can react immediately
- **Efficient**: Better perceived performance for long responses
- **Event-driven**: Uses events to handle incoming data chunks

### 🎯 The `Runner.run_streamed()` Method

`Runner.run_streamed()` provides:
- Real-time streaming of agent responses
- Event-based processing of response chunks
- Async iterator for handling stream events
- Immediate feedback to users

### 📡 Stream Events

The streaming system uses events to deliver content:
- **ResponseTextDeltaEvent**: Contains text chunks as they arrive
- **Raw Response Events**: Unprocessed response data
- **Stream Events**: Metadata about the streaming process

## 🎯 What You'll Learn

- How to implement streaming responses with agents
- Processing streaming events in real-time
- Understanding async iteration for streams
- Creating interactive AI experiences

## 🔧 Prerequisites

- Python 3.7+ installed
- Basic understanding of Python programming
- Knowledge of async/await patterns
- OpenAI API key
- Understanding of environment variables

## 📦 Required Dependencies

```bash
pip install openai-agents python-dotenv
```

## 🏗️ Project Structure

```
3runasyncstreaming/
├── 3runasyncstreaming.py    # Main script file
└── README.md                # This file
```

## 🔑 Environment Setup

Create a `.env` file in your project root with:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 📖 Code Explanation

### 1. Import Statements

```python
from agents import Agent, Runner
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
from agents import set_default_openai_key
import os
import asyncio
```

**What each import does:**
- `Agent`: The main class for creating AI agents
- `Runner`: Utility class for running agents (includes `run_streamed`)
- `ResponseTextDeltaEvent`: Event type for text chunks in streams
- `load_dotenv`: Loads environment variables from `.env` file
- `set_default_openai_key`: Sets the default API key for the SDK
- `os`: For accessing environment variables
- `asyncio`: For running asynchronous functions

### 2. Environment Configuration

```python
# Load API key
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
```

**Step-by-step explanation:**
1. `load_dotenv()`: Reads the `.env` file and loads variables
2. `os.environ.get("OPENAI_API_KEY")`: Retrieves the API key
3. `set_default_openai_key()`: Sets the API key for the SDK

### 3. Agent Creation

```python
# Create agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant that explains things clearly.",
    model="gpt-4o"
)
```

**Agent Configuration:**
- `name`: A friendly name for your agent
- `instructions`: The system prompt emphasizing clear explanations
- `model`: Using "gpt-4o" for optimal streaming performance

### 4. Streaming Function

```python
# Async function using streaming
async def main():
    print("=== Starting Stream ===")
    
    # Get the streaming result
    result = Runner.run_streamed(agent, "Explain recursion in programming in simple terms.")
    
    # Process the streaming events
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
    
    print("\n=== Stream Complete ===")
```

**What happens here:**
1. We define an `async` function for streaming
2. `Runner.run_streamed()` starts the streaming process
3. `async for` loop processes events as they arrive
4. We check for text delta events and print them immediately
5. `end=""` and `flush=True` ensure smooth output

### 5. Event Processing

```python
async for event in result.stream_events():
    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
        print(event.data.delta, end="", flush=True)
```

**Event Processing Breakdown:**
- `result.stream_events()`: Returns an async iterator of events
- `event.type == "raw_response_event"`: Filters for response events
- `isinstance(event.data, ResponseTextDeltaEvent)`: Ensures it's a text event
- `event.data.delta`: Contains the actual text chunk
- `end=""`: Prevents line breaks between chunks
- `flush=True`: Forces immediate output display

### 6. Execution

```python
# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
```

This line starts the execution of our streaming function.

## 🚀 How to Run

1. **Navigate to the directory:**
   ```bash
   cd 3runasyncstreaming
   ```

2. **Set up your environment:**
   - Create a `.env` file with your OpenAI API key
   - Install dependencies: `pip install openai-agents python-dotenv`

3. **Run the script:**
   ```bash
   uv run 3runasyncstreaming.py
   ```

## 📝 Expected Output

```
=== Starting Stream ===
Recursion is like a function that calls itself. Think of it as a Russian doll - each doll contains a smaller version of itself. In programming, a recursive function solves a problem by breaking it down into smaller, similar problems...
=== Stream Complete ===
```

## 🛠️ Customization Ideas

1. **Add typing indicators:**
   ```python
   async for event in result.stream_events():
       if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
           print(event.data.delta, end="", flush=True)
           await asyncio.sleep(0.01)  # Add slight delay for effect
   ```

2. **Color-coded streaming:**
   ```python
   import colorama
   colorama.init()
   
   async for event in result.stream_events():
       if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
           print(colorama.Fore.GREEN + event.data.delta, end="", flush=True)
   ```

3. **Progress indicators:**
   ```python
   chunk_count = 0
   async for event in result.stream_events():
       if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
           chunk_count += 1
           print(f"[{chunk_count}] {event.data.delta}", end="", flush=True)
   ```

## 🌊 When to Use Streaming

### ✅ **Use streaming when:**
- Building chat interfaces
- Creating interactive applications
- Providing real-time feedback
- Handling long responses
- Improving user experience

### ❌ **Don't use streaming when:**
- You need the complete response before processing
- Building batch processing systems
- Response length is always short
- You need to parse the entire response at once

## ⚠️ Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'agents'"
**Solution:** Install the SDK: `pip install openai-agents`

### Issue: "Stream events not appearing"
**Solution:** Ensure you're using `async for` and checking event types correctly

### Issue: "Output appears all at once"
**Solution:** Check that `flush=True` is set and `end=""` is used

### Issue: "OPENAI_API_KEY not found"
**Solution:** Check your `.env` file and ensure the API key is correct

## 🔗 Related Topics

- [Synchronous Agent Execution](../1runsync/)
- [Asynchronous Agent Execution](../2runasync/)
- [Agent Loops](../4agentloop/)
- [Configuration Management](../5runconfig/)

## 📚 Additional Resources

- [OpenAI Agents SDK Documentation](https://github.com/openai/openai-agents)
- [Python Async Iteration](https://realpython.com/async-io-python/)
- [Streaming in Web Applications](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API)

## 🎉 Next Steps

Once you understand streaming, try:
1. Building a chat interface with streaming
2. Adding typing indicators and animations
3. Implementing stream processing with filters
4. Creating interactive command-line tools

---

**Happy Coding! 🚀**

*This tutorial is part of the OpenAI Agents SDK learning series.* 