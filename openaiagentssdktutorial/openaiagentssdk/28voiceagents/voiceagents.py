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

# Define a weather tool
@function_tool
def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    print(f"[debug] get_weather called with city: {city}")
    choices = ["sunny", "cloudy", "rainy", "snowy"]
    return f"The weather in {city} is {random.choice(choices)} and {random.randint(60, 90)}°F."

# Define a joke tool
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

# Create a Spanish-speaking agent
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

# Create a main voice agent
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

async def simulate_voice_interaction():
    """Simulate a voice interaction with the agent."""
    # Create a voice pipeline with our agent
    pipeline = VoicePipeline(workflow=SingleAgentVoiceWorkflow(voice_agent))
    
    # For demonstration purposes, we'll create a simulated audio input
    # In a real application, this would come from a microphone
    print("Simulating user saying: 'What's the weather like in Miami?'")
    
    # Create a silent buffer (in a real app, this would be actual voice data)
    buffer = np.zeros(24000 * 3, dtype=np.int16)
    audio_input = AudioInput(
        buffer=buffer,
        # For simulation, we'll provide the transcription directly
        transcription="What's the weather like in Miami?"
    )

    # Run the voice pipeline
    print("\nProcessing voice request...")
    result = await pipeline.run(audio_input)
    
    print("\nAgent is responding with voice. Streaming audio...")
    
    # In a real application, we would play the audio
    # Here we'll just print when audio chunks would be played
    audio_chunks = 0
    async for event in result.stream():
        if event.type == "voice_stream_event_audio":
            audio_chunks += 1
            # In a real app: player.write(event.data)
    
    print(f"Audio response complete (would have played {audio_chunks} audio chunks)")
    print(f"Text of response: {result.text}")
    
    # Simulate a second interaction in Spanish
    print("\n---\n")
    print("Simulating user saying in Spanish: '¿Cómo está el clima hoy?'")
    
    audio_input = AudioInput(
        buffer=buffer,
        transcription="¿Cómo está el clima hoy?"
    )
    
    print("\nProcessing Spanish voice request...")
    result = await pipeline.run(audio_input)
    
    print("\nAgent is responding with voice in Spanish. Streaming audio...")
    audio_chunks = 0
    async for event in result.stream():
        if event.type == "voice_stream_event_audio":
            audio_chunks += 1
    
    print(f"Spanish audio response complete (would have played {audio_chunks} audio chunks)")
    print(f"Text of response: {result.text}")

async def main():
    print("🎤 Voice Agent Demonstration 🎧")
    print("===============================")
    print("This simulation shows how voice agents work with the OpenAI Agents SDK.")
    print("In a real application, the audio would come from a microphone and be played through speakers.")
    print("For this demo, we're simulating the audio I/O and showing the text transcriptions.\n")
    
    await simulate_voice_interaction()
    
    print("\n===============================")
    print("Voice Agent Demonstration Complete!")
    print("In a real application, you would:")
    print("1. Capture real audio from a microphone")
    print("2. Stream the audio to the voice pipeline")
    print("3. Play the response audio through speakers")
    print("4. Continue the conversation in a loop")

if __name__ == "__main__":
    asyncio.run(main()) 