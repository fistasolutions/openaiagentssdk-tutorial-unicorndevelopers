from agents import Agent, ModelSettings, function_tool, trace
from dotenv import load_dotenv
import asyncio
import os
import uuid
from agents import Runner, set_default_openai_key
load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)

async def main():
    
    # Create a simple agent with concise instructions
    agent = Agent(
        name="Assistant",
        instructions="Reply very concisely. Provide accurate but brief answers."
    )
    
    # Generate a unique thread ID for this conversation
    thread_id = str(uuid.uuid4())
    
    # Start a traced conversation
    with trace(workflow_name="Conversation", group_id=thread_id):
        print("\n--- First Turn ---")
        # First turn
        result = await Runner.run(agent, "What city is the Golden Gate Bridge in?")
        print("User: What city is the Golden Gate Bridge in?")
        print(f"Assistant: {result.final_output}")
        
        print("\n--- Second Turn ---")
        # Second turn - using the conversation history
        new_input = result.to_input_list() + [{"role": "user", "content": "What state is it in?"}]
        result = await Runner.run(agent, new_input)
        print("User: What state is it in?")
        print(f"Assistant: {result.final_output}")
        
        print("\n--- Third Turn ---")
        # Third turn - continuing the conversation
        new_input = result.to_input_list() + [{"role": "user", "content": "When was it built?"}]
        result = await Runner.run(agent, new_input)
        print("User: When was it built?")
        print(f"Assistant: {result.final_output}")
    
    # Start a new conversation with the same agent but a different thread ID
    new_thread_id = str(uuid.uuid4())
    
    with trace(workflow_name="New Conversation", group_id=new_thread_id):
        print("\n--- New Conversation ---")
        # First turn of new conversation
        result = await Runner.run(agent, "Tell me about the Eiffel Tower")
        print("User: Tell me about the Eiffel Tower")
        print(f"Assistant: {result.final_output}")
        
        # Second turn of new conversation
        new_input = result.to_input_list() + [{"role": "user", "content": "How tall is it?"}]
        result = await Runner.run(agent, new_input)
        print("User: How tall is it?")
        print(f"Assistant: {result.final_output}")
    
    # Interactive mode with conversation history
    print("\n--- Interactive Mode ---")
    print("Type 'exit' to quit or 'new' to start a new conversation")
    
    interactive_thread_id = str(uuid.uuid4())
    conversation_history = None
    
    with trace(workflow_name="Interactive Conversation", group_id=interactive_thread_id):
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() == 'exit':
                break
            elif user_input.lower() == 'new':
                print("Starting a new conversation")
                conversation_history = None
                interactive_thread_id = str(uuid.uuid4())
                continue
            
            if conversation_history is None:
                # First message in conversation
                result = await Runner.run(agent, user_input)
            else:
                # Continuing conversation
                new_input = conversation_history.to_input_list() + [{"role": "user", "content": user_input}]
                result = await Runner.run(agent, new_input)
            
            print(f"Assistant: {result.final_output}")
            conversation_history = result

if __name__ == "__main__":
    asyncio.run(main()) 