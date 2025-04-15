# 🔍 Tracing with AI Agents

## What This Code Does (Big Picture)
This example demonstrates how to use tracing in the OpenAI Agents SDK to monitor, debug, and analyze voice interactions with AI agents. Tracing provides detailed insights into how your agents process requests, make decisions, and generate responses.

## Why Tracing Matters 🕵️‍♀️
Tracing is like having a flight recorder for your AI interactions. It helps you:
- Debug issues when things go wrong
- Understand how your agents make decisions
- Analyze conversation patterns
- Improve your agent's performance over time
- Link related interactions together

## Step 1: Setting Up the Environment 🗝️
```python
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
```
This code:
- Imports the necessary libraries, including tracing components
- Loads your OpenAI API key from the environment
- Sets up the default key for our agents

## Step 2: Creating Tools and an Agent 🛠️
```python
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
```
This creates:
- A time tool that returns the current time
- A tip calculator tool
- A voice assistant agent with access to these tools

## Step 3: Basic Tracing (Default Settings) 🔎
```python
# Create a voice pipeline with default tracing (enabled)
pipeline = VoicePipeline(
    workflow=SingleAgentVoiceWorkflow(assistant)
)

# Create a simulated audio input
audio_input = AudioInput(
    buffer=buffer,
    transcription="What time is it?"
)

# Run the pipeline
result = await pipeline.run(audio_input)

# Get the trace URL
trace_url = get_trace_url()
```
This demonstrates:
- Creating a pipeline with default tracing settings
- Running a voice interaction
- Getting the URL to view the trace

By default, tracing is enabled and captures:
- The agent's thought process
- Tool calls and their results
- The final response

## Step 4: Custom Tracing Configuration ⚙️
```python
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
```
This demonstrates:
- Naming your workflow for easier identification
- Using a group ID to link related interactions
- Controlling what sensitive data is included in traces
- Adding custom metadata to your traces

## Step 5: Disabling Tracing 🚫
```python
# Create a voice pipeline with tracing disabled
pipeline_config = VoicePipelineConfig(
    disable_tracing=True  # Disable tracing completely
)

pipeline = VoicePipeline(
    workflow=SingleAgentVoiceWorkflow(assistant),
    config=pipeline_config
)
```
This demonstrates:
- How to completely disable tracing when needed
- Useful for production environments or privacy-sensitive applications

## Step 6: Tracing Multi-Turn Conversations 🔄
```python
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
```
This demonstrates:
- Linking multiple interactions in a conversation using the same group ID
- Updating metadata to reflect the conversation turn
- Creating a complete picture of a multi-turn interaction

## Key Tracing Configuration Options 🔧
The `VoicePipelineConfig` class provides several options for controlling tracing:

- **disable_tracing**: Controls whether tracing is disabled (default: False)
- **trace_include_sensitive_data**: Controls whether traces include potentially sensitive data like transcripts (default: False)
- **trace_include_sensitive_audio_data**: Controls whether traces include audio data (default: False)
- **workflow_name**: The name of the trace workflow for easier identification
- **group_id**: A unique identifier to link related traces together
- **trace_metadata**: Additional custom metadata to include with the trace

## Try It Yourself! 🚀
1. Install the required packages:
   ```
   uv add "openai-agents[voice]" python-dotenv numpy
   ```
2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Run the program:
   ```
   uv run tracing.py
   ```
4. Check the trace URLs in the output to see detailed traces of your interactions!

## Best Practices for Tracing 💡
- **Use Group IDs**: Link related interactions with the same group ID
- **Add Metadata**: Include relevant context in trace_metadata
- **Name Your Workflows**: Use descriptive workflow_name values
- **Be Careful with Sensitive Data**: Only include sensitive data when necessary
- **Disable in Production**: Consider disabling tracing in production for sensitive applications

## What You'll Learn 🧠
- How to configure tracing for voice pipelines
- How to link related interactions with group IDs
- How to control what data is included in traces
- How to access and analyze trace information
- How to use tracing for debugging and improving your agents

Happy tracing! 🎉 