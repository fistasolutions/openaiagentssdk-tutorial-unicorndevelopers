from agents import (
    Agent,
    Runner,
    RunContextWrapper,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    input_guardrail,
    TResponseInputItem,
    set_default_openai_key
)
import os
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel

# Load API key
load_dotenv()
set_default_openai_key(os.getenv("OPENAI_API_KEY"))

# Step 1: Define output model for the guardrail agent
class BannedWordOutput(BaseModel):
    contains_banned_word: bool
    matched_word: str | None

# Step 2: Create a helper agent to detect banned words
banned_words = ["stupid", "idiot", "dumb"]

banned_word_detector = Agent(
    name="Banned Word Detector",
    instructions=f"""
        Check if the input contains any of the following banned words: {', '.join(banned_words)}.
        If any are found, return contains_banned_word=True and specify which word in matched_word.
        Otherwise, set contains_banned_word=False.
    """,
    output_type=BannedWordOutput,
)

# Step 3: Create the actual input guardrail function
@input_guardrail
async def banned_word_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(banned_word_detector, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.contains_banned_word,
    )

# Step 4: Define the main agent with the input guardrail attached
polite_agent = Agent(
    name="Polite Agent",
    instructions="You are a polite assistant who replies to friendly questions only.",
    input_guardrails=[banned_word_guardrail],
)

# Step 5: Run the tests
async def main():
    # Test 1: Safe input
    print("\n--- Safe Input ---")
    try:
        result = await Runner.run(polite_agent, "Hello, how are you?")
        print("Final Output:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("Guardrail triggered unexpectedly on safe input!")

    # Test 2: Unsafe input
    print("\n--- Unsafe Input ---")
    try:
        await Runner.run(polite_agent, "You are so stupid.")
        print("Guardrail did not trigger – unexpected!")
    except InputGuardrailTripwireTriggered:
        print("✅ Guardrail triggered due to banned word!")

# Run the async main using asyncio
if __name__ == "__main__":
    asyncio.run(main())
