import asyncio
import json
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from agents import Agent, RunContextWrapper, FunctionTool, Runner, set_default_openai_key
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)

# Define a simple function that does some work
def do_some_work(data: str) -> str:
    print(f"Processing data: {data}")
    return f"Processed: {data}"

# Define a Pydantic model for function arguments
class FunctionArgs(BaseModel):
    username: str = Field(..., description="The user's name")
    age: int = Field(..., description="The user's age")

# Define the function that will be called by the tool
async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = FunctionArgs.model_validate_json(args)
    return do_some_work(data=f"{parsed.username} is {parsed.age} years old")

# Create a custom function tool
process_user_tool = FunctionTool(
    name="process_user",
    description="Processes extracted user data",
    params_json_schema=FunctionArgs.model_json_schema(),
    on_invoke_tool=run_function,
)

# Define a more complex Pydantic model
class ProductInfo(BaseModel):
    product_id: str = Field(..., description="Unique identifier for the product")
    name: str = Field(..., description="Name of the product")
    price: float = Field(..., description="Price of the product")
    categories: List[str] = Field(default_list=[], description="Categories the product belongs to")
    in_stock: bool = Field(..., description="Whether the product is in stock")
    description: Optional[str] = Field(None, description="Product description")

# Function to process product information
async def process_product(ctx: RunContextWrapper[Any], args: str) -> Dict[str, Any]:
    parsed = ProductInfo.model_validate_json(args)
    
    print(f"Processing product: {parsed.name} (ID: {parsed.product_id})")
    
    # Simulate some processing
    result = {
        "processed_id": f"PROC-{parsed.product_id}",
        "display_name": parsed.name.upper(),
        "price_with_tax": round(parsed.price * 1.1, 2),
        "availability": "In Stock" if parsed.in_stock else "Out of Stock",
        "category_count": len(parsed.categories),
    }
    
    return result

# Create a product processing tool
product_tool = FunctionTool(
    name="process_product",
    description="Process product information and calculate additional data",
    params_json_schema=ProductInfo.model_json_schema(),
    on_invoke_tool=process_product,
)

# Create a custom validation tool
class ValidationRequest(BaseModel):
    email: str = Field(..., description="Email address to validate")
    phone: Optional[str] = Field(None, description="Phone number to validate")

async def validate_contact_info(ctx: RunContextWrapper[Any], args: str) -> Dict[str, Any]:
    parsed = ValidationRequest.model_validate_json(args)
    
    # Simple validation logic
    email_valid = "@" in parsed.email and "." in parsed.email
    
    phone_valid = None
    if parsed.phone:
        # Very basic validation - just checking if it has at least 10 digits
        phone_valid = sum(c.isdigit() for c in parsed.phone) >= 10
    
    return {
        "email_valid": email_valid,
        "phone_valid": phone_valid,
        "validation_timestamp": ctx.current_time.isoformat() if hasattr(ctx, 'current_time') else None
    }

# Create a validation tool
validation_tool = FunctionTool(
    name="validate_contact",
    description="Validate email and optional phone number",
    params_json_schema=ValidationRequest.model_json_schema(),
    on_invoke_tool=validate_contact_info,
)

# Create an agent with the custom tools
agent = Agent(
    name="Custom Tool Assistant",
    instructions="""
    You are an assistant that can process user data and product information.
    
    You have access to the following tools:
    - process_user: Use this to process user information (name and age)
    - process_product: Use this to process product information and get additional calculated fields
    - validate_contact: Use this to validate email addresses and phone numbers
    
    When asked about users, products, or validation, use the appropriate tool.
    """,
    tools=[process_user_tool, product_tool, validation_tool],
)

# Print the tool schemas
def print_tool_schemas():
    print("=== Custom Function Tools ===\n")
    for tool in agent.tools:
        print(f"Tool Name: {tool.name}")
        print(f"Description: {tool.description}")
        print("Parameters Schema:")
        print(json.dumps(tool.params_json_schema, indent=2))
        print()

async def main():
    
    # Print tool schemas
    print_tool_schemas()
    
    # Example queries
    queries = [
        "Process user data for John who is 30 years old",
        "Process product information for a laptop with ID LP100, named 'UltraBook Pro', priced at $999.99, in the categories 'electronics' and 'computers', and it's in stock",
        "Validate the email address user@example.com and phone number 555-123-4567"
    ]
    
    # Run the agent with each query
    for i, query in enumerate(queries):
        print(f"\n=== Query {i+1}: {query} ===")
        try:
            result = await Runner.run(agent, query)
            print("\nResponse:")
            print(result.final_output)
        except Exception as e:
            print(f"Error: {e}")
    
    # Interactive mode
    print("\n=== Interactive Mode ===")
    print("Type 'exit' to quit")
    
    while True:
        user_input = input("\nYour query: ")
        if user_input.lower() == 'exit':
            break
        
        try:
            result = await Runner.run(agent, user_input)
            print("\nResponse:")
            print(result.final_output)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 