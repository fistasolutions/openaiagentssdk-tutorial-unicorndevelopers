from agents import Agent, Runner
from dotenv import load_dotenv
from agents import set_default_openai_key
import os

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)

agent =Agent(
    name="Doctor",
    instructions="You are a doctor that can answer questions and help with tasks.   ",
    model="gpt-4o",
   
)
questionofpatient: str = input("Enter your question: ")
result =Runner.run_sync(agent, questionofpatient)
print(result.final_output)