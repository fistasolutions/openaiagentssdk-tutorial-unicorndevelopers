# 🤝 Basic Agent Handoff Example

## 📋 Overview

Welcome to your first step into the world of **Agent Handoff**! This example demonstrates the fundamental concept of how one AI agent can intelligently delegate tasks to specialized agents. Think of it as creating a smart receptionist who knows exactly which expert to connect you with.

## 🎯 What You'll Learn

By the end of this example, you'll understand:
- ✅ How to create specialized agents for different tasks
- ✅ How to set up a triage agent that routes queries
- ✅ The basic syntax for agent handoff
- ✅ How to test and verify handoff behavior

## 🏥 Real-World Analogy

Imagine a customer service center:
- **Receptionist** (Triage Agent): Greets customers and determines their needs
- **Billing Specialist** (Billing Agent): Handles payment and subscription issues
- **Refund Specialist** (Refund Agent): Processes refund requests and complaints

The receptionist doesn't solve problems directly but ensures customers talk to the right expert!

## 📁 Code Walkthrough

Let's break down the code step by step:

### 🔧 Step 1: Import Required Libraries
```python
from agents import Agent, Runner, handoff
import asyncio
```

**What this does:**
- `Agent`: Creates AI agents with specific roles
- `Runner`: Executes agent conversations
- `handoff`: Enables delegation between agents
- `asyncio`: Handles asynchronous operations

### 🎯 Step 2: Create Specialized Agents
```python
# 🧾 Specialized agents
billing_agent = Agent(name="Billing agent", instructions="You handle billing queries.")
refund_agent = Agent(name="Refund agent", instructions="You handle refund-related issues.")
```

**What this does:**
- Creates two specialized agents with specific expertise
- Each agent has a clear role and instructions
- These agents will handle the actual work

### 🤝 Step 3: Create the Triage Agent
```python
# 🤝 Triage agent with handoffs to billing and refund agents
triage_agent = Agent(
    name="Triage agent",
    instructions="You route the user's query to the correct department.",
    handoffs=[
        billing_agent,  # Direct agent handoff (tool name will be auto-generated)
        handoff(refund_agent)  # Customizable handoff with default behavior
    ]
)
```

**What this does:**
- Creates a main agent that receives all user queries
- Defines handoffs to both specialized agents
- Shows two different ways to set up handoffs:
  - **Direct handoff**: `billing_agent` (simple)
  - **Explicit handoff**: `handoff(refund_agent)` (more control)

### 🚀 Step 4: Test the System
```python
async def main():
    print("🧪 Running Handoff Demo...\n")

    result = await Runner.run(
        triage_agent,
        input="I would like a refund for my last purchase."
    )

    print("🧠 Final Output:")
    print(result.final_output)
```

**What this does:**
- Runs the triage agent with a test query
- The agent should automatically route to the refund specialist
- Displays the final response

## 🎨 How It Works (Visual Flow)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Query    │───▶│  Triage Agent   │───▶│  Refund Agent   │
│ "I want a       │    │                 │    │                 │
│  refund"        │    │ • Analyzes query│    │ • Processes     │
│                 │    │ • Decides route │    │   refund        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Billing Agent  │
                       │                 │
                       │ • Handles       │
                       │   billing       │
                       └─────────────────┘
```

## 🚀 How to Run

1. **Navigate to the directory**:
   ```bash
   cd openaiagentssdktutorial/openaiagentssdk/17handsoff/1basichandsoff
   ```

2. **Set up your environment** (if not already done):
   ```bash
   # Create .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   echo "OPENAI_MODEL=gpt-4" >> .env
   ```

3. **Run the example**:
   ```bash
   python 1basichandsoff.py
   ```

## 📊 Expected Output

When you run this example, you should see something like:

```
🧪 Running Handoff Demo...

🧠 Final Output:
I understand you'd like a refund for your last purchase. Let me help you with that.

To process your refund, I'll need a few details:
1. Your order number or transaction ID
2. The reason for the refund
3. Your preferred refund method (original payment method, store credit, etc.)

Could you please provide your order number so I can look up the details?
```

## 🧪 Testing Different Scenarios

Try these different queries to see how the triage agent routes them:

### 💳 Billing Query
```python
"I was charged twice for my subscription this month."
```
**Expected**: Routes to Billing Agent

### 💰 Refund Query
```python
"I want to return this item and get my money back."
```
**Expected**: Routes to Refund Agent

### 🤔 General Query
```python
"What are your business hours?"
```
**Expected**: Handled by Triage Agent (no handoff needed)

## 🛠️ Customization Ideas

### 🎯 Add More Specialized Agents
```python
technical_agent = Agent(
    name="Technical Support",
    instructions="You handle technical issues and troubleshooting."
)

account_agent = Agent(
    name="Account Management",
    instructions="You handle account-related queries and updates."
)

# Add to triage agent
triage_agent = Agent(
    name="Triage agent",
    instructions="You route the user's query to the correct department.",
    handoffs=[
        billing_agent,
        refund_agent,
        technical_agent,
        account_agent
    ]
)
```

### 📝 Improve Triage Instructions
```python
triage_agent = Agent(
    name="Triage agent",
    instructions="""
    You are a customer service triage agent. Your job is to:
    1. Analyze the user's query
    2. Determine which department should handle it:
       - Billing: Payment issues, charges, subscriptions
       - Refunds: Return requests, refund processing
       - Technical: App problems, login issues
       - Account: Profile updates, account settings
    3. Route to the appropriate specialist
    4. If unclear, ask for clarification
    """,
    handoffs=[billing_agent, refund_agent]
)
```

## 🐛 Troubleshooting

### ❌ Agent Not Delegating
**Problem**: The triage agent handles everything itself instead of delegating.

**Solutions**:
1. **Check instructions**: Make sure the triage agent knows it should delegate
2. **Test with clear keywords**: Use obvious terms like "refund" or "billing"
3. **Verify handoff setup**: Ensure agents are properly added to the handoffs list

### ❌ No Output
**Problem**: The script runs but produces no output.

**Solutions**:
1. **Check API key**: Ensure your OpenAI API key is set in `.env`
2. **Verify model**: Make sure the model name is correct
3. **Check imports**: Ensure all required libraries are installed

### ❌ Wrong Agent Handling Query
**Problem**: Billing queries go to refund agent or vice versa.

**Solutions**:
1. **Refine instructions**: Make specialized agent instructions more specific
2. **Improve triage logic**: Update triage agent instructions for better routing
3. **Test thoroughly**: Try various query phrasings

## 📚 Key Takeaways

1. **🎯 Specialization**: Each agent has a specific role and expertise
2. **🔄 Delegation**: The triage agent doesn't solve problems, it routes them
3. **⚙️ Flexibility**: You can add as many specialized agents as needed
4. **🧪 Testing**: Always test with various query types to ensure proper routing

## 🎓 Next Steps

Ready to learn more advanced handoff features? Move on to:
- **[Customizing Handoff](../2customizinghandsoff/)**: Add callbacks and custom behavior
- **[Handoff Inputs](../3handsoffinputs/)**: Pass structured data between agents
- **[Input Filters](../4inputfilters/)**: Clean and process data before handoff

---

**🎉 Congratulations!** You've successfully created your first agent handoff system. You now understand the fundamental concept of intelligent task delegation between AI agents! 🚀 