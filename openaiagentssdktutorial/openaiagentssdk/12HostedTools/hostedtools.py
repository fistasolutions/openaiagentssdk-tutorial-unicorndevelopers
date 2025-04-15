from agents import Agent, FileSearchTool, Runner, WebSearchTool, set_default_openai_key
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
# You would need to set this in your .env file
vector_store_id = os.environ.get("VECTOR_STORE_ID", "your_vector_store_id_here")

async def main():
    set_default_openai_key(openai_api_key)
    
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
    
    # Example queries that would benefit from web search and file search
    queries = [
        "Which coffee shop should I go to, taking into account my preferences and the weather today in SF?",
        "What are the key differences between Python and JavaScript?",
        "Summarize the main points from our company's Q2 financial report."
    ]
    
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

if __name__ == "__main__":
    asyncio.run(main()) 