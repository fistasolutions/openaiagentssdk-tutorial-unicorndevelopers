from agents import Agent, Runner, function_tool, set_default_openai_key
from dotenv import load_dotenv
import os

# === Load ENV and Set OpenAI Key ===
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
openai_model = os.environ.get("OPENAI_MODEL")


@function_tool
def calculate_bmi(weight: float, height: float) -> str:
    """
    Calculate the Body Mass Index (BMI) based on weight and height.

    Args:
        weight: The weight of the person in kilograms.
        height: The height of the person in meters.
    """
    bmi = weight / (height ** 2)
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 24.9:
        category = "Normal weight"
    elif bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obese"
    return f"BMI is {bmi:.2f}, which is considered {category}."


# === Agent Configuration ===
agent = Agent(
    name="HealthAssistant",
    instructions="You are a health assistant that can calculate BMI using a tool.",
    tools=[calculate_bmi],
    model=openai_model
)

# === Run Synchronously ===
result = Runner.run_sync(agent, "Calculate BMI for someone who is 68 kg and 1.75 meters tall.")
print("🔹 Final Output:\n", result.final_output)
