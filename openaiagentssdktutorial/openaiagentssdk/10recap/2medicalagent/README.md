# Medical Agent Example

This example demonstrates how to create a specialized AI agent for medical-related queries and assistance.

## Overview

The `2medicalagent.py` file shows how to create an agent with a specific role and domain expertise. This agent is configured to act as a medical professional, capable of answering health-related questions and providing medical information.

## Key Components

1. **Specialized Agent**:
   - Named "Doctor"
   - Configured with medical expertise
   - Uses GPT-4 model for high-quality responses

2. **Interactive Input**:
   - Takes user questions through input
   - Demonstrates real-time interaction with the agent

## Code Explanation

```python
agent = Agent(
    name="Doctor",
    instructions="You are a doctor that can answer questions and help with tasks.",
    model="gpt-4o"
)

# Interactive question handling
questionofpatient = input("Enter your question: ")
result = Runner.run_sync(agent, questionofpatient)
```

## How to Run

1. Ensure your OpenAI API key is in the `.env` file
2. Run the script:
   ```bash
   python 2medicalagent.py
   ```
3. Enter your medical question when prompted

## Expected Output

The agent will respond to medical questions with professional, doctor-like responses. Note that this is for educational purposes and not for actual medical advice.

## Learning Points

- Creating domain-specific agents
- Interactive agent communication
- Handling user input
- Real-time agent responses

## Important Notes

- This agent is for educational purposes only
- Not intended for actual medical diagnosis or advice
- Always consult real medical professionals for health concerns

## Next Steps

After understanding this example, you can explore:
- Adding medical-specific tools
- Implementing more structured responses
- Adding medical context and guidelines
- Creating other specialized agents 