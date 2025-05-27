# Basic Context Example

This example demonstrates how to use context with AI agents, showing how to create and use custom context classes for personalized agent interactions.

## Overview

The `5basiccontext.py` file shows how to:
1. Create custom context classes
2. Use context with agents
3. Implement context-aware tools
4. Handle different user types

## Key Components

1. **Context Class**:
   ```python
   @dataclass
   class UserContext:
       uid: str
       is_pro_user: bool
   ```

2. **Context-Aware Tool**:
   ```python
   @function_tool
   def greet_user(context: UserContext) -> str:
       """Give a personalized greeting based on user's status."""
   ```

3. **Contextual Agent**:
   - Uses generic type parameter for context
   - Provides different responses based on user type

## Code Explanation

```python
# Create agent with context
agent = Agent[UserContext](
    name="Simple Greeter",
    instructions="Greet the user based on their account type using the tool.",
    tools=[greet_user],
    model=openai_model
)

# Create different user contexts
pro_user = UserContext(uid="alice123", is_pro_user=True)
free_user = UserContext(uid="bob456", is_pro_user=False)

# Run with different contexts
result = Runner.run_sync(agent, "Please greet me", context=pro_user)
```

## How to Run

1. Ensure your OpenAI API key is in the `.env` file
2. Run the script:
   ```bash
   uv run 5basiccontext.py
   ```

## Expected Output

The agent will provide different greetings based on the user context:
- Pro users get a premium greeting
- Free users get a standard greeting with upgrade suggestion

## Learning Points

- Creating custom context classes
- Using dataclasses for context
- Implementing context-aware tools
- Running agents with different contexts
- Type hints with generics

## Context Usage

The example shows how to:
1. Define context structure
2. Pass context to tools
3. Use context in agent responses
4. Handle multiple context types

## Next Steps

After understanding this example, you can explore:
- Adding more context fields
- Creating complex context hierarchies
- Implementing context validation
- Adding context persistence
- Creating context-specific tools 