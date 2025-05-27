# Guardrails Example

This example demonstrates how to implement input guardrails to ensure safe and appropriate agent responses.

## Overview

The `10gaurdrails.py` file shows how to:
1. Create input guardrails
2. Implement content filtering
3. Handle banned words
4. Manage agent safety

## Key Components

1. **Output Model**:
   ```python
   class BannedWordOutput(BaseModel):
       contains_banned_word: bool
       matched_word: str | None
   ```

2. **Guardrail Agent**:
   ```python
   banned_word_detector = Agent(
       name="Banned Word Detector",
       instructions=f"Check if the input contains any of the following banned words: {', '.join(banned_words)}.",
       output_type=BannedWordOutput,
   )
   ```

3. **Guardrail Function**:
   ```python
   @input_guardrail
   async def banned_word_guardrail(
       ctx: RunContextWrapper[None], 
       agent: Agent, 
       input: str | list[TResponseInputItem]
   ) -> GuardrailFunctionOutput:
       result = await Runner.run(banned_word_detector, input, context=ctx.context)
       return GuardrailFunctionOutput(
           output_info=result.final_output,
           tripwire_triggered=result.final_output.contains_banned_word,
       )
   ```

## Code Explanation

```python
# Define the main agent with guardrails
polite_agent = Agent(
    name="Polite Agent",
    instructions="You are a polite assistant who replies to friendly questions only.",
    input_guardrails=[banned_word_guardrail],
)

# Test cases
async def main():
    # Test safe input
    result = await Runner.run(polite_agent, "Hello, how are you?")
    
    # Test unsafe input
    try:
        await Runner.run(polite_agent, "You are so stupid.")
    except InputGuardrailTripwireTriggered:
        print("✅ Guardrail triggered due to banned word!")
```

## How to Run

1. Ensure your OpenAI API key is in the `.env` file
2. Run the script:
   ```bash
   uv run 10gaurdrails.py
   ```

## Expected Output

The system will:
1. Allow safe inputs to pass through
2. Block inputs containing banned words
3. Provide appropriate error messages

## Learning Points

- Creating input guardrails
- Implementing content filtering
- Handling banned words
- Managing agent safety
- Async guardrail execution

## Guardrail Benefits

1. **Safety**:
   - Prevents inappropriate content
   - Ensures polite interactions
   - Maintains conversation quality

2. **Flexibility**:
   - Easy to add new guardrails
   - Customizable filtering rules
   - Extensible design

## Next Steps

After understanding this example, you can explore:
- Adding more guardrail types
- Implementing complex filtering rules
- Creating custom guardrail behaviors
- Adding guardrail chains
- Implementing guardrail logging 