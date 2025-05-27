from agents import Agent, Runner
from dotenv import load_dotenv
from agents import set_default_openai_key
import os

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
openai_model = os.environ.get("OPENAI_MODEL")

agent = Agent(
    name="Sales Agent",
    instructions="You are a sales agent. You are given a product and a customer. You need to sell the product to the customer.",
    model=openai_model
)

user_prompt=input("Enter your prompt: ")
result = Runner.run_sync(agent,user_prompt)
print(result.final_output)