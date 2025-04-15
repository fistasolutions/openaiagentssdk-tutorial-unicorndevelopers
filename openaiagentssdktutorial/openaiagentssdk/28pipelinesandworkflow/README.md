# 🔄 Pipelines and Workflows with AI Agents

## What This Code Does (Big Picture)
This example demonstrates how to use pipelines and workflows in the OpenAI Agents SDK to create sophisticated voice applications. It shows different ways to handle audio input, process it through an AI agent, and stream the response back as audio.

## Voice Pipeline Architecture 🏗️
A voice pipeline is a powerful system that connects audio processing with AI agents:

```
Speech-to-Text → Your Workflow → Text-to-Speech
   (Input)        (Processing)      (Output)
```

This example shows three key ways to use voice pipelines:
1. With complete audio (AudioInput)
2. With streaming audio (StreamedAudioInput)
3. With handling interruptions

## Step 1: Setting Up the Environment 🗝️
```python
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
```
This code:
- Imports the necessary libraries, including voice pipeline components
- Loads your OpenAI API key from the environment
- Sets up the default key for our agents

## Step 2: Creating Tools for Our Agent 🛠️
```python
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
```
This creates:
- A knowledge base search tool that simulates looking up company information
- A customer info tool that simulates retrieving customer data

## Step 3: Creating Our Agent 🤖
```python
support_agent = Agent(
    name="Customer Support",
    instructions="""You are a helpful customer support agent. 
    Use the knowledge base tool to answer questions about company policies, products, and services.
    Use the customer info tool when asked about specific customers.
    Be concise and professional in your responses.""",
    model="gpt-4o",
    tools=[search_knowledge_base, get_customer_info]
)
```
This creates a customer support agent that:
- Has access to the knowledge base and customer info tools
- Is instructed to be concise and professional
- Uses the GPT-4o model for responses

## Step 4: Using AudioInput (Complete Audio) 🎤
```python
# Create a voice pipeline with custom configuration
pipeline_config = VoicePipelineConfig(
    workflow_name="customer_support",
    disable_tracing=True,  # Disable tracing for this example
)

pipeline = VoicePipeline(
    workflow=SingleAgentVoiceWorkflow(support_agent),
    config=pipeline_config
)

# Create a simulated audio input
buffer = np.zeros(24000 * 3, dtype=np.int16)  # 3 seconds of silence
audio_input = AudioInput(
    buffer=buffer,
    transcription="What are your product features?"
)

# Run the pipeline
result = await pipeline.run(audio_input)
```
This demonstrates:
- Creating a pipeline with custom configuration
- Using AudioInput for complete audio processing
- Running the pipeline and getting a result

AudioInput is ideal for:
- Pre-recorded audio
- Push-to-talk applications
- When you know exactly when the user is done speaking

## Step 5: Using StreamedAudioInput (Streaming Audio) 🌊
```python
# Create a streamed audio input
streamed_input = StreamedAudioInput()

# Start the pipeline with the streamed input
result_future = asyncio.create_task(pipeline.run(streamed_input))

# Push audio chunks with transcriptions
await streamed_input.push_chunk(chunk1, transcription="Can you tell me about")
await asyncio.sleep(0.5)  # Simulate time between chunks
await streamed_input.push_chunk(chunk2, transcription="your company policy?")

# Signal that the user is done speaking
await streamed_input.end()
```
This demonstrates:
- Creating a StreamedAudioInput for real-time audio
- Pushing audio chunks as they arrive
- Signaling when the user is done speaking

StreamedAudioInput is ideal for:
- Real-time conversations
- When you need to detect when a user stops speaking
- Applications that need to process audio as it arrives

## Step 6: Handling Interruptions 🔄
```python
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
```
This demonstrates:
- Monitoring lifecycle events (turn_started, turn_ended)
- Detecting when the agent is speaking
- Handling user interruptions by starting a new turn

## Understanding Voice Stream Events 📊
The voice pipeline produces several types of events:

1. **Audio Events** (`voice_stream_event_audio`):
   - Contain chunks of audio data to play
   - Streamed in real-time for immediate playback

2. **Lifecycle Events** (`voice_stream_event_lifecycle`):
   - `turn_started`: The agent has started processing a new turn
   - `turn_ended`: The agent has finished processing a turn
   - Useful for managing conversation flow

3. **Error Events** (`voice_stream_event_error`):
   - Indicate problems in the pipeline
   - Contain error information

## Try It Yourself! 🚀
1. Install the required packages:
   ```
   uv add "openai-agents[voice]" python-dotenv numpy sounddevice
   ```
2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Run the program:
   ```
   uv run pipelinesandworkflow.py
   ```
4. Explore the different ways to handle audio input and processing!

## Best Practices 💡
- **For Complete Audio**: Use `AudioInput` when you have the full audio clip or know when the user is done speaking.
- **For Streaming Audio**: Use `StreamedAudioInput` when processing audio in real-time.
- **For Interruptions**: Monitor lifecycle events and create new pipeline runs for interruptions.
- **For Configuration**: Use `VoicePipelineConfig` to customize pipeline behavior, tracing, and model settings.

## What You'll Learn 🧠
- How to create and configure voice pipelines
- How to process complete and streaming audio
- How to handle conversation turns and interruptions
- How to monitor lifecycle events in a voice conversation
- How to build sophisticated voice applications with AI agents

Happy pipeline building! 🎉 