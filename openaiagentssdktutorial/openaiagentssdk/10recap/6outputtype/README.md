# Output Type Example

This example demonstrates how to use structured output types with AI agents, showing how to define and enforce specific response formats.

## Overview

The `6outputtype.py` file shows how to:
1. Define structured output models
2. Enforce response formats
3. Use Pydantic models for validation
4. Handle typed agent responses

## Key Components

1. **Output Model**:
   ```python
   class CalendarEvent(BaseModel):
       name: str
       date: str
       participants: list[str]
   ```

2. **Typed Agent**:
   - Uses output_type parameter
   - Enforces structured responses
   - Validates output format

## Code Explanation

```python
# Create an agent with structured output
agent = Agent(
    name="Simple Calendar Agent",
    instructions="Extract calendar events from the input text. Include event name, date, and participants.",
    output_type=CalendarEvent,  # Enforces structured output
    model=openai_model
)

# Run with example input
query = "Schedule a team meeting called 'Sprint Review' on July 3rd with Alice, Bob, and Charlie."
result = Runner.run_sync(agent, query)
```

## How to Run

1. Ensure your OpenAI API key is in the `.env` file
2. Run the script:
   ```bash
   uv run 6outputtype.py
   ```

## Expected Output

The agent will return a structured response matching the CalendarEvent model:
```python
{
    "name": "Sprint Review",
    "date": "July 3rd",
    "participants": ["Alice", "Bob", "Charlie"]
}
```

## Learning Points

- Creating Pydantic models
- Enforcing output types
- Structured response handling
- Type validation
- Data extraction patterns

## Output Type Benefits

1. **Type Safety**:
   - Ensures consistent response format
   - Validates data types
   - Prevents malformed responses

2. **Structured Data**:
   - Easy to process programmatically
   - Clear data contract
   - Predictable format

## Next Steps

After understanding this example, you can explore:
- Creating more complex output models
- Adding validation rules
- Implementing nested structures
- Handling optional fields
- Creating custom validators 