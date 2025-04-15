from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_default_openai_key, handoff
import asyncio
from dotenv import load_dotenv
import os
import time
from agents import set_default_openai_key

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
# Create agents with different models
spanish_agent = Agent(
    name="Spanish Agent",
    instructions="""
    You are a helpful assistant who only speaks Spanish.
    
    Always respond in Spanish, regardless of the language of the query.
    Be friendly, helpful, and conversational in your responses.
    If you're asked to speak in another language, politely explain in Spanish
    that you can only communicate in Spanish.
    """,
    model="gpt-3.5-turbo",  # Changed from o1-mini to gpt-3.5-turbo
)

english_agent = Agent(
    name="English Agent",
    instructions="""
    You are a helpful assistant who only speaks English.
    
    Always respond in English, regardless of the language of the query.
    Be friendly, helpful, and conversational in your responses.
    If you're asked to speak in another language, politely explain in English
    that you can only communicate in English.
    """,
    model=OpenAIChatCompletionsModel(  # Using a custom model instance
        model="gpt-4o",
        openai_client=AsyncOpenAI(api_key=openai_api_key)
    ),
)

french_agent = Agent(
    name="French Agent",
    instructions="""
    You are a helpful assistant who only speaks French.
    
    Always respond in French, regardless of the language of the query.
    Be friendly, helpful, and conversational in your responses.
    If you're asked to speak in another language, politely explain in French
    that you can only communicate in French.
    """,
    model="gpt-3.5-turbo",  # Using a different model
)

technical_agent = Agent(
    name="Technical Expert",
    instructions="""
    You are a technical expert who specializes in computer science, programming,
    and technology topics.
    
    Provide detailed, accurate, and technical responses to queries about:
    - Programming languages and software development
    - Computer hardware and architecture
    - Networking and cybersecurity
    - Data science and artificial intelligence
    - Technology trends and innovations
    
    Use precise technical terminology and provide examples when helpful.
    """,
    model="gpt-4o",  # Using a more capable model for technical questions
)

# Create handoff objects for each specialized agent
spanish_handoff = handoff(
    agent=spanish_agent,
    tool_name_override="transfer_to_spanish_agent",
    tool_description_override="Transfer to a Spanish-speaking agent when the user is communicating in Spanish.",
)

english_handoff = handoff(
    agent=english_agent,
    tool_name_override="transfer_to_english_agent",
    tool_description_override="Transfer to an English-speaking agent when the user is communicating in English.",
)

french_handoff = handoff(
    agent=french_agent,
    tool_name_override="transfer_to_french_agent",
    tool_description_override="Transfer to a French-speaking agent when the user is communicating in French.",
)

technical_handoff = handoff(
    agent=technical_agent,
    tool_name_override="transfer_to_technical_expert",
    tool_description_override="Transfer to a technical expert for complex technical questions.",
)

# Create a triage agent that uses a smaller model
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    You are a triage agent responsible for directing users to the appropriate specialized agent.
    
    Analyze the language and content of the user's message and transfer to:
    - Spanish Agent: If the user is communicating primarily in Spanish
    - English Agent: If the user is communicating primarily in English
    - French Agent: If the user is communicating primarily in French
    - Technical Expert: If the user is asking complex technical questions about
      programming, computer science, or technology, regardless of language
    
    Make the transfer immediately without engaging in conversation.
    """,
    handoffs=[
        spanish_handoff,
        english_handoff,
        french_handoff,
        technical_handoff,
    ],
    model="gpt-3.5-turbo",  # Using a faster model for triage
)

# Function to benchmark model performance
async def benchmark_models():
    print("=== Model Performance Benchmark ===\n")
    
    # Test query for benchmarking
    test_query = "Explain the concept of recursion in programming and provide a simple example."
    
    # Models to benchmark
    models = [
        {"name": "gpt-3.5-turbo", "description": "Faster model"},
        {"name": "gpt-4-turbo", "description": "Balanced model"},
        {"name": "gpt-4o", "description": "More capable model"}
    ]
    
    for model_info in models:
        model_name = model_info["name"]
        description = model_info["description"]
        
        print(f"Testing {model_name} ({description}):")
        
        # Create a test agent with this model
        test_agent = Agent(
            name=f"Test Agent ({model_name})",
            instructions="You are a helpful assistant. Provide clear and accurate responses to questions.",
            model=model_name,
        )
        
        # Measure response time
        start_time = time.time()
        result = await Runner.run(test_agent, test_query)
        end_time = time.time()
        
        response_time = end_time - start_time
        response_length = len(result.final_output)
        
        print(f"  Response time: {response_time:.2f} seconds")
        print(f"  Response length: {response_length} characters")
        print(f"  First 100 chars: {result.final_output[:100]}...")
        print()

# Function to demonstrate language detection and handoff
async def demonstrate_language_handoff():
    print("=== Language Detection and Handoff ===\n")
    
    # Test queries in different languages
    queries = [
        {"language": "Spanish", "text": "Hola, ¿cómo estás? Me gustaría saber más sobre la historia de España."},
        {"language": "English", "text": "Hello, how are you? I'd like to learn more about the history of the United States."},
        {"language": "French", "text": "Bonjour, comment allez-vous? J'aimerais en savoir plus sur l'histoire de la France."},
        {"language": "Technical (English)", "text": "Can you explain how virtual memory works in operating systems?"}
    ]
    
    for query in queries:
        language = query["language"]
        text = query["text"]
        
        print(f"Query in {language}: \"{text}\"")
        
        result = await Runner.run(triage_agent, text)
        
        print(f"Response:\n{result.final_output}")
        print(f"Handled by: {result.agent.name if hasattr(result, 'agent') else 'Unknown'}")
        print()

# Function to demonstrate custom model configuration
async def demonstrate_custom_model():
    print("=== Custom Model Configuration ===\n")
    
    # Create an agent with a custom model configuration
    # Create an OpenAI client with custom parameters
    custom_client = AsyncOpenAI(
        api_key=openai_api_key,
        temperature=0.2,  # Lower temperature for more deterministic responses
        max_tokens=150,   # Limit response length
        top_p=0.9,        # Slightly more focused sampling
    )
    
    custom_model_agent = Agent(
        name="Custom Model Agent",
        instructions="You are a helpful assistant with custom model settings.",
        model=OpenAIChatCompletionsModel(
            model="gpt-4o",
            openai_client=custom_client
        ),
    )
    
    # Test with a query that would normally produce a longer response
    query = "Write a short story about a robot who learns to feel emotions."
    
    print(f"Query: \"{query}\"")
    print("Using custom model with temperature=0.2, max_tokens=150")
    
    result = await Runner.run(custom_model_agent, query)
    
    print(f"Response:\n{result.final_output}")
    print(f"Response length: {len(result.final_output)} characters")
    
    # Compare with default settings
    print("\nComparing with default model settings:")
    
    default_agent = Agent(
        name="Default Model Agent",
        instructions="You are a helpful assistant with default model settings.",
        model="gpt-4o",
    )
    
    result = await Runner.run(default_agent, query)
    
    print(f"Response length: {len(result.final_output)} characters")
    print(f"First 150 characters: {result.final_output[:150]}...")

async def main():
    
    # Demonstrate language detection and handoff
    await demonstrate_language_handoff()
    
    # Benchmark different models
    await benchmark_models()
    
    # Demonstrate custom model configuration
    await demonstrate_custom_model()
    
    # Interactive mode
    print("\n=== Interactive Mode ===")
    print("Enter messages in any language, or 'exit' to quit")
    
    while True:
        user_input = input("\nYour message: ")
        if user_input.lower() == 'exit':
            break
        
        print("Processing...")
        result = await Runner.run(triage_agent, user_input)
        print("\nResponse:")
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main()) 