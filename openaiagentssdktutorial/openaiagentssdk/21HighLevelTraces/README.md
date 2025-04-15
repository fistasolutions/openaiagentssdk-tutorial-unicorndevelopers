# 🔍 High Level Traces Example

## What This Code Does (Big Picture)
Imagine being able to see the entire journey of your AI's thought process like a storyboard! This code shows how to use traces to organize and visualize multi-step AI workflows, making it easier to understand complex processes like a joke creation workshop with multiple specialized agents.

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
from agents import Agent, Runner, trace, set_default_openai_key
import asyncio
from dotenv import load_dotenv
import os
import time
import random

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
```
The AI assistants need a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Creating Specialized Agents for a Joke Workshop 🤖
```python
# Create specialized agents for different tasks
joke_agent = Agent(
    name="Joke Generator",
    instructions="""
    You are a creative joke generator. Your job is to create original, funny jokes based on the topic provided.
    
    Guidelines for your jokes:
    - Keep jokes appropriate for all audiences
    - Avoid offensive or controversial content
    - Use wordplay, puns, and clever twists
    - Be concise and to the point
    - Create jokes that are easy to understand
    
    When asked for a joke, provide just the joke itself without additional commentary.
    """,
)

rating_agent = Agent(
    name="Joke Evaluator",
    instructions="""
    You are a professional joke evaluator. Your job is to rate jokes on a scale of 1-10 and provide brief feedback.
    
    When rating jokes, consider:
    - Originality and creativity
    - Cleverness of wordplay or punchline
    - Overall humor value
    - Appropriateness for general audiences
    - Clarity and delivery
    
    Provide your rating in this format:
    Rating: [1-10]
    Feedback: [Brief explanation of your rating]
    """,
)

improvement_agent = Agent(
    name="Joke Improver",
    instructions="""
    You are a joke improvement specialist. Your job is to take an existing joke and make it funnier.
    
    Ways to improve jokes:
    - Tighten the wording for better delivery
    - Enhance the punchline for more impact
    - Add a clever twist or unexpected element
    - Improve the setup to better lead to the punchline
    - Fix any issues with timing or structure
    
    Provide both the improved joke and a brief explanation of what you changed and why.
    """,
)
```
This creates three specialized agents:
- A joke generator that creates original jokes on a given topic
- A joke evaluator that rates jokes on a scale of 1-10
- A joke improver that enhances jokes to make them funnier

## Step 3: Creating a Joke Workshop Process with Traces 🔄
```python
# Function to simulate a joke workshop process
async def joke_workshop(topic):
    print(f"\n=== Starting Joke Workshop on '{topic}' ===\n")
    
    # Use a trace to group all the steps in the joke workshop process
    with trace(f"Joke Workshop: {topic}"):
        # Step 1: Generate initial jokes
        print("Step 1: Generating initial jokes...")
        jokes = []
        
        # Generate 3 different jokes on the topic
        for i in range(3):
            with trace(f"Generate Joke #{i+1}"):
                result = await Runner.run(joke_agent, f"Create a funny joke about {topic}. Make it original and clever.")
                jokes.append(result.final_output)
                print(f"Joke #{i+1}: {result.final_output}")
                # Add a small delay to simulate processing time
                time.sleep(0.5)
        
        # Step 2: Rate each joke
        print("\nStep 2: Rating jokes...")
        ratings = []
        
        for i, joke in enumerate(jokes):
            with trace(f"Rate Joke #{i+1}"):
                result = await Runner.run(rating_agent, f"Please rate this joke about {topic}: \"{joke}\"")
                ratings.append(result.final_output)
                print(f"Rating for Joke #{i+1}: {result.final_output}")
                time.sleep(0.5)
        
        # Step 3: Improve the best joke
        print("\nStep 3: Improving the best joke...")
        
        # Find the joke with the highest rating (simple parsing)
        best_joke_index = 0
        highest_rating = 0
        
        for i, rating in enumerate(ratings):
            try:
                # Extract the numeric rating (assuming format "Rating: [1-10]")
                rating_value = int(rating.split("Rating:")[1].split("\n")[0].strip())
                if rating_value > highest_rating:
                    highest_rating = rating_value
                    best_joke_index = i
            except:
                # If parsing fails, just continue
                continue
        
        best_joke = jokes[best_joke_index]
        print(f"Best joke selected: {best_joke}")
        
        with trace("Improve Best Joke"):
            result = await Runner.run(
                improvement_agent, 
                f"Please improve this joke about {topic}: \"{best_joke}\". Make it funnier while keeping its essence."
            )
            improved_joke = result.final_output
            print(f"\nImproved joke: {improved_joke}")
        
        # Step 4: Final rating of the improved joke
        print("\nStep 4: Rating the improved joke...")
        
        with trace("Rate Improved Joke"):
            result = await Runner.run(rating_agent, f"Please rate this improved joke about {topic}: \"{improved_joke}\"")
            final_rating = result.final_output
            print(f"Final rating: {final_rating}")
        
        # Return the final results
        return {
            "topic": topic,
            "original_jokes": jokes,
            "ratings": ratings,
            "best_original_joke": best_joke,
            "improved_joke": improved_joke,
            "final_rating": final_rating
        }
```
This function creates a complete joke workshop process:
1. It generates 3 different jokes on a topic
2. It rates each joke on a scale of 1-10
3. It identifies the best joke based on ratings
4. It improves the best joke to make it funnier
5. It provides a final rating for the improved joke

The key innovation is using `with trace()` to organize the process into logical sections that can be visualized and analyzed.

## Step 4: Creating a Simple Trace Demo 🔍
```python
# Function to demonstrate a simple trace
async def simple_trace_demo():
    print("=== Simple Trace Demo ===\n")
    
    with trace("Simple Joke Workflow"):
        print("Generating a joke...")
        first_result = await Runner.run(joke_agent, "Tell me a joke about programming")
        
        print("Rating the joke...")
        second_result = await Runner.run(rating_agent, f"Rate this joke: {first_result.final_output}")
        
        print(f"\nJoke: {first_result.final_output}")
        print(f"Rating: {second_result.final_output}")
```
This function demonstrates a simple trace with just two steps:
1. Generating a joke about programming
2. Rating that joke

It shows the basic usage of the `trace()` function to group related operations.

## Step 5: Creating a Nested Trace Demo 🔄
```python
# Function to demonstrate nested traces
async def nested_trace_demo():
    print("\n=== Nested Trace Demo ===\n")
    
    with trace("Customer Interaction"):
        print("Starting customer interaction...")
        
        with trace("Initial Greeting"):
            print("Greeting the customer...")
            time.sleep(0.5)
            print("Customer greeted successfully")
        
        with trace("Joke Request"):
            print("Customer requested a joke...")
            
            with trace("Joke Generation"):
                result = await Runner.run(joke_agent, "Tell me a joke about customer service")
                joke = result.final_output
                print(f"Generated joke: {joke}")
            
            with trace("Joke Delivery"):
                print("Delivering joke to customer...")
                time.sleep(0.5)
                print("Joke delivered successfully")
        
        with trace("Customer Feedback"):
            print("Getting customer feedback...")
            time.sleep(0.5)
            feedback = random.choice(["loved it", "thought it was okay", "didn't laugh"])
            print(f"Customer {feedback}")
        
        print("Customer interaction completed")
```
This function demonstrates nested traces, showing how to create a hierarchical structure:
1. The main "Customer Interaction" trace contains several sub-traces
2. The "Joke Request" trace contains its own sub-traces
3. Each trace represents a logical step in the process

This hierarchical structure makes it easier to understand complex workflows with multiple levels of detail.

## Step 6: Running the Demos and Workshop 🏃‍♂️
```python
async def main():
    
    # Demonstrate a simple trace
    await simple_trace_demo()
    
    # Demonstrate nested traces
    await nested_trace_demo()
    
    # Run the full joke workshop with traces
    topics = ["cats", "technology", "cooking"]
    
    for topic in topics:
        await joke_workshop(topic)
    
    # Interactive mode
    print("\n=== Interactive Joke Workshop ===")
    print("Enter a topic for a joke workshop, or 'exit' to quit")
    
    while True:
        topic = input("\nJoke topic: ")
        if topic.lower() == 'exit':
            break
        
        await joke_workshop(topic)
```
This main function:
1. Runs the simple trace demo
2. Runs the nested trace demo
3. Runs the joke workshop for three different topics
4. Creates an interactive mode where you can enter your own topics

## Final Summary 📌
✅ We created specialized agents for joke generation, evaluation, and improvement
✅ We created a multi-step joke workshop process with traces
✅ We demonstrated simple traces for basic workflows
✅ We demonstrated nested traces for complex hierarchical workflows
✅ We created an interactive mode for custom joke topics
✅ We showed how traces can organize and visualize complex AI processes

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
   uv run highleveltraces.py
   ```
4. Try the interactive joke workshop with your own topics!

## What You'll Learn 🧠
- How to use traces to organize complex AI workflows
- How to create nested traces for hierarchical processes
- How to coordinate multiple specialized agents in a workflow
- How to build an interactive system with traces
- How to visualize and understand multi-step AI processes

Happy coding! 🎉 