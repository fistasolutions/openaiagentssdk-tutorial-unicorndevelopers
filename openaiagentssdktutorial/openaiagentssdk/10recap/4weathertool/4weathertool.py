from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
from agents import set_default_openai_key
import os

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
openai_model = os.environ.get("OPENAI_MODEL")

@function_tool
def get_weather(location: str) -> str:
    """
    Get the weather of a location.
    """
    return f"The weather of {location} is sunny."
@function_tool
def sales_guide(product: str) -> str:
    """
    Get the sales guide of a product.
    """
    return f"The sales guide of {product} is a guide to sell the product."

weather_agent = Agent(
    name="Weather Agent",
    instructions="You are a weather agent. You are given a location and you need to return the weather of the location.",
    model=openai_model,
    tools=[get_weather]
)
sales_guide_agent= Agent(
    name="Sales Guide Agent",
    instructions="You are a sales guide agent. You are given a product and you need to return the sales guide of the product.",
    model=openai_model,
    tools=[sales_guide]
)

user_prompt=input("Enter your prompt: ")
result = Runner.run_sync(weather_agent,user_prompt)
print(result.final_output)

user_prompt=input("Enter your prompt: ")
result = Runner.run_sync(sales_guide_agent,user_prompt)
print(result.final_output)