# 📊 Basic Output Example

## What This Code Does (Big Picture)
Imagine having a robot assistant that can read emails or messages and automatically extract event details like meeting times, participants, and locations! This code creates an AI that can pull structured information from text and return it in a format that's easy for computers to work with.

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
from agents import Agent, Runner, ModelSettings
from pydantic import BaseModel
from agents import Agent, ModelSettings, function_tool
from dotenv import load_dotenv
from agents import set_default_openai_key
import asyncio
import os
from typing import List, Optional

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(api_key)
```
The AI assistant needs a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Defining What a Calendar Event Looks Like 📅
```python
class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: List[str]
    location: Optional[str] = None
    description: Optional[str] = None
```
This creates a template for what information we want to extract:
- Event name (required)
- Date (required)
- List of participants (required)
- Location (optional)
- Description (optional)

## Step 3: Creating an Event Extractor AI 🤖
```python
calendar_extractor = Agent(
    name="Calendar Event Extractor",
    instructions="""
    You are a specialized assistant that extracts calendar events from text.
    Extract all details about events including:
    - Event name
    - Date (in YYYY-MM-DD format)
    - List of participants
    - Location (if mentioned)
    - Description (if available)
    
    If multiple events are mentioned, focus on the most prominent one.
    If a detail is not provided in the text, omit that field from your response.
    """,
    output_type=CalendarEvent,
)
```
This creates an AI assistant that:
- Has one job: extract calendar events from text
- Knows exactly what information to look for
- Returns the information in our CalendarEvent format
- Focuses on the most prominent event if multiple are mentioned
- Omits fields that aren't provided in the text

## Step 4: Creating a Date Validation Tool ✅
```python
@function_tool
def validate_date(date_str: str) -> str:
    """Validate and format a date string to YYYY-MM-DD format"""
    try:
        # Try to parse the date - this is just an example and would need more robust parsing in a real app
        formats = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%B %d, %Y"]
        for fmt in formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                continue
        return date_str  # Return original if no format matches
    except Exception:
        return date_str
```
This tool helps the AI convert different date formats (like "May 20, 2023" or "5/20/23") into a standard format (YYYY-MM-DD) by:
- Trying multiple date formats
- Converting successfully parsed dates to YYYY-MM-DD
- Returning the original string if parsing fails

## Step 5: Creating an Advanced Extractor with the Tool 🔧
```python
advanced_calendar_extractor = Agent(
    name="Advanced Calendar Event Extractor",
    instructions="""
    You are a specialized assistant that extracts calendar events from text.
    Extract all details about events including:
    - Event name
    - Date (in YYYY-MM-DD format, use the validate_date tool to ensure correct formatting)
    - List of participants
    - Location (if mentioned)
    - Description (if available)
    
    If multiple events are mentioned, focus on the most prominent one.
    If a detail is not provided in the text, omit that field from your response.
    """,
    output_type=CalendarEvent,
    tools=[validate_date],   
)
```
This creates an improved AI that:
- Still extracts calendar events
- Can also validate and standardize dates using the tool
- Returns the same structured CalendarEvent format
- Is instructed to use the validate_date tool for date formatting

## Step 6: Running the Program with Different Texts 🏃‍♂️
```python
async def main():
    # Example texts with calendar events
    simple_text = "Let's have a team meeting on 2023-05-15 with John, Sarah, and Mike."
    
    complex_text = """
    Hi team,
    
    I'm scheduling our quarterly planning session for May 20, 2023 at the main conference room.
    All department heads (Lisa, Mark, Jennifer, and David) should attend. We'll be discussing
    our Q3 objectives and reviewing Q2 performance. Please bring your department reports.
    
    Also, don't forget about the company picnic on 06/15/2023!
    """
    
    # Example using the basic calendar extractor
    print("\n--- Basic Calendar Extractor Example ---")
    result = await Runner.run(calendar_extractor, simple_text)
    print("Extracted Event:", result.final_output)
    print(f"Event Type: {type(result.final_output)}")
    
    # Example using the advanced calendar extractor with date validation
    print("\n--- Advanced Calendar Extractor Example ---")
    result = await Runner.run(advanced_calendar_extractor, complex_text)
    print("Extracted Event:", result.final_output)
    
    # Access structured data fields
    event = result.final_output
    print(f"\nEvent Name: {event.name}")
    print(f"Date: {event.date}")
    print(f"Participants: {', '.join(event.participants)}")
    if event.location:
        print(f"Location: {event.location}")
    if event.description:
        print(f"Description: {event.description}")
```
This runs the AI on different texts and:
1. Extracts the event details from each text
2. Returns the information as structured data
3. Lets us access specific fields like name, date, and participants
4. Shows how to conditionally access optional fields

## Final Summary 📌
✅ We defined a structure for calendar events using Pydantic
✅ We created a basic AI that extracts events from text
✅ We added a tool to validate and standardize dates
✅ We created an advanced AI that uses the date validation tool
✅ We accessed the structured data fields programmatically

## Try It Yourself! 🚀
1. Install the required packages:
   ```
   uv add openai-agents python-dotenv pydantic
   ```
2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Run the program:
   ```
   uv run basicoutput.py
   ```
4. Try with different texts containing event information!

## What You'll Learn 🧠
- How to define structured output types with Pydantic
- How to make agents return structured data
- How to validate and format extracted data
- How to access structured data in your code
- How to handle optional fields in structured outputs

Happy coding! 🎉 