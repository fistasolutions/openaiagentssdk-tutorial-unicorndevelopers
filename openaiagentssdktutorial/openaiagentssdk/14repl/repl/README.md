# 💬 REPL Interface with OpenAI Agents SDK

## 📚 Overview

This tutorial demonstrates how to create a REPL (Read-Eval-Print Loop) interface for interactive conversations with AI agents using the OpenAI Agents SDK. You'll learn how to build an interactive command-line interface that allows real-time conversations with agents.

## 🔍 Key Concepts Explained

### 💬 What is a REPL?

- **Interactive Interface**: Real-time conversation with agents
- **Read-Eval-Print Loop**: Continuous input, processing, and output cycle
- **User-Friendly**: Simple command-line interface for agent interactions
- **Persistent Session**: Maintains conversation context across interactions

### 🎯 REPL Components

A REPL typically consists of:
- **Input Handler**: Reads user commands and messages
- **Agent Processor**: Processes input through the agent
- **Output Display**: Shows agent responses
- **Loop Control**: Manages the conversation flow

### 🔄 REPL vs Single Execution

| Approach | Interaction | Context | Use Case |
|----------|-------------|---------|----------|
| **Single Execution** | One-time | None | Scripts, batch processing |
| **REPL Interface** | Continuous | Maintained | Interactive conversations |

## 🎯 What You'll Learn

- How to create interactive REPL interfaces
- Using `run_demo_loop` for agent conversations
- Building persistent conversation sessions
- Managing interactive agent workflows
- Creating user-friendly agent interfaces

## 🔧 Prerequisites

- Python 3.7+ installed
- Basic understanding of Python programming
- Knowledge of async/await patterns
- Understanding of agent basics (from previous tutorials)
- OpenAI API key
- Understanding of environment variables

## 📦 Required Dependencies

```bash
pip install openai-agents python-dotenv
```

## 🏗️ Project Structure

```
repl/
├── repl.py    # Main script file
└── README.md  # This file
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
from agents import Agent, run_demo_loop, set_default_openai_key
from dotenv import load_dotenv
import os
```

**What each import does:**
- `asyncio`: For asynchronous programming
- `Agent`: The main class for creating AI agents
- `run_demo_loop`: Built-in REPL interface function
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

### 3. Agent Creation

```python
agent = Agent(name="Assistant", instructions="You are a helpful assistant.", model=model)
```

**Agent Configuration:**
- `name`: "Assistant" - general-purpose conversational agent
- `instructions`: Clear directive to be helpful
- `model`: Uses the model specified in environment variables

### 4. REPL Interface

```python
async def main() -> None:
    agent = Agent(name="Assistant", instructions="You are a helpful assistant.", model=model)
    await run_demo_loop(agent)
```

**REPL Setup:**
- `async def main()`: Asynchronous main function
- `run_demo_loop(agent)`: Starts the interactive REPL interface
- The function handles the entire conversation loop

### 5. Execution

```python
if __name__ == "__main__":
    asyncio.run(main())
```

**What happens here:**
1. `asyncio.run(main())` starts the asynchronous execution
2. The REPL interface begins
3. Users can interact with the agent in real-time

## 🚀 How to Run

1. **Navigate to the directory:**
   ```bash
   cd repl
   ```

2. **Set up your environment:**
   - Create a `.env` file with your OpenAI API key and model
   - Install dependencies: `pip install openai-agents python-dotenv`

3. **Run the script:**
   ```bash
   uv run repl.py
   ```

## 📝 Expected Output

```
Welcome to the Agent REPL!
Type your message and press Enter to chat with the agent.
Type 'quit' or 'exit' to end the conversation.

You: Hello, how are you?
Assistant: Hello! I'm doing well, thank you for asking. I'm here to help you with any questions or tasks you might have. How can I assist you today?

You: What's the weather like?
Assistant: I don't have access to real-time weather information, but I can help you find weather data through various methods. You could check a weather website, use a weather app, or I could help you write code to fetch weather data from an API if you're interested in that approach.

You: quit
Goodbye!
```

## 🛠️ Customization Ideas

1. **Custom REPL with enhanced features:**
   ```python
   async def custom_repl(agent):
       print("🤖 Custom Agent REPL")
       print("Commands: /help, /clear, /quit")
       
       conversation_history = []
       
       while True:
           try:
               user_input = input("\nYou: ").strip()
               
               if user_input.lower() in ['quit', 'exit', '/quit']:
                   print("👋 Goodbye!")
                   break
               elif user_input == '/help':
                   print("Available commands:")
                   print("- /help: Show this help")
                   print("- /clear: Clear conversation history")
                   print("- /quit: Exit the REPL")
                   continue
               elif user_input == '/clear':
                   conversation_history = []
                   print("🗑️ Conversation history cleared")
                   continue
               
               # Add user input to history
               conversation_history.append({"role": "user", "content": user_input})
               
               # Get agent response
               result = await Runner.run(agent, conversation_history)
               
               # Add agent response to history
               conversation_history.append({"role": "assistant", "content": result.final_output})
               
               print(f"🤖 Assistant: {result.final_output}")
               
           except KeyboardInterrupt:
               print("\n👋 Goodbye!")
               break
           except Exception as e:
               print(f"❌ Error: {e}")
   ```

2. **Specialized agent REPL:**
   ```python
   async def specialized_repl():
       # Create specialized agents
       agents = {
           "general": Agent(name="General", instructions="You are a helpful assistant."),
           "tech": Agent(name="Tech", instructions="You are a technical expert."),
           "creative": Agent(name="Creative", instructions="You are a creative assistant.")
       }
       
       current_agent = agents["general"]
       
       while True:
           user_input = input("\nYou: ").strip()
           
           if user_input.lower() == 'quit':
               break
           elif user_input.startswith('/switch '):
               agent_type = user_input.split(' ')[1]
               if agent_type in agents:
                   current_agent = agents[agent_type]
                   print(f"🔄 Switched to {agent_type} agent")
               else:
                   print(f"❌ Unknown agent: {agent_type}")
               continue
           
           result = await Runner.run(current_agent, user_input)
           print(f"🤖 {current_agent.name}: {result.final_output}")
   ```

3. **REPL with tools:**
   ```python
   from agents import function_tool
   
   @function_tool
   def get_time() -> str:
       from datetime import datetime
       return datetime.now().strftime("%H:%M:%S")
   
   async def tool_repl():
       agent = Agent(
           name="Tool Assistant",
           instructions="You can use tools to help users.",
           tools=[get_time]
       )
       
       await run_demo_loop(agent)
   ```

## 💬 Building Advanced REPL Interfaces

### REPL with History

```python
class REPLWithHistory:
    def __init__(self, agent):
        self.agent = agent
        self.conversation_history = []
        self.command_history = []
    
    async def start(self):
        print("🤖 REPL with History")
        print("Commands: /history, /save, /load, /quit")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                self.command_history.append(user_input)
                
                if user_input.lower() == '/quit':
                    break
                elif user_input == '/history':
                    self.show_history()
                    continue
                elif user_input == '/save':
                    self.save_conversation()
                    continue
                elif user_input == '/load':
                    self.load_conversation()
                    continue
                
                # Process with agent
                result = await Runner.run(self.agent, user_input)
                print(f"🤖 Assistant: {result.final_output}")
                
                # Update history
                self.conversation_history.extend([
                    {"role": "user", "content": user_input},
                    {"role": "assistant", "content": result.final_output}
                ])
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
    
    def show_history(self):
        print("\n📜 Conversation History:")
        for i, (user, assistant) in enumerate(zip(
            self.conversation_history[::2], 
            self.conversation_history[1::2]
        )):
            print(f"{i+1}. You: {user['content']}")
            print(f"   Assistant: {assistant['content']}\n")
    
    def save_conversation(self):
        import json
        with open('conversation.json', 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
        print("💾 Conversation saved to conversation.json")
    
    def load_conversation(self):
        import json
        try:
            with open('conversation.json', 'r') as f:
                self.conversation_history = json.load(f)
            print("📂 Conversation loaded from conversation.json")
        except FileNotFoundError:
            print("❌ No saved conversation found")
```

### Multi-Agent REPL

```python
class MultiAgentREPL:
    def __init__(self):
        self.agents = {
            "general": Agent(name="General", instructions="Helpful assistant"),
            "tech": Agent(name="Tech", instructions="Technical expert"),
            "creative": Agent(name="Creative", instructions="Creative assistant")
        }
        self.current_agent = "general"
    
    async def start(self):
        print("🤖 Multi-Agent REPL")
        print("Commands: /switch <agent>, /list, /quit")
        
        while True:
            user_input = input(f"\nYou ({self.current_agent}): ").strip()
            
            if user_input.lower() == '/quit':
                break
            elif user_input.startswith('/switch '):
                agent_name = user_input.split(' ')[1]
                if agent_name in self.agents:
                    self.current_agent = agent_name
                    print(f"🔄 Switched to {agent_name} agent")
                else:
                    print(f"❌ Unknown agent: {agent_name}")
                continue
            elif user_input == '/list':
                print("Available agents:")
                for name, agent in self.agents.items():
                    print(f"- {name}: {agent.name}")
                continue
            
            # Process with current agent
            agent = self.agents[self.current_agent]
            result = await Runner.run(agent, user_input)
            print(f"🤖 {agent.name}: {result.final_output}")
```

## 💬 When to Use REPL Interfaces

### ✅ **Use REPL interfaces when:**
- Building interactive applications
- Creating conversational AI interfaces
- Need persistent conversation sessions
- Testing and debugging agents
- Building user-facing chat applications

### ❌ **Don't use REPL interfaces when:**
- Batch processing applications
- Server-side API endpoints
- Performance-critical systems
- Automated workflows

## ⚠️ Common Issues & Solutions

### Issue: "REPL not responding"
**Solution:** Check that the agent is properly configured and API key is valid

### Issue: "Conversation context lost"
**Solution:** Implement conversation history management

### Issue: "REPL crashes on input"
**Solution:** Add proper error handling and input validation

### Issue: "ModuleNotFoundError: No module named 'agents'"
**Solution:** Install the SDK: `pip install openai-agents`

## 🔗 Related Topics

- [Basic Streaming](../../11runningagents/3runasyncstreaming/)
- [Advanced Streaming](../streaming/)
- [Agent Loops](../../11runningagents/4agentloop/)
- [Conversation Management](../../11runningagents/6conversation/)
- [Function Tools](../../15tools/8functiontool/)

## 📚 Additional Resources

- [OpenAI Agents SDK Documentation](https://github.com/openai/openai-agents)
- [Python REPL Development](https://docs.python.org/3/library/code.html)
- [Interactive Python Applications](https://realpython.com/python-interview/)

## 🎉 Next Steps

Once you understand REPL interfaces, try:
1. Building custom REPL applications
2. Creating multi-agent conversation systems
3. Implementing conversation persistence
4. Building interactive debugging tools

---

**Happy Coding! 🚀**

*This tutorial is part of the OpenAI Agents SDK learning series.* 