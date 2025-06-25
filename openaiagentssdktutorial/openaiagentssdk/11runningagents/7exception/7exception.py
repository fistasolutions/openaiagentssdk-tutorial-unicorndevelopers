from agents import Agent, Runner, set_default_openai_key
from agents.exceptions import (
    AgentsException,
    MaxTurnsExceeded,
    ModelBehaviorError,
    UserError,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered
)
from dotenv import load_dotenv
import os

# Load and set API key
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))

# Define an agent
agent = Agent(
    name="FaultyAgent",
    instructions="Produce invalid output to test error handling.",
    model="gpt-4o"
)

try:
    # Try a normal run (this will work fine unless the model misbehaves)
    result = Runner.run_sync(agent, "Tell me a story about a cat who codes.")
    print("Final Output:", result.final_output)

except MaxTurnsExceeded:
    print("❌ Error: The conversation exceeded the allowed number of turns.")

except ModelBehaviorError:
    print("❌ Error: The model gave a bad response (e.g. invalid JSON).")

except InputGuardrailTripwireTriggered:
    print("🚨 Guardrail Triggered: The input didn't meet safety/validation rules.")

except OutputGuardrailTripwireTriggered:
    print("🚨 Guardrail Triggered: The output failed validation or policy checks.")

except UserError:
    print("❌ UserError: You likely made a mistake in how you used the SDK.")

except AgentsException as e:
    print(f"⚠️ General SDK Exception: {e}")

except Exception as e:
    print(f"🔥 Unexpected Error: {e}")
