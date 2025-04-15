# 🎤 Voice Agents with AI Assistants 🎧

## What This Code Does (Big Picture)
This example demonstrates how to create voice-enabled AI assistants using the OpenAI Agents SDK. It shows how to build a voice pipeline that can:
1. Convert speech to text (transcription)
2. Process the text with an AI agent
3. Convert the agent's response back to speech

The result is an AI assistant you can talk to naturally!

## Voice Pipeline Explained 🔊
A voice pipeline is a three-step process:

```
Speech-to-Text → Agent Processing → Text-to-Speech
   (Input)        (Processing)        (Output)
```

Think of it like a conversation:
1. You speak (audio input)
2. The AI understands and thinks (processing)
3. The AI speaks back (audio output)

## Step 1: Setting Up the Environment 🗝️
```python
import asyncio
import random
import numpy as np
import sounddevice as sd

from agents import (
    Agent,
    function_tool,
    set_default_openai_key
)
from agents.voice import (
    AudioInput,
    SingleAgentVoiceWorkflow,
    VoicePipeline,
)
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions
from dotenv import load_dotenv
import os

# Load environment variables and set up API key
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
```
This code:
- Imports the necessary libraries, including voice-specific modules
- Loads your OpenAI API key from the environment
- Sets up the default key for our agents

## Step 2: Creating Tools for Our Voice Agent 🛠️
```python
@function_tool
def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    print(f"[debug] get_weather called with city: {city}")
    choices = ["sunny", "cloudy", "rainy", "snowy"]
    return f"The weather in {city} is {random.choice(choices)} and {random.randint(60, 90)}°F."

@function_tool
def tell_joke(topic: str = "general") -> str:
    """Tell a joke about a specific topic."""
    print(f"[debug] tell_joke called with topic: {topic}")
    jokes = {
        "weather": "What did one raindrop say to the other? Two's company, three's a cloud!",
        "programming": "Why do programmers prefer dark mode? Because light attracts bugs!",
        "food": "Why don't eggs tell jokes? They'd crack each other up!",
        "general": "Why don't scientists trust atoms? Because they make up everything!"
    }
    return jokes.get(topic.lower(), jokes["general"])
```
This creates:
- A weather tool that simulates getting weather information
- A joke tool that returns jokes on different topics

## Step 3: Creating Voice-Enabled Agents 🤖
```python
spanish_agent = Agent(
    name="Spanish Assistant",
    handoff_description="A Spanish-speaking assistant for users who prefer Spanish.",
    instructions=prompt_with_handoff_instructions(
        "You're speaking to a human, so be polite and concise. Always respond in Spanish. "
        "If asked about the weather, use the weather tool."
    ),
    model="gpt-4o",
    tools=[get_weather]
)

voice_agent = Agent(
    name="Voice Assistant",
    instructions=prompt_with_handoff_instructions(
        "You're speaking to a human through voice, so be conversational, polite, and concise. "
        "If the user speaks in Spanish, hand off to the Spanish assistant. "
        "Use the weather tool when asked about weather and the joke tool when asked for jokes."
    ),
    model="gpt-4o",
    handoffs=[spanish_agent],
    tools=[get_weather, tell_joke]
)
```
This creates:
- A Spanish-speaking agent for Spanish language requests
- A main voice agent that can handle English requests and hand off to the Spanish agent when needed

Notice the use of `prompt_with_handoff_instructions` which adds special instructions for voice interactions.

## Step 4: Setting Up the Voice Pipeline 🔊
```python
pipeline = VoicePipeline(workflow=SingleAgentVoiceWorkflow(voice_agent))
```
This creates a voice pipeline that:
- Uses a single agent workflow (our voice_agent)
- Handles the entire speech-to-text-to-speech process

## Step 5: Processing Voice Input 🎤
```python
buffer = np.zeros(24000 * 3, dtype=np.int16)
audio_input = AudioInput(
    buffer=buffer,
    transcription="What's the weather like in Miami?"
)

result = await pipeline.run(audio_input)
```
This code:
- Creates an audio input (simulated in this example)
- Runs it through the voice pipeline
- Gets a result that contains both text and audio

## Step 6: Streaming the Voice Output 🎧
```python
async for event in result.stream():
    if event.type == "voice_stream_event_audio":
        # In a real app: player.write(event.data)
        audio_chunks += 1
```
This code:
- Streams the audio response in chunks
- In a real application, would play each chunk through speakers
- Allows for real-time audio playback

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
   uv run voiceagents.py
   ```
4. For a real voice application, you would:
   - Capture microphone input
   - Stream it to the voice pipeline
   - Play the response through speakers

## Real-World Applications 🌎
- Voice assistants for customer service
- Accessibility tools for users who prefer voice interaction
- Hands-free applications for driving or cooking
- Language learning applications with pronunciation feedback
- Interactive voice response systems

## What You'll Learn 🧠
- How to create voice-enabled AI assistants
- How to set up a complete voice pipeline
- How to handle multilingual voice interactions
- How to stream audio responses in real-time
- How to integrate tools and handoffs in voice applications

Happy voice coding! 🎉 