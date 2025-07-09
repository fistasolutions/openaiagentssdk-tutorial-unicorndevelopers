# 📝 Recommended Prompt Prefix Example

## 📋 Overview

Welcome to the **Recommended Prompt** tutorial! This is the final piece of the agent handoff puzzle. Here you'll learn how to use the official recommended prompt prefix to ensure your agents use handoff tools reliably and consistently. Think of this as the "instruction manual" that makes your handoff system work perfectly every time.

## 🎯 What You'll Learn

By the end of this example, you'll understand:
- ✅ How to use the official recommended prompt prefix
- ✅ Why prompt engineering is crucial for reliable handoffs
- ✅ How to ensure consistent handoff behavior
- ✅ Best practices for agent instructions

## 📚 Real-World Analogy

Think of a restaurant with a well-trained staff:
- **Training Manual** (Recommended Prompt): Contains standard procedures and best practices
- **Chef** (Agent): Knows exactly when and how to delegate tasks
- **Sous Chef** (Handoff Agent): Receives clear, specific instructions
- **Consistent Quality**: Every dish is prepared the same way, every time

The training manual ensures everyone follows the same process!

## 📁 Code Walkthrough

Let's break down the code step by step:

### 🔧 Step 1: Import Required Libraries
```python
import os
from dotenv import load_dotenv
from agents import Agent, Runner, handoff, set_default_openai_key
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
```

**What this does:**
- `RECOMMENDED_PROMPT_PREFIX`: The official, tested prompt prefix for reliable handoffs
- Other imports: Core agent functionality and environment setup

### 🔐 Step 2: Set Up Environment
```python
# 🔐 Load API keys
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
openai_model = os.environ.get("OPENAI_MODEL")
```

**What this does:**
- Loads your OpenAI API credentials
- Sets up the AI model to use

### 🧾 Step 3: Create the Refund Agent
```python
# 🧾 Refund Agent (receives handoff)
refund_agent = Agent(
    name="Refund Agent",
    instructions="You specialize in handling refund-related customer queries.",
    model=openai_model
)
```

**What this does:**
- Creates a specialized agent for handling refund requests
- This agent has specific expertise in refund processing

### 🤝 Step 4: Create the Handoff
```python
# 🤝 Handoff object
refund_handoff = handoff(agent=refund_agent)
```

**What this does:**
- Creates a simple handoff to the refund agent
- Uses default settings for maximum reliability

### 🧠 Step 5: Create the Triage Agent with Recommended Prompt
```python
# 🧠 Main Triage Agent with recommended handoff instructions
triage_agent = Agent(
    name="Triage Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are a customer service assistant. Handle general inquiries, but if the question is about refunds, use the refund tool.""",
    model=openai_model,
    handoffs=[refund_handoff],
)
```

**What this does:**
- `f"""{RECOMMENDED_PROMPT_PREFIX}`: Includes the official prompt prefix
- The prefix contains tested instructions for reliable handoff behavior
- Custom instructions are added after the prefix

### 🚀 Step 6: Test the System
```python
# 🚀 Test query
result = Runner.run_sync(triage_agent, "I want to request a refund for my last order.")

# 🖨️ Output
print("🤖 Final Output:\n", result.final_output)
```

## 🎨 How It Works (Visual Flow)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Query    │───▶│  Triage Agent   │───▶│  Refund Agent   │
│ "I want refund" │    │                 │    │                 │
│                 │    │ • Uses          │    │ • Handles       │
│                 │    │   recommended   │    │   prompt        │
│                 │    │   prefix        │    │   behavior      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │ Recommended     │
                       │ Prompt Prefix   │
                       │                 │
                       │ • Clear         │
                       │   instructions  │
                       │ • Reliable      │
                       │   behavior      │
                       │ • Best          │
                       │   practices     │
                       └─────────────────┘
```

## 🚀 How to Run

1. **Navigate to the directory**:
   ```bash
   cd openaiagentssdktutorial/openaiagentssdk/17handsoff/5recomendedprompt
   ```

2. **Set up your environment** (if not already done):
   ```bash
   # Create .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   echo "OPENAI_MODEL=gpt-4" >> .env
   ```

3. **Run the example**:
   ```bash
   python 5recomendedprompt.py
   ```

## 📊 Expected Output

When you run this example, you should see something like:

```
🤖 Final Output:
I understand you'd like to request a refund for your last order. Let me connect you with our refund specialist who can help you with this process.

[Refund agent response with detailed refund process...]
```

## 🔍 What's in the Recommended Prompt Prefix?

The `RECOMMENDED_PROMPT_PREFIX` contains carefully crafted instructions that:

### 🎯 Clear Handoff Instructions
- Tells the agent when to use handoff tools
- Explains how to identify which tool to use
- Provides guidance on when NOT to handoff

### 🔧 Tool Usage Guidelines
- Explains how to call handoff tools correctly
- Provides examples of proper tool usage
- Ensures consistent behavior across different agents

### 📝 Best Practices
- Encourages the agent to be helpful and clear
- Ensures proper communication with users
- Maintains professional tone and approach

## 🛠️ Advanced Prompt Examples

### 🎯 Multi-Agent System
```python
# Create multiple specialized agents
billing_agent = Agent(name="Billing Agent", instructions="Handle billing and payment issues.")
technical_agent = Agent(name="Technical Agent", instructions="Handle technical problems.")
refund_agent = Agent(name="Refund Agent", instructions="Handle refund requests.")

# Create handoffs
billing_handoff = handoff(agent=billing_agent)
technical_handoff = handoff(agent=technical_agent)
refund_handoff = handoff(agent=refund_agent)

# Main agent with comprehensive instructions
main_agent = Agent(
    name="Customer Service Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are a customer service assistant. Route queries to the appropriate specialist:

- Billing issues: Use the billing tool
- Technical problems: Use the technical tool  
- Refund requests: Use the refund tool
- General questions: Handle directly

Always be helpful and professional.""",
    model=openai_model,
    handoffs=[billing_handoff, technical_handoff, refund_handoff]
)
```

### 🏥 Healthcare Triage System
```python
# Specialized medical agents
cardiology_agent = Agent(name="Cardiology Specialist", instructions="Handle heart-related issues.")
orthopedics_agent = Agent(name="Orthopedics Specialist", instructions="Handle bone and joint issues.")
neurology_agent = Agent(name="Neurology Specialist", instructions="Handle brain and nervous system issues.")

# Create handoffs
cardiology_handoff = handoff(agent=cardiology_agent)
orthopedics_handoff = handoff(agent=orthopedics_agent)
neurology_handoff = handoff(agent=neurology_agent)

# Triage agent with medical routing
triage_agent = Agent(
    name="Medical Triage Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are a medical triage assistant. Route patient concerns to appropriate specialists:

- Heart-related symptoms: Use cardiology tool
- Bone/joint pain: Use orthopedics tool
- Neurological symptoms: Use neurology tool
- General health questions: Handle directly

Always prioritize patient safety and provide appropriate disclaimers.""",
    model=openai_model,
    handoffs=[cardiology_handoff, orthopedics_handoff, neurology_handoff]
)
```

### 🏢 Business Support System
```python
# Business support agents
sales_agent = Agent(name="Sales Agent", instructions="Handle sales inquiries and product questions.")
support_agent = Agent(name="Support Agent", instructions="Handle technical support issues.")
billing_agent = Agent(name="Billing Agent", instructions="Handle billing and account issues.")

# Create handoffs
sales_handoff = handoff(agent=sales_agent)
support_handoff = handoff(agent=support_agent)
billing_handoff = handoff(agent=billing_agent)

# Business assistant with clear routing
business_agent = Agent(
    name="Business Assistant",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are a business assistant. Route inquiries to the appropriate department:

- Product questions, pricing, sales: Use sales tool
- Technical problems, bugs, usage: Use support tool
- Billing, payments, accounts: Use billing tool
- General business questions: Handle directly

Maintain professional business communication.""",
    model=openai_model,
    handoffs=[sales_handoff, support_handoff, billing_handoff]
)
```

## 🧪 Testing Different Scenarios

### 🔍 Test Refund Routing
```python
# Should route to refund agent
result = await Runner.run(
    triage_agent,
    input="I need to return this item and get my money back."
)
```

### 🔍 Test General Query
```python
# Should handle directly (no handoff)
result = await Runner.run(
    triage_agent,
    input="What are your business hours?"
)
```

### 🔍 Test Edge Cases
```python
# Should route appropriately
result = await Runner.run(
    triage_agent,
    input="I was charged twice for my subscription and want a refund."
)
```

## 🐛 Troubleshooting

### ❌ Agent Not Using Handoff Tools
**Problem**: The agent handles everything itself instead of delegating.

**Solutions**:
1. **Check prompt prefix**: Ensure `RECOMMENDED_PROMPT_PREFIX` is included
2. **Verify instructions**: Make sure custom instructions are clear about when to handoff
3. **Test with obvious triggers**: Use clear language that should trigger handoff
4. **Review tool descriptions**: Ensure handoff tools have clear descriptions

### ❌ Wrong Tool Selection
**Problem**: Agent uses the wrong handoff tool for the query.

**Solutions**:
1. **Improve instructions**: Make routing criteria more specific
2. **Add examples**: Provide clear examples of when to use each tool
3. **Test thoroughly**: Try various query phrasings to ensure proper routing
4. **Refine tool descriptions**: Make tool purposes clearer

### ❌ Inconsistent Behavior
**Problem**: Agent behavior varies between runs.

**Solutions**:
1. **Use recommended prefix**: Always include the official prompt prefix
2. **Keep instructions simple**: Avoid overly complex routing logic
3. **Test repeatedly**: Run the same query multiple times to check consistency
4. **Monitor performance**: Track handoff success rates

## 📚 Key Takeaways

1. **📝 Use Official Prefix**: Always include `RECOMMENDED_PROMPT_PREFIX` for reliable handoffs
2. **🎯 Clear Instructions**: Make routing criteria explicit and specific
3. **🔧 Consistent Behavior**: The recommended prefix ensures predictable results
4. **📊 Best Practices**: Follow established patterns for optimal performance

## 🎓 Next Steps

Congratulations! You've completed the full Agent Handoff tutorial. You now know:

- ✅ **Basic Handoff**: How to create and use simple agent handoffs
- ✅ **Customization**: How to add callbacks and custom behavior
- ✅ **Structured Data**: How to pass validated information between agents
- ✅ **Input Filtering**: How to clean and preprocess data
- ✅ **Best Practices**: How to use recommended prompts for reliability

## 🛠️ Real-World Applications

### 🏢 Enterprise Customer Support
```python
# Large-scale customer support system
enterprise_agent = Agent(
    name="Enterprise Support",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are an enterprise customer support agent. Route issues appropriately:

- Technical problems: Use technical support tool
- Billing issues: Use billing tool
- Account management: Use account tool
- Feature requests: Use product tool
- Escalations: Use escalation tool

Maintain enterprise-level professionalism and documentation.""",
    handoffs=[tech_handoff, billing_handoff, account_handoff, product_handoff, escalation_handoff]
)
```

### 🏥 Healthcare System
```python
# Comprehensive healthcare triage
healthcare_agent = Agent(
    name="Healthcare Triage",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are a healthcare triage assistant. Route patient concerns appropriately:

- Emergency symptoms: Use emergency tool
- Chronic conditions: Use specialist tool
- Medication questions: Use pharmacy tool
- Appointment scheduling: Use scheduling tool
- General health: Handle directly

Always prioritize patient safety and provide appropriate medical disclaimers.""",
    handoffs=[emergency_handoff, specialist_handoff, pharmacy_handoff, scheduling_handoff]
)
```

---

**🎉 Congratulations!** You've mastered the complete Agent Handoff system! You now have all the tools and knowledge to build sophisticated, reliable multi-agent systems that can intelligently route and handle complex workflows. Your AI applications are now ready for the real world! 🚀 