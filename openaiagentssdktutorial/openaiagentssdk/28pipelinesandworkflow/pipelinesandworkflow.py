import asyncio
import numpy as np
import sounddevice as sd
import time
from typing import List, Optional

from agents import Agent, function_tool, set_default_openai_key
from agents.voice import (
    AudioInput,
    StreamedAudioInput,
    SingleAgentVoiceWorkflow,
    VoicePipeline,
    VoicePipelineConfig
)
from dotenv import load_dotenv
import os

# Load environment variables and set up API key
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)

# Define some tools for our agent
@function_tool
def search_knowledge_base(query: str) -> str:
    """Search the knowledge base for information."""
    print(f"[debug] Searching knowledge base for: {query}")
    # Simulate a knowledge base search
    time.sleep(0.5)  # Simulate processing time
    
    knowledge = {
        "company policy": "Our company policy emphasizes work-life balance and flexible working hours.",
        "product features": "Our flagship product includes AI-powered analytics, real-time reporting, and cloud integration.",
        "pricing": "Our pricing starts at $19/month for basic features, with premium plans at $49/month.",
        "support": "Technical support is available 24/7 via chat, email, or phone."
    }
    
    for key, value in knowledge.items():
        if key in query.lower():
            return value
    
    return "I couldn't find specific information about that query in our knowledge base."

@function_tool
def get_customer_info(customer_id: str) -> str:
    """Get information about a customer by their ID."""
    print(f"[debug] Getting info for customer: {customer_id}")
    # Simulate a customer database lookup
    time.sleep(0.5)  # Simulate processing time
    
    customers = {
        "12345": "Customer since 2020, Premium plan, Last contact: 2 weeks ago",
        "67890": "Customer since 2021, Basic plan, Last contact: 1 month ago",
        "24680": "Customer since 2019, Enterprise plan, Last contact: 3 days ago",
        "13579": "Customer since 2022, Trial plan, Last contact: Yesterday"
    }
    
    return customers.get(customer_id, "Customer not found in our database.")

# Create our agent
support_agent = Agent(
    name="Customer Support",
    instructions="""You are a helpful customer support agent. 
    Use the knowledge base tool to answer questions about company policies, products, and services.
    Use the customer info tool when asked about specific customers.
    Be concise and professional in your responses.""",
    model="gpt-4o",
    tools=[search_knowledge_base, get_customer_info]
)

async def demonstrate_audio_input():
    """Demonstrate using AudioInput with a voice pipeline."""
    print("\n=== Demonstrating AudioInput (Complete Audio) ===")
    
    # Create a voice pipeline with custom configuration
    pipeline_config = VoicePipelineConfig(
        workflow_name="customer_support",
        disable_tracing=True,  # Disable tracing for this example
    )
    
    pipeline = VoicePipeline(
        workflow=SingleAgentVoiceWorkflow(support_agent),
        config=pipeline_config
    )
    
    # Create a simulated audio input (in a real app, this would be actual audio)
    print("Simulating user asking: 'What are your product features?'")
    buffer = np.zeros(24000 * 3, dtype=np.int16)  # 3 seconds of silence
    audio_input = AudioInput(
        buffer=buffer,
        # For simulation, we'll provide the transcription directly
        transcription="What are your product features?"
    )
    
    # Run the pipeline
    print("Processing complete audio input...")
    result = await pipeline.run(audio_input)
    
    # Process the result
    print("Agent is responding. Streaming audio...")
    audio_chunks = 0
    async for event in result.stream():
        if event.type == "voice_stream_event_audio":
            audio_chunks += 1
            # In a real app: player.write(event.data)
    
    print(f"Audio response complete (would have played {audio_chunks} audio chunks)")
    print(f"Text of response: {result.text}")

async def demonstrate_streamed_audio_input():
    """Demonstrate using StreamedAudioInput with a voice pipeline."""
    print("\n=== Demonstrating StreamedAudioInput (Streaming Audio) ===")
    
    # Create a voice pipeline
    pipeline = VoicePipeline(
        workflow=SingleAgentVoiceWorkflow(support_agent)
    )
    
    # Create a streamed audio input
    print("Simulating streaming audio from user...")
    streamed_input = StreamedAudioInput()
    
    # Start the pipeline with the streamed input
    result_future = asyncio.create_task(pipeline.run(streamed_input))
    
    # Simulate sending audio chunks with transcriptions
    # In a real app, you'd push actual audio chunks and let the pipeline handle transcription
    
    # First chunk
    print("User starts speaking: 'Can you tell me about'")
    chunk1 = np.zeros(24000 * 1, dtype=np.int16)  # 1 second of silence
    await streamed_input.push_chunk(chunk1, transcription="Can you tell me about")
    await asyncio.sleep(0.5)  # Simulate time between chunks
    
    # Second chunk
    print("User continues: 'your company policy?'")
    chunk2 = np.zeros(24000 * 1, dtype=np.int16)  # 1 second of silence
    await streamed_input.push_chunk(chunk2, transcription="your company policy?")
    await asyncio.sleep(0.5)  # Simulate time between chunks
    
    # Signal that the user is done speaking
    print("User stops speaking. Detecting end of speech...")
    await streamed_input.end()
    
    # Get the result
    result = await result_future
    
    # Process the result
    print("Agent is responding. Streaming audio...")
    audio_chunks = 0
    lifecycle_events = 0
    
    async for event in result.stream():
        if event.type == "voice_stream_event_audio":
            audio_chunks += 1
            # In a real app: player.write(event.data)
        elif event.type == "voice_stream_event_lifecycle":
            lifecycle_events += 1
            print(f"Lifecycle event: {event.data}")
    
    print(f"Audio response complete (would have played {audio_chunks} audio chunks)")
    print(f"Detected {lifecycle_events} lifecycle events")
    print(f"Text of response: {result.text}")

async def demonstrate_handling_interruptions():
    """Demonstrate how to handle interruptions in a voice conversation."""
    print("\n=== Demonstrating Handling Interruptions ===")
    
    # Create a voice pipeline
    pipeline = VoicePipeline(
        workflow=SingleAgentVoiceWorkflow(support_agent)
    )
    
    # Create a streamed audio input
    print("Simulating a conversation with interruption...")
    streamed_input = StreamedAudioInput()
    
    # Start the pipeline with the streamed input
    result_future = asyncio.create_task(pipeline.run(streamed_input))
    
    # First turn - user asks a question
    print("User: 'Tell me about your pricing plans in detail'")
    chunk1 = np.zeros(24000 * 1, dtype=np.int16)
    await streamed_input.push_chunk(chunk1, transcription="Tell me about your pricing plans in detail")
    await streamed_input.end()  # End of first turn
    
    # Get the result and start processing it
    result = await result_future
    
    # Start a task to process the result stream
    async def process_stream():
        playing_audio = False
        async for event in result.stream():
            if event.type == "voice_stream_event_lifecycle":
                if event.data == "turn_started":
                    print("Agent started speaking...")
                    playing_audio = True
                elif event.data == "turn_ended":
                    print("Agent finished speaking")
                    playing_audio = False
            elif event.type == "voice_stream_event_audio" and playing_audio:
                # Simulate playing audio
                await asyncio.sleep(0.05)  # Simulate time to play audio chunk
                
                # Simulate user interruption while agent is speaking
                if playing_audio and not hasattr(process_stream, "interrupted"):
                    process_stream.interrupted = True
                    print("\n[User interrupts!] 'Actually, just tell me about the basic plan'")
                    
                    # Start a new turn with the interruption
                    new_input = StreamedAudioInput()
                    new_result_future = asyncio.create_task(pipeline.run(new_input))
                    
                    # Push the interruption
                    await new_input.push_chunk(
                        np.zeros(24000 * 1, dtype=np.int16),
                        transcription="Actually, just tell me about the basic plan"
                    )
                    await new_input.end()
                    
                    # Process the new result
                    new_result = await new_result_future
                    print("\nAgent responds to interruption:")
                    print(f"Text: {new_result.text}")
                    return
    
    # Run the stream processing
    await process_stream()

async def main():
    print("🔄 Pipelines and Workflows Demonstration 🔄")
    print("===========================================")
    print("This example shows different ways to use voice pipelines and workflows.")
    
    # Demonstrate different types of audio inputs
    await demonstrate_audio_input()
    await demonstrate_streamed_audio_input()
    await demonstrate_handling_interruptions()
    
    print("\n===========================================")
    print("Pipelines and Workflows Demonstration Complete!")

if __name__ == "__main__":
    asyncio.run(main()) 