import asyncio
import numpy as np
import os
import uuid
from datetime import datetime

from agents import Agent, function_tool, set_default_openai_key
from agents.voice import (
    AudioInput,
    SingleAgentVoiceWorkflow,
    VoicePipeline,
    VoicePipelineConfig
)
from agents.tracing import get_trace_url
from dotenv import load_dotenv

# Load environment variables and set up API key
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)

# Define a simple tool for our agent
@function_tool
def get_current_time() -> str:
    """Get the current time."""
    return f"The current time is {datetime.now().strftime('%H:%M:%S')}."

@function_tool
def calculate_tip(bill_amount: float, tip_percentage: float = 15.0) -> str:
    """Calculate tip amount based on bill total and percentage."""
    tip_amount = bill_amount * (tip_percentage / 100)
    total = bill_amount + tip_amount
    return f"For a ${bill_amount:.2f} bill with {tip_percentage}% tip, you should leave ${tip_amount:.2f} for a total of ${total:.2f}."

# Create our agent
assistant = Agent(
    name="Voice Assistant",
    instructions="""You are a helpful voice assistant. 
    Be concise in your responses since they will be spoken aloud.
    Use the get_current_time tool when asked about the time.
    Use the calculate_tip tool when asked about calculating tips.""",
    model="gpt-4o",
    tools=[get_current_time, calculate_tip]
)

async def demonstrate_basic_tracing():
    """Demonstrate basic tracing with default settings."""
    print("\n=== Demonstrating Basic Tracing (Default Settings) ===")
    
    # Create a voice pipeline with default tracing (enabled)
    pipeline = VoicePipeline(
        workflow=SingleAgentVoiceWorkflow(assistant)
    )
    
    # Create a simulated audio input
    print("Simulating user asking: 'What time is it?'")
    buffer = np.zeros(24000 * 2, dtype=np.int16)  # 2 seconds of silence
    audio_input = AudioInput(
        buffer=buffer,
        transcription="What time is it?"
    )
    
    # Run the pipeline
    print("Processing audio with tracing enabled...")
    result = await pipeline.run(audio_input)
    
    # Process the result
    print(f"Assistant response: {result.text}")
    
    # Get the trace URL
    trace_url = get_trace_url()
    if trace_url:
        print(f"Trace URL: {trace_url}")
    else:
        print("No trace URL available. Make sure tracing is properly configured.")

async def demonstrate_custom_tracing():
    """Demonstrate custom tracing configuration."""
    print("\n=== Demonstrating Custom Tracing Configuration ===")
    
    # Generate a unique group ID for this conversation
    group_id = str(uuid.uuid4())
    
    # Create a voice pipeline with custom tracing configuration
    pipeline_config = VoicePipelineConfig(
        workflow_name="tip_calculator",  # Name this workflow
        group_id=group_id,  # Set a group ID to link multiple interactions
        trace_include_sensitive_data=True,  # Include transcripts in traces
        trace_include_sensitive_audio_data=False,  # Don't include audio data
        trace_metadata={  # Add custom metadata
            "user_id": "demo_user_123",
            "session_type": "demonstration",
            "app_version": "1.0.0"
        }
    )
    
    pipeline = VoicePipeline(
        workflow=SingleAgentVoiceWorkflow(assistant),
        config=pipeline_config
    )
    
    # Create a simulated audio input
    print("Simulating user asking: 'Calculate a tip for a $45.75 bill with 18% tip.'")
    buffer = np.zeros(24000 * 3, dtype=np.int16)  # 3 seconds of silence
    audio_input = AudioInput(
        buffer=buffer,
        transcription="Calculate a tip for a $45.75 bill with 18% tip."
    )
    
    # Run the pipeline
    print("Processing audio with custom tracing...")
    result = await pipeline.run(audio_input)
    
    # Process the result
    print(f"Assistant response: {result.text}")
    
    # Get the trace URL
    trace_url = get_trace_url()
    if trace_url:
        print(f"Trace URL: {trace_url}")
        print(f"Group ID for this trace: {group_id}")
    else:
        print("No trace URL available. Make sure tracing is properly configured.")
    
    return group_id

async def demonstrate_disabled_tracing():
    """Demonstrate disabling tracing."""
    print("\n=== Demonstrating Disabled Tracing ===")
    
    # Create a voice pipeline with tracing disabled
    pipeline_config = VoicePipelineConfig(
        disable_tracing=True  # Disable tracing completely
    )
    
    pipeline = VoicePipeline(
        workflow=SingleAgentVoiceWorkflow(assistant),
        config=pipeline_config
    )
    
    # Create a simulated audio input
    print("Simulating user asking: 'What can you help me with?'")
    buffer = np.zeros(24000 * 2, dtype=np.int16)  # 2 seconds of silence
    audio_input = AudioInput(
        buffer=buffer,
        transcription="What can you help me with?"
    )
    
    # Run the pipeline
    print("Processing audio with tracing disabled...")
    result = await pipeline.run(audio_input)
    
    # Process the result
    print(f"Assistant response: {result.text}")
    
    # Try to get the trace URL (should be None)
    trace_url = get_trace_url()
    if trace_url:
        print(f"Trace URL: {trace_url}")
    else:
        print("No trace URL available (expected since tracing is disabled).")

async def demonstrate_conversation_tracing(group_id):
    """Demonstrate tracing a multi-turn conversation with the same group ID."""
    print("\n=== Demonstrating Conversation Tracing (Multiple Turns) ===")
    
    # Create a voice pipeline with the same group ID as before
    pipeline_config = VoicePipelineConfig(
        workflow_name="tip_calculator",
        group_id=group_id,  # Use the same group ID to link these interactions
        trace_metadata={
            "user_id": "demo_user_123",
            "session_type": "demonstration",
            "conversation_turn": "follow-up"
        }
    )
    
    pipeline = VoicePipeline(
        workflow=SingleAgentVoiceWorkflow(assistant),
        config=pipeline_config
    )
    
    # Create a simulated audio input for a follow-up question
    print("Simulating user follow-up: 'What if I want to leave a 20% tip instead?'")
    buffer = np.zeros(24000 * 3, dtype=np.int16)
    audio_input = AudioInput(
        buffer=buffer,
        transcription="What if I want to leave a 20% tip instead?"
    )
    
    # Run the pipeline
    print("Processing follow-up with linked tracing...")
    result = await pipeline.run(audio_input)
    
    # Process the result
    print(f"Assistant response: {result.text}")
    
    # Get the trace URL
    trace_url = get_trace_url()
    if trace_url:
        print(f"Trace URL: {trace_url}")
        print(f"Group ID for this trace: {group_id}")
        print("This trace is linked to the previous one via the group ID.")
    else:
        print("No trace URL available. Make sure tracing is properly configured.")

async def main():
    print("🔍 Tracing Demonstration 🔍")
    print("===========================")
    print("This example shows how to configure and use tracing with voice pipelines.")
    
    # Demonstrate different tracing configurations
    await demonstrate_basic_tracing()
    group_id = await demonstrate_custom_tracing()
    await demonstrate_disabled_tracing()
    await demonstrate_conversation_tracing(group_id)
    
    print("\n===========================")
    print("Tracing Demonstration Complete!")
    print("Check the trace URLs to see the detailed traces of these interactions.")

if __name__ == "__main__":
    asyncio.run(main()) 