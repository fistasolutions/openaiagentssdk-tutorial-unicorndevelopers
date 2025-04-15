# 🔍 Run Item And Agents Events Example

## What This Code Does (Big Picture)
Imagine being able to see exactly what your robot friend is thinking and doing behind the scenes! This code shows how to track all the steps an AI takes when answering your questions, including when it calls tools, what it's thinking, and how it forms its response.

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
import asyncio
import random
from agents import Agent, ItemHelpers, Runner, function_tool, set_default_openai_key
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
```
The AI assistant needs a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Creating Tools for the Joke Agent 🛠️
```python
# Define a tool that returns a random number of jokes to tell
@function_tool
def how_many_jokes() -> int:
    """Randomly decide how many jokes to tell (between 1 and 5)"""
    return random.randint(1, 5)

# Define a tool that provides a random joke topic
@function_tool
def get_joke_topic() -> str:
    """Get a random topic for a joke"""
    topics = [
        "programming", "animals", "food", "weather", 
        "office life", "sports", "movies", "technology"
    ]
    return random.choice(topics)
```
These tools help the joke agent:
- Decide how many jokes to tell (between 1 and 5)
- Pick random topics for jokes from a predefined list

## Step 3: Creating a Joke-Telling Agent 🤖
```python
# Create an agent that will use the tools to determine how many jokes to tell
agent = Agent(
    name="Joker",
    instructions="""
    You are a joke-telling assistant. When greeting the user:
    1. First call the `how_many_jokes` tool to determine how many jokes to tell
    2. For each joke, call the `get_joke_topic` tool to get a topic
    3. Tell a joke about that topic
    4. Continue until you've told the requested number of jokes
    
    Keep your jokes clean and family-friendly.
    """,
    tools=[how_many_jokes, get_joke_topic],
)
```
This creates an AI assistant that tells jokes on random topics, using the tools to determine how many jokes to tell and what topics to use.

## Step 4: Running the Agent with Event Tracking 🔍
```python
# Run the agent with streaming enabled
result = Runner.run_streamed(
    agent,
    input="Tell me some jokes please!",
)

print("=== Run starting ===")
print("Tracking events in real-time:\n")

# Track some statistics
tool_call_count = 0
joke_count = 0

# Process the stream events
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
            tool_call_count += 1
            # Based on the output, we can see the structure includes raw_item with name
            if hasattr(event.item, 'raw_item') and hasattr(event.item.raw_item, 'name'):
                print(f"-- Tool was called: {event.item.raw_item.name}")
                print(f"   Arguments: {event.item.raw_item.arguments}")
            else:
                print(f"-- Tool was called (unknown tool)")
            
        elif event.item.type == "tool_call_output_item":
            print(f"-- Tool output: {event.item.output}")
            # Fix the attribute error by checking the structure
            if hasattr(event.item, 'raw_item') and hasattr(event.item.raw_item, 'tool_call_id'):
                tool_call_id = event.item.raw_item.tool_call_id
                if "how_many_jokes" in str(tool_call_id):
                    joke_count = int(event.item.output)
                    print(f"   [Agent will tell {joke_count} jokes]")
            
        elif event.item.type == "message_output_item":
            message_text = ItemHelpers.text_message_output(event.item)
            # Only print the first 100 characters of the message to keep the output clean
            preview = message_text[:100] + ("..." if len(message_text) > 100 else "")
            print(f"-- Message output: {preview}")
            
        else:
            print(f"-- Other item type: {event.item.type}")

# Print final statistics
print("\n=== Run complete ===")
print(f"Total tool calls: {tool_call_count}")
print(f"Jokes requested: {joke_count}")
```
This code:
1. Runs the agent in streaming mode
2. Tracks different types of events in real-time
3. Counts tool calls and tracks how many jokes will be told
4. Shows what the agent is doing at each step
5. Displays a preview of the message output
6. Prints final statistics about the run

## Step 5: Creating a Multi-Agent Joke System 🤖🤖🤖
```python
# Create a joke evaluator agent
evaluator_agent = Agent(
    name="Joke Evaluator",
    instructions="""
    You evaluate jokes on a scale of 1-10 based on:
    - Originality
    - Humor
    - Cleverness
    
    Provide a brief explanation for your rating.
    """,
)

# Create a joke improver agent
improver_agent = Agent(
    name="Joke Improver",
    instructions="""
    You take jokes and improve them by:
    - Adding a better punchline
    - Improving the setup
    - Making them more concise
    
    Explain what you changed and why.
    """,
)
```
This creates a system with three specialized agents:
1. The original joke-telling agent
2. An evaluator agent that rates jokes on originality, humor, and cleverness
3. An improver agent that enhances jokes based on evaluation feedback

## Step 6: Running the Multi-Agent Pipeline 🔄
```python
# Run a sequence of agents
print("Generating a joke...")
joke_result = Runner.run_streamed(
    agent,
    input="Tell me just one joke about computers",
)

# Track the joke for the next steps
joke_text = ""

print("Tracking joke generation:")
async for event in joke_result.stream_events():
    if event.type == "run_item_stream_event" and event.item.type == "message_output_item":
        joke_text = ItemHelpers.text_message_output(event.item)
        print("-- Joke generated")

# Now evaluate the joke
print("\nEvaluating the joke...")
eval_result = Runner.run_streamed(
    evaluator_agent,
    input=f"Please evaluate this joke: {joke_text}",
)

evaluation = ""
async for event in eval_result.stream_events():
    if event.type == "run_item_stream_event" and event.item.type == "message_output_item":
        evaluation = ItemHelpers.text_message_output(event.item)
        print("-- Evaluation complete")

# Now improve the joke
print("\nImproving the joke...")
improve_result = Runner.run_streamed(
    improver_agent,
    input=f"Please improve this joke: {joke_text}\nThe evaluation was: {evaluation}",
)

improved_joke = ""
async for event in improve_result.stream_events():
    if event.type == "run_item_stream_event" and event.item.type == "message_output_item":
        improved_joke = ItemHelpers.text_message_output(event.item)
        print("-- Improvement complete")

# Print the final results
print("\n=== Multi-Agent Process Results ===")
print("\nOriginal Joke:")
print(joke_text)
print("\nEvaluation:")
print(evaluation)
print("\nImproved Joke:")
print(improved_joke)
```
This creates a pipeline where:
1. The joke agent creates a joke about computers
2. The evaluator agent reviews the joke based on specific criteria
3. The improver agent enhances the joke based on the evaluation
4. The final results show the original joke, evaluation, and improved version

## Final Summary 📌
✅ We created tools for generating random joke parameters
✅ We created a joke-telling agent that uses these tools
✅ We tracked all the events and steps the agent takes
✅ We counted tool calls and monitored joke generation
✅ We created a multi-agent system for joke creation, evaluation, and improvement
✅ We built a complete pipeline that shows the entire joke improvement process

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
   uv run runitemandagentsevents.py
   ```
4. Watch the detailed event stream as the agents work and see the joke improvement process!

## What You'll Learn 🧠
- How to track and process different types of agent events
- How to build multi-agent systems that work together
- How to monitor tool usage and count events
- How to extract and use information from event streams
- How to create a pipeline of agents that pass information to each other
- How to use ItemHelpers to extract text from message outputs

Happy coding! 🎉 