# 📦 Handoff Inputs Example

## 📋 Overview

Welcome to the **Handoff Inputs** tutorial! Now you're ready to learn how to pass structured, validated data between agents during handoff. This is like giving your receptionist a detailed form to fill out before transferring a call, ensuring the specialist has all the necessary information.

## 🎯 What You'll Learn

By the end of this example, you'll understand:
- ✅ How to define structured data models using Pydantic
- ✅ How to pass validated information between agents
- ✅ How to use async callbacks with structured data
- ✅ How to ensure data integrity during handoff

## 📋 Real-World Analogy

Think of a hospital emergency room:
- **Triage Nurse** (Main Agent): Assesses patient and fills out a detailed form
- **Patient Form** (Pydantic Model): Contains structured data like symptoms, urgency level, medical history
- **Specialist Doctor** (Handoff Agent): Receives the completed form with all relevant information
- **Validation System**: Ensures all required fields are filled correctly

## 📁 Code Walkthrough

Let's break down the code step by step:

### 🔧 Step 1: Import Required Libraries
```python
import os
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import Agent, handoff, Runner, RunContextWrapper, set_default_openai_key
```

**What this does:**
- `pydantic.BaseModel`: Creates structured data models with validation
- `asyncio`: Handles asynchronous operations
- `RunContextWrapper`: Provides context during handoff
- Other imports: Core agent functionality

### 🔐 Step 2: Set Up Environment
```python
# 🔐 Load OpenAI key and model
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
openai_model = os.environ.get("OPENAI_MODEL")
```

**What this does:**
- Loads your OpenAI API credentials
- Sets up the AI model to use

### 📝 Step 3: Define the Data Model
```python
# 📝 Define expected handoff input
class EscalationData(BaseModel):
    reason: str
```

**What this does:**
- Creates a Pydantic model that defines the structure of data to pass
- `reason: str` means the handoff must include a reason field that's a string
- Pydantic automatically validates the data structure

### 🔁 Step 4: Create Async Callback Function
```python
# 🔁 Callback executed when handoff is triggered
async def on_handoff(ctx: RunContextWrapper[None], input_data: EscalationData):
    print(f"🚨 Escalation triggered with reason: {input_data.reason}")
```

**What this does:**
- `async def`: Makes this function asynchronous (can handle complex operations)
- `input_data: EscalationData`: Receives the validated structured data
- Accesses the `reason` field from the validated data
- Perfect for logging, notifications, or database updates

### 🎯 Step 5: Create the Escalation Agent
```python
# 🎯 Escalation agent
escalation_agent = Agent(
    name="Escalation Agent",
    instructions="You handle high-priority customer complaints.",
    model=openai_model
)
```

**What this does:**
- Creates the specialized agent that will receive the handoff
- This agent handles escalated customer issues

### 🔧 Step 6: Create Handoff with Input Type
```python
# 🔧 Handoff object with input type + callback
escalation_handoff = handoff(
    agent=escalation_agent,
    on_handoff=on_handoff,
    input_type=EscalationData
)
```

**What this does:**
- `agent=escalation_agent`: Specifies the target agent
- `on_handoff=on_handoff`: Runs our async callback function
- `input_type=EscalationData`: Tells the system to expect structured data matching our model

### 🧠 Step 7: Create the Triage Agent
```python
# 🧠 Central agent that may escalate
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are a customer support agent. If a complaint is very serious, escalate it using the handoff tool."
        " Ask the user for a reason and pass it to the escalation tool."
    ),
    model=openai_model,
    handoffs=[escalation_handoff],
)
```

**What this does:**
- Creates the main agent that receives customer queries
- Instructions tell it to escalate serious complaints
- Must collect a reason and pass it as structured data

### 🚀 Step 8: Test the System
```python
# 🚀 Run the agent
result = Runner.run_sync(
    triage_agent,
    "This is outrageous, my credit card was charged twice and nobody is responding!"
)

# 🖨️ Show result
print("🤖 Final Output:\n", result.final_output)
```

## 🎨 How It Works (Visual Flow)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Query    │───▶│  Triage Agent   │───▶│ Escalation Agent│
│ "Urgent issue"  │    │                 │    │                 │
│                 │    │ • Analyzes      │    │ • Handles       │
│                 │    │ • Collects      │    │   escalated     │
│                 │    │   reason        │    │   issues        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │ EscalationData  │
                       │                 │
                       │ reason: "Double │
                       │  charge issue"  │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │ Async Callback  │
                       │                 │
                       │ 🚨 Logs reason  │
                       │ 📊 Updates DB   │
                       │ 🔔 Notifications│
                       └─────────────────┘
```

## 🚀 How to Run

1. **Navigate to the directory**:
   ```bash
   cd openaiagentssdktutorial/openaiagentssdk/17handsoff/3handsoffinputs
   ```

2. **Set up your environment** (if not already done):
   ```bash
   # Create .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   echo "OPENAI_MODEL=gpt-4" >> .env
   ```

3. **Run the example**:
   ```bash
   python 3handsoffinputs.py
   ```

## 📊 Expected Output

When you run this example, you should see something like:

```
🚨 Escalation triggered with reason: Double charge on credit card
🤖 Final Output:
I understand this is a serious issue with a double charge on your credit card. This requires immediate attention from our escalation team.

Let me connect you with our escalation specialist who can help resolve this urgent matter...
```

## 🛠️ Advanced Data Model Examples

### 📋 Complex Customer Data
```python
from pydantic import BaseModel, Field
from typing import Optional, List

class CustomerEscalationData(BaseModel):
    customer_id: Optional[str] = Field(None, description="Customer account ID")
    issue_type: str = Field(..., description="Type of issue (billing, technical, etc.)")
    urgency_level: str = Field(..., description="Low, Medium, High, Critical")
    description: str = Field(..., description="Detailed description of the issue")
    previous_attempts: int = Field(0, description="Number of previous support attempts")
    affected_services: List[str] = Field(default_factory=list, description="Services affected")
    
    class Config:
        schema_extra = {
            "example": {
                "customer_id": "CUST12345",
                "issue_type": "billing",
                "urgency_level": "High",
                "description": "Double charge on subscription",
                "previous_attempts": 2,
                "affected_services": ["premium_subscription"]
            }
        }
```

### 🏥 Medical Triage Data
```python
class MedicalTriageData(BaseModel):
    patient_age: int = Field(..., ge=0, le=120, description="Patient age")
    symptoms: List[str] = Field(..., description="List of symptoms")
    pain_level: int = Field(..., ge=1, le=10, description="Pain level 1-10")
    duration: str = Field(..., description="How long symptoms have been present")
    emergency_contact: Optional[str] = Field(None, description="Emergency contact info")
    allergies: List[str] = Field(default_factory=list, description="Known allergies")
```

### 🏦 Financial Escalation Data
```python
class FinancialEscalationData(BaseModel):
    transaction_id: str = Field(..., description="Transaction identifier")
    amount: float = Field(..., gt=0, description="Transaction amount")
    currency: str = Field(..., description="Currency code")
    issue_category: str = Field(..., description="Fraud, billing, refund, etc.")
    evidence_files: List[str] = Field(default_factory=list, description="File references")
    customer_priority: str = Field(..., description="VIP, regular, etc.")
```

## 🧪 Testing Different Scenarios

### 🔍 Test Data Validation
```python
# This should work - valid data
result = await Runner.run(
    triage_agent,
    input="I need immediate help with a billing issue!"
)

# This should also work - different valid data
result = await Runner.run(
    triage_agent,
    input="There's a technical problem with my account that's urgent!"
)
```

### 🔍 Test Async Callback
```python
# The callback should print the reason
async def test_callback(ctx: RunContextWrapper[None], input_data: EscalationData):
    print(f"🔍 Testing callback with reason: {input_data.reason}")
    print(f"🔍 Full input data: {input_data}")
```

## 🐛 Troubleshooting

### ❌ Data Validation Errors
**Problem**: Handoff fails with validation errors.

**Solutions**:
1. **Check model definition**: Ensure all required fields are defined
2. **Verify data structure**: Make sure the agent provides data in the correct format
3. **Add optional fields**: Use `Optional[type]` for non-required fields
4. **Check field types**: Ensure data types match the model definition

### ❌ Callback Not Receiving Data
**Problem**: Callback runs but doesn't receive the structured data.

**Solutions**:
1. **Check function signature**: Ensure callback takes `input_data: YourModel` parameter
2. **Verify input_type**: Make sure `input_type=YourModel` is set in handoff
3. **Test with print statements**: Add debug prints to see what data is received

### ❌ Agent Not Collecting Data
**Problem**: Triage agent doesn't ask for required information.

**Solutions**:
1. **Update instructions**: Make agent instructions more explicit about data collection
2. **Add examples**: Show the agent what data format is expected
3. **Test with prompts**: Use clear prompts that should trigger data collection

## 📚 Key Takeaways

1. **📋 Structured Data**: Use Pydantic models to define and validate data structure
2. **🔄 Async Callbacks**: Handle complex operations during handoff
3. **✅ Data Validation**: Ensure data integrity and completeness
4. **🎯 Type Safety**: Catch errors early with proper type definitions

## 🎓 Next Steps

Ready to learn even more advanced handoff features? Move on to:
- **[Input Filters](../4inputfilters/)**: Clean and process data before handoff
- **[Recommended Prompt](../5recomendedprompt/)**: Use best practices for reliable handoffs

## 🛠️ Real-World Applications

### 🏢 Customer Support Escalation
```python
class SupportEscalationData(BaseModel):
    ticket_id: str
    customer_tier: str  # bronze, silver, gold, platinum
    issue_complexity: str  # simple, moderate, complex
    escalation_reason: str
    attempted_solutions: List[str]

async def escalate_support(ctx: RunContextWrapper[None], data: SupportEscalationData):
    print(f"📞 Escalating ticket {data.ticket_id} for {data.customer_tier} customer")
    # Could also create JIRA ticket, notify supervisor, etc.
```

### 🏥 Healthcare Triage
```python
class MedicalTriageData(BaseModel):
    patient_id: str
    symptoms: List[str]
    pain_level: int
    vital_signs: dict
    medical_history: str

async def triage_patient(ctx: RunContextWrapper[None], data: MedicalTriageData):
    print(f"🏥 Triage for patient {data.patient_id} with pain level {data.pain_level}")
    # Could also update patient records, alert medical staff, etc.
```

---

**🎉 Fantastic!** You've now learned how to pass structured, validated data between agents during handoff. Your system can now handle complex information transfer with data integrity! 🚀 