# 🔧 Hosted Tools Example

## What This Code Does (Big Picture)
Imagine giving your robot friend superpowers to search the internet and look through documents! This code shows how to use OpenAI's built-in tools that let your AI assistant search the web for current information and find relevant content in your documents.

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
from agents import Agent, FileSearchTool, Runner, WebSearchTool, set_default_openai_key
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
# You would need to set this in your .env file
vector_store_id = os.environ.get("VECTOR_STORE_ID", "your_vector_store_id_here")
```
The AI assistant needs a magic key (API key) to work properly, plus a special ID for where your documents are stored.

This code finds these keys hidden in a secret file (.env) and unlocks them.

## Step 2: Setting the Default API Key 🔑
```python
async def main():
    set_default_openai_key(openai_api_key)
```
This sets the OpenAI API key as the default for all agents in our program.

## Step 3: Creating a Research Assistant with Hosted Tools 🤖
```python
# Create an agent with hosted tools
research_agent = Agent(
    name="Research Assistant",
    instructions="""
    You are a helpful research assistant that can search the web and retrieve information 
    from documents to provide comprehensive answers.
    
    When answering questions:
    1. Use the WebSearchTool to find current information from the internet
    2. Use the FileSearchTool to find relevant information from stored documents
    3. Combine information from both sources to provide a complete answer
    4. Always cite your sources
    5. If the information is not available or unclear, be honest about limitations
    
    Be concise but thorough in your responses.
    """,
    tools=[
        WebSearchTool(),
        FileSearchTool(
            max_num_results=3,
            vector_store_ids=[vector_store_id],
        ),
    ],
)
```
This creates an AI assistant that:
- Can search the web for current information
- Can search through your documents for relevant content
- Combines information from both sources
- Cites its sources properly
- Is instructed to be concise but thorough

## Step 4: Preparing Example Queries 📝
```python
# Example queries that would benefit from web search and file search
queries = [
    "Which coffee shop should I go to, taking into account my preferences and the weather today in SF?",
    "What are the key differences between Python and JavaScript?",
    "Summarize the main points from our company's Q2 financial report."
]
```
These are sample questions that demonstrate the power of combining web search and document search:
1. A question that needs current information (weather) and personal preferences
2. A general knowledge question that could be answered from the web
3. A company-specific question that would require searching through internal documents

## Step 5: Running the Research Assistant 🏃‍♂️
```python
# Run the first query as an example
print("\n=== Research Query Example ===")
print(f"Query: {queries[0]}")

try:
    result = await Runner.run(research_agent, queries[0])
    print("\nResponse:")
    print(result.final_output)
except Exception as e:
    print(f"\nError: {e}")
    print("\nNote: To use WebSearchTool and FileSearchTool, you need:")
    print("1. Proper API keys configured")
    print("2. A valid vector store ID for FileSearchTool")
    print("3. Access to the OpenAI hosted tools")
```
This runs the research assistant with the first sample question and:
1. Displays the query being processed
2. Shows the AI's response if successful
3. Provides helpful error information if the tools aren't properly configured

## Step 6: Creating an Interactive Research Mode 💬
```python
# Interactive mode
print("\n=== Interactive Research Mode ===")
print("Type 'exit' to quit")
print("Note: This requires proper configuration of API keys and vector store IDs")

while True:
    user_input = input("\nYour research question: ")
    if user_input.lower() == 'exit':
        break
    
    try:
        print("Researching... (this may take a moment)")
        result = await Runner.run(research_agent, user_input)
        print("\nResearch results:")
        print(result.final_output)
    except Exception as e:
        print(f"\nError: {e}")
```
This creates an interactive mode where:
- You can ask your own research questions
- The AI searches the web and your documents
- It shows a "Researching..." message while working
- It combines information to give you comprehensive answers
- It handles errors gracefully
- You can type "exit" to quit

## Final Summary 📌
✅ We created a research assistant with web search capabilities
✅ We gave it access to search through our documents
✅ We instructed it to combine information from multiple sources
✅ We provided example queries that demonstrate its capabilities
✅ We created an interactive research mode for asking questions
✅ We added error handling for when the tools aren't properly configured

## Try It Yourself! 🚀
1. Install the required packages:
   ```
   uv add openai-agents python-dotenv
   ```
2. Create a `.env` file with your OpenAI API key and vector store ID:
   ```
   OPENAI_API_KEY=your_api_key_here
   VECTOR_STORE_ID=your_vector_store_id_here
   ```
3. Run the program:
   ```
   uv run hostedtools.py
   ```
4. Ask research questions that require current and stored information!

## What You'll Learn 🧠
- How to use OpenAI's hosted tools for web search and document search
- How to combine information from multiple sources
- How to create a research assistant with advanced capabilities
- How to work with vector stores for document search
- How to handle errors when working with external services

Happy coding! 🎉 