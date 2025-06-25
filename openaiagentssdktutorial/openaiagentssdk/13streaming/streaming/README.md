# 🌊 Advanced Streaming with Tools and Events

## 📚 Overview

This tutorial demonstrates advanced streaming capabilities with the OpenAI Agents SDK, including tool integration and real-time event processing. You'll learn how to handle different types of streaming events, integrate function tools, and process agent updates in real-time.

## 🔍 Key Concepts Explained

### 🌊 Advanced Streaming Events

- **Event Types**: Different categories of streaming events
- **Tool Integration**: Real-time tool execution and output
- **Agent Updates**: Dynamic agent changes during execution
- **Item Processing**: Handling various item types as they're generated

### 🎯 Streaming Event Types

The SDK provides several event types:
- **raw_response_event**: Raw model response data
- **agent_updated_stream_event**: Agent configuration changes
- **run_item_stream_event**: Items generated during execution
- **tool_call_item**: Tool execution requests
- **tool_call_output_item**: Tool execution results
- **message_output_item**: Agent message outputs

### 🔧 Function Tools in Streaming

Function tools can be:
- **Integrated**: Added to agents for enhanced capabilities
- **Streamed**: Executed and monitored in real-time
- **Processed**: Results handled as they become available

## 🎯 What You'll Learn

- How to implement advanced streaming with tools
- Processing different types of streaming events
- Integrating function tools with streaming agents
- Real-time event handling and processing
- Building interactive streaming applications

## 🔧 Prerequisites

- Python 3.7+ installed
- Basic understanding of Python programming
- Knowledge of async/await patterns
- Understanding of streaming basics (from previous tutorials)
- OpenAI API key
- Understanding of environment variables

## 📦 Required Dependencies

```bash
pip install openai-agents python-dotenv
```

## 🏗️ Project Structure

```
streaming/
├── streaming.py    # Main script file
└── README.md       # This file
```

## 🔑 Environment Setup

Create a `.env` file in your project root with:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
```

## 📖 Code Explanation

### 1. Import Statements

```python
import asyncio
import random
from agents import Agent, ItemHelpers, Runner, function_tool, set_default_openai_key
from dotenv import load_dotenv
import os
```

**What each import does:**
- `asyncio`: For asynchronous programming
- `random`: For generating random numbers in the tool
- `Agent`: The main class for creating AI agents
- `ItemHelpers`: Utility class for processing agent items
- `Runner`: Utility class for running agents
- `function_tool`: Decorator for creating function tools
- `set_default_openai_key`: Sets the default API key for the SDK
- `load_dotenv`: Loads environment variables from `.env` file
- `os`: For accessing environment variables

### 2. Environment Configuration

```python
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
model=os.environ.get("OPENAI_MODEL")
```

**Step-by-step explanation:**
1. `load_dotenv()`: Reads the `.env` file and loads variables
2. `set_default_openai_key()`: Sets the API key for the SDK
3. `os.environ.get("OPENAI_MODEL")`: Gets the model from environment

### 3. Function Tool Definition

```python
@function_tool
def how_many_jokes() -> int:
    return random.randint(1, 10)
```

**Tool Configuration:**
- `@function_tool`: Decorator that makes the function available to agents
- `how_many_jokes()`: Returns a random number between 1 and 10
- **Purpose**: Determines how many jokes the agent should tell

### 4. Main Function Setup

```python
async def main():
    agent = Agent(
        name="Joker",
        instructions="First call the `how_many_jokes` tool, then tell that many jokes.",
        tools=[how_many_jokes],
        model=model
    )
```

**Agent Configuration:**
- `name`: "Joker" - specialized for telling jokes
- `instructions`: Clear directive to use the tool first, then tell jokes
- `tools=[how_many_jokes]`: Makes the tool available to the agent
- `model`: Uses the model specified in environment variables

### 5. Streaming Execution

```python
result = Runner.run_streamed(
    agent,
    input="Hello",
)
print("=== Run starting ===")
```

**What happens here:**
1. `Runner.run_streamed()` starts the streaming process
2. Agent receives "Hello" as input
3. Agent will call the tool and then tell jokes
4. All events are streamed in real-time

### 6. Event Processing Loop

```python
async for event in result.stream_events():
    # We'll ignore the raw responses event deltas
    if event.type == "raw_response_event":
        continue
    # When the agent updates, print that
    elif event.type == "agent_updated_stream_event":
        print(f"Agent updated: {event.new_agent.name}")
        continue
    # When items are generated, print them
    elif event.type == "run_item_stream_event":
        if event.item.type == "tool_call_item":
            print("-- Tool was called")
        elif event.item.type == "tool_call_output_item":
            print(f"-- Tool output: {event.item.output}")
        elif event.item.type == "message_output_item":
            print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
        else:
            pass  # Ignore other event types
```

**Event Processing Breakdown:**
- `async for event in result.stream_events()`: Iterates through streaming events
- **raw_response_event**: Ignored (contains raw model data)
- **agent_updated_stream_event**: Shows when agent configuration changes
- **run_item_stream_event**: Processes different item types:
  - `tool_call_item`: Tool execution request
  - `tool_call_output_item`: Tool execution result
  - `message_output_item`: Agent message output

## 🚀 How to Run

1. **Navigate to the directory:**
   ```bash
   cd streaming
   ```

2. **Set up your environment:**
   - Create a `.env` file with your OpenAI API key and model
   - Install dependencies: `pip install openai-agents python-dotenv`

3. **Run the script:**
   ```bash
   uv run streaming.py
   ```

## 📝 Expected Output

```
=== Run starting ===
-- Tool was called
-- Tool output: 7
-- Message output:
 Here are 7 jokes for you:

1. Why don't scientists trust atoms? Because they make up everything!
2. Why did the scarecrow win an award? Because he was outstanding in his field!
...
=== Run complete ===
```

## 🛠️ Customization Ideas

1. **Add more tools:**
   ```python
   @function_tool
   def get_current_time() -> str:
       from datetime import datetime
       return datetime.now().strftime("%H:%M:%S")
   
   @function_tool
   def calculate_fibonacci(n: int) -> int:
       if n <= 1:
           return n
       return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
   
   agent = Agent(
       name="MultiTool Agent",
       instructions="Use tools as needed to help users.",
       tools=[how_many_jokes, get_current_time, calculate_fibonacci],
       model=model
   )
   ```

2. **Enhanced event processing:**
   ```python
   async for event in result.stream_events():
       if event.type == "run_item_stream_event":
           if event.item.type == "tool_call_item":
               print(f"🔧 Tool called: {event.item.tool_name}")
           elif event.item.type == "tool_call_output_item":
               print(f"📤 Tool result: {event.item.output}")
           elif event.item.type == "message_output_item":
               message = ItemHelpers.text_message_output(event.item)
               print(f"💬 Agent says: {message}")
   ```

3. **Event logging:**
   ```python
   import json
   from datetime import datetime
   
   async def log_events(result):
       events_log = []
       async for event in result.stream_events():
           event_data = {
               "timestamp": datetime.now().isoformat(),
               "type": event.type,
               "data": str(event.data) if hasattr(event, 'data') else None
           }
           events_log.append(event_data)
           print(f"Event: {event.type}")
       
       # Save to file
       with open('events_log.json', 'w') as f:
           json.dump(events_log, f, indent=2)
   ```

## 🌊 Advanced Streaming Patterns

### Event Filtering

```python
async def process_specific_events(result, event_types=None):
    """Process only specific event types"""
    if event_types is None:
        event_types = ["run_item_stream_event"]
    
    async for event in result.stream_events():
        if event.type in event_types:
            yield event
```

### Real-time Analytics

```python
class StreamingAnalytics:
    def __init__(self):
        self.tool_calls = 0
        self.messages = 0
        self.agent_updates = 0
    
    async def analyze_stream(self, result):
        async for event in result.stream_events():
            if event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    self.tool_calls += 1
                elif event.item.type == "message_output_item":
                    self.messages += 1
            elif event.type == "agent_updated_stream_event":
                self.agent_updates += 1
        
        return {
            "tool_calls": self.tool_calls,
            "messages": self.messages,
            "agent_updates": self.agent_updates
        }
```

### Interactive Streaming

```python
async def interactive_streaming(agent, initial_input):
    """Interactive streaming with user input"""
    result = Runner.run_streamed(agent, initial_input)
    
    print("Streaming started... (Press Ctrl+C to stop)")
    
    try:
        async for event in result.stream_events():
            if event.type == "run_item_stream_event":
                if event.item.type == "message_output_item":
                    message = ItemHelpers.text_message_output(event.item)
                    print(f"Agent: {message}", end="", flush=True)
    except KeyboardInterrupt:
        print("\nStreaming stopped by user")
```

## 🌊 When to Use Advanced Streaming

### ✅ **Use advanced streaming when:**
- Building interactive applications
- Need real-time tool execution feedback
- Implementing complex agent workflows
- Creating debugging and monitoring tools
- Building user-facing streaming interfaces

### ❌ **Don't use advanced streaming when:**
- Simple one-off agent calls
- Batch processing
- Performance-critical applications
- When you don't need real-time feedback

## ⚠️ Common Issues & Solutions

### Issue: "Event type not recognized"
**Solution:** Check the SDK version and event type spelling

### Issue: "Tool not being called"
**Solution:** Ensure the tool is properly decorated and added to the agent

### Issue: "Streaming events not appearing"
**Solution:** Verify you're using `async for` and checking event types correctly

### Issue: "ModuleNotFoundError: No module named 'agents'"
**Solution:** Install the SDK: `pip install openai-agents`

## 🔗 Related Topics

- [Basic Streaming](../../11runningagents/3runasyncstreaming/)
- [Function Tools](../../15tools/8functiontool/)
- [Custom Function Tools](../../15tools/9customfunctiontool/)
- [Agent Loops](../../11runningagents/4agentloop/)
- [REPL Interface](../repl/)

## 📚 Additional Resources

- [OpenAI Agents SDK Documentation](https://github.com/openai/openai-agents)
- [Python Async Programming](https://realpython.com/async-io-python/)
- [Event-Driven Programming](https://en.wikipedia.org/wiki/Event-driven_programming)

## 🎉 Next Steps

Once you understand advanced streaming, try:
1. Building interactive streaming applications
2. Creating real-time monitoring dashboards
3. Implementing complex tool workflows
4. Building streaming analytics systems

---

**Happy Coding! 🚀**

*This tutorial is part of the OpenAI Agents SDK learning series.* 