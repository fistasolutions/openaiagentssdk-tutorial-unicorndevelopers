from pydantic import BaseModel
from agents import Agent, Runner, set_default_openai_key
import asyncio
import os
from dotenv import load_dotenv

# Load your OpenAI API key from the .env file
load_dotenv()
set_default_openai_key(os.getenv("OPENAI_API_KEY"))
openai_model = os.environ.get("OPENAI_MODEL")
# Step 1: Define a structured output model
class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

# Step 2: Create an agent that uses this model
agent = Agent(
    name="Simple Calendar Agent",
    instructions="Extract calendar events from the input text. Include event name, date, and participants.",
    output_type=CalendarEvent,  # 👈 This is the structured output!
    model=openai_model
)

# Step 3: Run the agent

query = "Schedule a team meeting called 'Sprint Review' on July 3rd with Alice, Bob, and Charlie."
result = Runner.run_sync(agent, query)
print("\nStructured Output:")
print(result.final_output)  # This will be a CalendarEvent object!
