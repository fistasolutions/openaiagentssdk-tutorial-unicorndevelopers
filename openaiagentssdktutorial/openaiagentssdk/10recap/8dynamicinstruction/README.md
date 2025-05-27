# Dynamic Instruction Example

This example demonstrates how to create agents with dynamic instructions that can adapt based on context or user type.

## Overview

The `8dynamicinstruction.py` file shows how to:
1. Create dynamic instruction functions
2. Use context to modify agent behavior
3. Implement user-type specific responses
4. Handle dynamic agent configuration

## Key Components

1. **Context Class**:
   ```python
   @dataclass
   class UserContext:
       name: str
       is_premium: bool
   ```

2. **Dynamic Instructions Function**:
   ```python
   def dynamic_instructions(context, agent) -> str:
       user_name = context.context.name
       if context.context.is_premium:
           return f"Hello {user_name}! You are a premium user. Give detailed premium support."
       else:
           return f"Hello {user_name}! Provide standard support."
   ```

3. **Contextual Agent**:
   - Uses dynamic instructions
   - Adapts to user type
   - Provides personalized responses

## Code Explanation

```python
# Create agent using dynamic instructions
agent = Agent[UserContext](
    name="Dynamic Agent",
    instructions=dynamic_instructions,
    model=openai_model
)

# Create different user contexts
premium_user = UserContext(name="Alice", is_premium=True)
free_user = UserContext(name="Bob", is_premium=False)

# Run with different contexts
result1 = Runner.run_sync(agent, "What support do I have access to?", context=premium_user)
result2 = Runner.run_sync(agent, "What support do I have access to?", context=free_user)
```

## How to Run

1. Ensure your OpenAI API key is in the `.env` file
2. Run the script:
   ```bash
   uv run 8dynamicinstruction.py
   ```

## Expected Output

The agent will provide different responses based on user type:
- Premium users get detailed, premium-level support
- Free users get standard support with upgrade options

## Learning Points

- Creating dynamic instructions
- Using context for personalization
- Implementing user-type specific behavior
- Dynamic agent configuration
- Context-based response adaptation

## Dynamic Instruction Benefits

1. **Flexibility**:
   - Adapts to different user types
   - Provides personalized experiences
   - Maintains consistent behavior patterns

2. **Maintainability**:
   - Centralized instruction logic
   - Easy to modify behavior
   - Clear separation of concerns

## Next Steps

After understanding this example, you can explore:
- Adding more user types
- Implementing complex instruction logic
- Creating instruction templates
- Adding instruction validation
- Implementing instruction chains 