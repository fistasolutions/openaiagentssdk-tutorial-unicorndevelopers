# 🔧 Custom Function Tools Example

## What This Code Does (Big Picture)
Imagine building specialized equipment for your robot friend to solve complex problems! This code shows how to create advanced custom tools that can process user data, product information, and validate contact details using Pydantic models for structured data handling.

Now, let's go step by step!

## Step 1: Setting Up the Magic Key 🗝️
```python
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
```
The AI assistant needs a magic key (API key) to work properly.

This code finds the OpenAI API key hidden in a secret file (.env), unlocks it, and sets it as the default key for our agents.

## Step 2: Creating a Simple Helper Function 🔧
```python
# Define a simple function that does some work
def do_some_work(data: str) -> str:
    print(f"Processing data: {data}")
    return f"Processed: {data}"
```
This is a helper function that:
- Takes a string input
- Prints what it's processing
- Returns a processed version of the input

## Step 3: Creating a Pydantic Model for User Data 👤
```python
# Define a Pydantic model for function arguments
class FunctionArgs(BaseModel):
    username: str = Field(..., description="The user's name")
    age: int = Field(..., description="The user's age")
```
This creates a structured template for user data that:
- Requires a username (string)
- Requires an age (integer)
- Includes descriptions for each field

## Step 4: Creating a Function to Process User Data 🔄
```python
# Define the function that will be called by the tool
async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = FunctionArgs.model_validate_json(args)
    return do_some_work(data=f"{parsed.username} is {parsed.age} years old")
```
This function:
- Takes a context and arguments string
- Parses the arguments using our Pydantic model
- Calls our helper function with formatted user data
- Returns the processed result

## Step 5: Creating a Custom User Processing Tool 🛠️
```python
# Create a custom function tool
process_user_tool = FunctionTool(
    name="process_user",
    description="Processes extracted user data",
    params_json_schema=FunctionArgs.model_json_schema(),
    on_invoke_tool=run_function,
)
```
This creates a custom tool that:
- Has a specific name and description
- Uses the JSON schema from our Pydantic model
- Links to the function we created for processing

## Step 6: Creating a Complex Product Information Model 📦
```python
# Define a more complex Pydantic model
class ProductInfo(BaseModel):
    product_id: str = Field(..., description="Unique identifier for the product")
    name: str = Field(..., description="Name of the product")
    price: float = Field(..., description="Price of the product")
    categories: List[str] = Field(default_list=[], description="Categories the product belongs to")
    in_stock: bool = Field(..., description="Whether the product is in stock")
    description: Optional[str] = Field(None, description="Product description")
```
This creates a detailed template for product information with:
- Required fields (ID, name, price, in-stock status)
- Optional fields (description)
- A list field for categories
- Descriptions for each field

## Step 7: Creating a Product Processing Function 🏭
```python
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
```
This function:
- Parses product information from JSON
- Prints what it's processing
- Creates new derived fields (processed ID, display name, price with tax)
- Returns a dictionary with the processed information

## Step 8: Creating a Product Processing Tool 📊
```python
# Create a product processing tool
product_tool = FunctionTool(
    name="process_product",
    description="Process product information and calculate additional data",
    params_json_schema=ProductInfo.model_json_schema(),
    on_invoke_tool=process_product,
)
```
This creates a tool specifically for processing product information.

## Step 9: Creating a Contact Validation Model and Function ✅
```python
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
```
This creates:
- A model for validation requests (email required, phone optional)
- A function that performs basic validation on email and phone
- A result that includes validation status and timestamp

## Step 10: Creating a Validation Tool 🔍
```python
# Create a validation tool
validation_tool = FunctionTool(
    name="validate_contact",
    description="Validate email and optional phone number",
    params_json_schema=ValidationRequest.model_json_schema(),
    on_invoke_tool=validate_contact_info,
)
```
This creates a tool for validating contact information.

## Step 11: Creating a Multi-Tool Assistant 🤖
```python
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
```
This creates an AI assistant that:
- Has access to all three custom tools
- Knows when to use each tool based on the request
- Has clear instructions about each tool's purpose

## Step 12: Displaying Tool Schemas 📋
```python
# Print the tool schemas
def print_tool_schemas():
    print("=== Custom Function Tools ===\n")
    for tool in agent.tools:
        print(f"Tool Name: {tool.name}")
        print(f"Description: {tool.description}")
        print("Parameters Schema:")
        print(json.dumps(tool.params_json_schema, indent=2))
        print()
```
This function:
- Loops through all the tools attached to the agent
- Prints detailed information about each tool
- Shows the tool's name, description, and parameter schema
- Formats the parameter schema as readable JSON

## Step 13: Running the Program with Example Queries 🏃‍♂️
```python
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
```
This tests the assistant with different requests:
1. A user processing request
2. A product processing request
3. A contact validation request

## Step 14: Creating an Interactive Mode 💬
```python
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
```
This creates an interactive mode where:
- You can ask the assistant to use any of its tools
- You see the assistant's responses
- Errors are handled gracefully
- You can type "exit" to quit

## Final Summary 📌
✅ We created Pydantic models for structured data handling
✅ We created custom function tools for processing user data
✅ We created tools for processing product information
✅ We created tools for validating contact information
✅ We created an AI assistant that knows how to use all these tools
✅ We displayed detailed information about each tool's schema
✅ We tested the assistant with different types of requests
✅ We added an interactive mode for custom queries

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
   uv run customfunctiontools.py
   ```
4. Try asking the assistant to process different types of data!

## What You'll Learn 🧠
- How to create structured data models with Pydantic
- How to create custom function tools with detailed schemas
- How to process different types of data (user info, products, contact details)
- How to validate input data
- How to return complex structured responses
- How to use context in function tools
- How to handle errors in custom tools

Happy coding! 🎉 