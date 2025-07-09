# 🛠️ Customizing Agent Handoff Example

## 📋 Overview

Welcome to the **Customizing Agent Handoff** tutorial! Now that you understand the basics, let's learn how to add custom behavior to your handoffs. This is like giving your receptionist special instructions and tools to make the handoff process more intelligent and trackable.

## 🎯 What You'll Learn

By the end of this example, you'll understand:
- ✅ How to add custom callbacks that run during handoff
- ✅ How to customize tool names and descriptions
- ✅ How to monitor and log handoff events
- ✅ How to make your handoff system more transparent and debuggable

## 🔧 Real-World Analogy

Think of a hospital where the triage nurse has special tools:
- **📞 Pager System**: Notifies specialists when they're needed
- **📋 Patient Records**: Transfers relevant information
- **🔔 Alert System**: Logs when handoffs occur for tracking
- **🏷️ Clear Labels**: Makes it obvious which specialist is being called

## 📁 Code Walkthrough

Let's break down the code step by step:

### 🔧 Step 1: Import Required Libraries
```python
from agents import Agent, Runner, handoff, RunContextWrapper
import asyncio
```

**What this does:**
- `Agent`, `Runner`, `handoff`: Core handoff functionality
- `RunContextWrapper`: Provides context information during handoff
- `asyncio`: Handles asynchronous operations

### 🎯 Step 2: Create a Custom Callback Function
```python
# ✅ Define a custom action to perform during handoff
def on_handoff(ctx: RunContextWrapper[None]):
    print("🔄 Handoff triggered! Logging event...")
```

**What this does:**
- Creates a function that runs every time a handoff occurs
- `ctx` parameter provides context about the handoff
- Perfect for logging, notifications, or custom logic

### 🎯 Step 3: Create the Specialized Agent
```python
# 🎯 Target agent for the handoff
specialist_agent = Agent(
    name="Specialist agent",
    instructions="You handle specialized tasks."
)
```

**What this does:**
- Creates the agent that will receive the handoff
- This agent has specific expertise for complex tasks

### 🔧 Step 4: Create Customized Handoff Configuration
```python
# 🔧 Customized handoff configuration
custom_handoff = handoff(
    agent=specialist_agent,
    on_handoff=on_handoff,
    tool_name_override="custom_handoff_tool",
    tool_description_override="Custom tool to transfer to a specialist agent."
)
```

**What this does:**
- `agent=specialist_agent`: Specifies which agent to handoff to
- `on_handoff=on_handoff`: Runs our custom callback function
- `tool_name_override`: Changes the tool name from auto-generated to custom
- `tool_description_override`: Provides a clear description for the agent

### 🤖 Step 5: Create the Main Agent
```python
# 🤖 Orchestrator agent that uses the customized handoff
main_agent = Agent(
    name="Main agent",
    instructions="Delegate complex tasks using custom handoffs.",
    handoffs=[custom_handoff]
)
```

**What this does:**
- Creates the main agent that receives user queries
- Includes our customized handoff in its toolkit
- Will use the custom tool name and description

### 🚀 Step 6: Test the System
```python
async def main():
    result = await Runner.run(
        main_agent,
        input="This seems like a complex task. Can you handle it?"
    )
    print("🧠 Final Output:")
    print(result.final_output)
```

## 🎨 How It Works (Visual Flow)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Query    │───▶│   Main Agent    │───▶│ Specialist Agent│
│ "Complex task"  │    │                 │    │                 │
│                 │    │ • Analyzes      │    │ • Handles       │
│                 │    │ • Uses custom   │    │   complex task  │
│                 │    │   handoff tool  │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Custom Callback│
                       │                 │
                       │ 🔄 Logs event   │
                       │ 📊 Tracks usage │
                       │ 🔔 Notifications│
                       └─────────────────┘
```

## 🚀 How to Run

1. **Navigate to the directory**:
   ```bash
   cd openaiagentssdktutorial/openaiagentssdk/17handsoff/2customizinghandsoff
   ```

2. **Set up your environment** (if not already done):
   ```bash
   # Create .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   echo "OPENAI_MODEL=gpt-4" >> .env
   ```

3. **Run the example**:
   ```bash
   python 2customizinghandsoff.py
   ```

## 📊 Expected Output

When you run this example, you should see something like:

```
🔄 Handoff triggered! Logging event...
🧠 Final Output:
I understand this is a complex task that requires specialized expertise. Let me connect you with our specialist agent who can handle this more effectively.

[Specialist agent response here...]
```

## 🛠️ Advanced Customization Examples

### 📊 Logging with Timestamps
```python
import datetime

def on_handoff_with_timestamp(ctx: RunContextWrapper[None]):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🔄 [{timestamp}] Handoff triggered to specialist agent")
    print(f"📝 User query: {ctx.input}")
    print(f"🎯 Agent: {ctx.agent.name}")
```

### 🔔 Multiple Callbacks
```python
def log_handoff(ctx: RunContextWrapper[None]):
    print("📊 Logging handoff event...")

def notify_specialist(ctx: RunContextWrapper[None]):
    print("🔔 Notifying specialist agent...")

def update_metrics(ctx: RunContextWrapper[None]):
    print("📈 Updating handoff metrics...")

# Combine multiple callbacks
def combined_callback(ctx: RunContextWrapper[None]):
    log_handoff(ctx)
    notify_specialist(ctx)
    update_metrics(ctx)

custom_handoff = handoff(
    agent=specialist_agent,
    on_handoff=combined_callback,
    tool_name_override="escalate_to_specialist",
    tool_description_override="Escalate complex issues to a specialist agent for expert handling."
)
```

### 🏷️ Descriptive Tool Names
```python
# Make tool names more descriptive
billing_handoff = handoff(
    agent=billing_agent,
    on_handoff=log_handoff,
    tool_name_override="escalate_billing_issue",
    tool_description_override="Transfer billing and payment issues to our billing specialist."
)

refund_handoff = handoff(
    agent=refund_agent,
    on_handoff=log_handoff,
    tool_name_override="process_refund_request",
    tool_description_override="Handle refund requests and return processing with our refund specialist."
)
```

## 🧪 Testing Different Scenarios

### 🔍 Test Custom Callback
```python
# This should trigger the callback
result = await Runner.run(
    main_agent,
    input="I need help with a very complex technical issue."
)
```

### 🔍 Test Tool Name Customization
```python
# The agent should use "custom_handoff_tool" instead of auto-generated name
result = await Runner.run(
    main_agent,
    input="This requires specialized knowledge."
)
```

## 🐛 Troubleshooting

### ❌ Callback Not Running
**Problem**: The handoff occurs but the callback doesn't execute.

**Solutions**:
1. **Check function signature**: Ensure callback takes `RunContextWrapper[None]` parameter
2. **Verify handoff setup**: Make sure `on_handoff=callback_function` is set
3. **Test with print statements**: Add debug prints to verify function is called

### ❌ Tool Name Not Changing
**Problem**: The tool still shows auto-generated name instead of custom name.

**Solutions**:
1. **Check parameter name**: Use `tool_name_override` (not `tool_name`)
2. **Verify agent instructions**: Make sure agent knows to use the custom tool
3. **Test with clear instructions**: Update agent instructions to mention the custom tool name

### ❌ No Handoff Occurring
**Problem**: The main agent handles everything itself instead of delegating.

**Solutions**:
1. **Check agent instructions**: Ensure main agent knows when to delegate
2. **Verify handoff list**: Make sure custom handoff is in the handoffs list
3. **Test with obvious triggers**: Use clear language that should trigger handoff

## 📚 Key Takeaways

1. **🔄 Callbacks**: Run custom code during handoff for logging, notifications, or processing
2. **🏷️ Custom Names**: Make tool names and descriptions more descriptive and clear
3. **📊 Monitoring**: Use callbacks to track handoff patterns and system usage
4. **🔧 Flexibility**: Customize handoff behavior for your specific needs

## 🎓 Next Steps

Ready to learn even more advanced handoff features? Move on to:
- **[Handoff Inputs](../3handsoffinputs/)**: Pass structured data between agents
- **[Input Filters](../4inputfilters/)**: Clean and process data before handoff
- **[Recommended Prompt](../5recomendedprompt/)**: Use best practices for reliable handoffs

## 🛠️ Real-World Applications

### 🏢 Customer Support System
```python
def log_support_handoff(ctx: RunContextWrapper[None]):
    print(f"📞 Support handoff: {ctx.input[:50]}...")
    # Could also send to CRM, create ticket, etc.

support_handoff = handoff(
    agent=support_agent,
    on_handoff=log_support_handoff,
    tool_name_override="escalate_to_support",
    tool_description_override="Escalate customer issues to human support team."
)
```

### 🏥 Healthcare Triage
```python
def log_medical_handoff(ctx: RunContextWrapper[None]):
    print(f"🏥 Medical handoff: {ctx.input[:50]}...")
    # Could also alert medical staff, update patient records, etc.

medical_handoff = handoff(
    agent=medical_agent,
    on_handoff=log_medical_handoff,
    tool_name_override="consult_medical_specialist",
    tool_description_override="Consult with medical specialist for health-related queries."
)
```

---

**🎉 Excellent!** You've now learned how to customize agent handoffs with callbacks and custom tool configurations. Your handoff system is becoming more intelligent and trackable! 🚀 