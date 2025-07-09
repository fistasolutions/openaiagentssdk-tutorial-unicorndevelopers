# 🧹 Handoff Input Filters Example

## 📋 Overview

Welcome to the **Input Filters** tutorial! Now you'll learn how to clean, sanitize, and preprocess data before it reaches your specialized agents. This is like having a filter system that removes impurities from water before it reaches your coffee machine - ensuring only clean, relevant information gets through.

## 🎯 What You'll Learn

By the end of this example, you'll understand:
- ✅ How to use built-in input filters to clean data
- ✅ How to remove irrelevant information before handoff
- ✅ How to sanitize sensitive data for security
- ✅ How to preprocess input for specialized agents

## 🧽 Real-World Analogy

Think of a document processing system:
- **Raw Document** (User Input): Contains text, formatting, metadata, and irrelevant information
- **Document Filter** (Input Filter): Removes formatting, extracts relevant text, removes sensitive data
- **Clean Document** (Filtered Input): Contains only the essential information needed
- **Specialist** (Handoff Agent): Receives clean, focused information to work with

## 📁 Code Walkthrough

Let's break down the code step by step:

### 🔧 Step 1: Import Required Libraries
```python
import os
from dotenv import load_dotenv
from agents import Agent, Runner, handoff, set_default_openai_key
from agents.extensions import handoff_filters
```

**What this does:**
- `handoff_filters`: Provides built-in filter functions for cleaning data
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

### 🎯 Step 3: Create the FAQ Agent
```python
# 🎯 FAQ Agent (receives handoff)
faq_agent = Agent(
    name="FAQ Agent",
    instructions="You answer frequently asked questions clearly and concisely.",
    model=openai_model
)
```

**What this does:**
- Creates a specialized agent for handling FAQ queries
- This agent expects clean, focused questions

### 🧹 Step 4: Create Handoff with Input Filter
```python
# 🧹 Handoff with input filter to remove tool calls
faq_handoff = handoff(
    agent=faq_agent,
    input_filter=handoff_filters.remove_all_tools
)
```

**What this does:**
- `agent=faq_agent`: Specifies the target agent
- `input_filter=handoff_filters.remove_all_tools`: Applies a filter to clean the input
- The filter removes any tool calls or function calls from the input

### 🧠 Step 5: Create the Triage Agent
```python
# 🧠 Main agent (performs handoff)
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You handle general customer queries. "
        "If the user is asking a standard FAQ, use the FAQ handoff tool to pass it along."
    ),
    model=openai_model,
    handoffs=[faq_handoff],
)
```

**What this does:**
- Creates the main agent that receives all customer queries
- Instructions tell it to route FAQ questions to the specialized agent
- The handoff will automatically clean the input before passing it

### 🚀 Step 6: Test the System
```python
# 🚀 Run a sample query
result = Runner.run_sync(triage_agent, "What is your refund policy?")

# 🖨️ Output
print("🤖 Final Output:\n", result.final_output)
```

## 🎨 How It Works (Visual Flow)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Raw Input     │───▶│  Input Filter   │───▶│  Clean Input    │
│                 │    │                 │    │                 │
│ • User query    │    │ • Removes tools │    │ • Clean text    │
│ • Tool calls    │    │ • Sanitizes     │    │ • Relevant info │
│ • Metadata      │    │ • Preprocesses  │    │ • Focused query │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  FAQ Agent      │
                       │                 │
                       │ • Receives clean│
                       │   input         │
                       │ • Provides      │
                       │   focused answer│
                       └─────────────────┘
```

## 🚀 How to Run

1. **Navigate to the directory**:
   ```bash
   cd openaiagentssdktutorial/openaiagentssdk/17handsoff/4inputfilters
   ```

2. **Set up your environment** (if not already done):
   ```bash
   # Create .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   echo "OPENAI_MODEL=gpt-4" >> .env
   ```

3. **Run the example**:
   ```bash
   python 4inputfilters.py
   ```

## 📊 Expected Output

When you run this example, you should see something like:

```
🤖 Final Output:
Our refund policy allows returns within 30 days of purchase for most items. Here are the key points:

• Return window: 30 days from purchase date
• Condition: Items must be unused and in original packaging
• Process: Contact customer service to initiate return
• Refund method: Original payment method
• Processing time: 5-7 business days

For specific items or exclusions, please check the product page or contact our support team.
```

## 🛠️ Built-in Filter Examples

### 🧹 Remove All Tools
```python
# Removes any tool calls or function calls from input
faq_handoff = handoff(
    agent=faq_agent,
    input_filter=handoff_filters.remove_all_tools
)
```

### 📝 Remove Tool Calls Only
```python
# Removes only tool calls, keeps other content
support_handoff = handoff(
    agent=support_agent,
    input_filter=handoff_filters.remove_tool_calls
)
```

### 🔒 Remove Function Calls Only
```python
# Removes only function calls, keeps other content
billing_handoff = handoff(
    agent=billing_agent,
    input_filter=handoff_filters.remove_function_calls
)
```

## 🛠️ Custom Filter Examples

### 🎯 Custom Text Filter
```python
def custom_text_filter(input_text: str) -> str:
    """Remove sensitive information and clean text."""
    # Remove email addresses
    import re
    cleaned = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', input_text)
    
    # Remove phone numbers
    cleaned = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', cleaned)
    
    # Remove credit card numbers
    cleaned = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '[CARD]', cleaned)
    
    return cleaned

secure_handoff = handoff(
    agent=secure_agent,
    input_filter=custom_text_filter
)
```

### 📊 Data Preprocessing Filter
```python
def preprocess_for_analysis(input_text: str) -> str:
    """Prepare text for data analysis agent."""
    # Convert to lowercase
    cleaned = input_text.lower()
    
    # Remove extra whitespace
    cleaned = ' '.join(cleaned.split())
    
    # Remove common stop words (simplified)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    words = cleaned.split()
    filtered_words = [word for word in words if word not in stop_words]
    
    return ' '.join(filtered_words)

analysis_handoff = handoff(
    agent=analysis_agent,
    input_filter=preprocess_for_analysis
)
```

### 🎭 Context-Aware Filter
```python
def context_filter(input_text: str) -> str:
    """Filter based on context and agent type."""
    # For FAQ agent, focus on the core question
    if "what is" in input_text.lower() or "how do" in input_text.lower():
        # Extract the main question
        lines = input_text.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('```'):
                return line.strip()
    
    return input_text

smart_faq_handoff = handoff(
    agent=faq_agent,
    input_filter=context_filter
)
```

## 🧪 Testing Different Scenarios

### 🔍 Test Tool Removal
```python
# Input with tool calls should be cleaned
result = await Runner.run(
    triage_agent,
    input="What is your refund policy? I need to use the refund_tool to process this."
)
```

### 🔍 Test Sensitive Data Removal
```python
# Input with sensitive data should be sanitized
result = await Runner.run(
    triage_agent,
    input="My email is john.doe@example.com and my card is 1234-5678-9012-3456"
)
```

### 🔍 Test Complex Input
```python
# Complex input should be simplified
result = await Runner.run(
    triage_agent,
    input="""
    I have a question about your refund policy.
    
    Here are some details:
    - Order ID: 12345
    - Purchase date: 2024-01-15
    - Amount: $99.99
    
    What is your refund policy?
    """
)
```

## 🐛 Troubleshooting

### ❌ Filter Not Working
**Problem**: Input is not being filtered as expected.

**Solutions**:
1. **Check filter function**: Ensure the filter function is properly defined
2. **Verify handoff setup**: Make sure `input_filter=your_filter` is set correctly
3. **Test filter directly**: Test the filter function with sample input
4. **Check filter logic**: Review the filter logic for bugs

### ❌ Data Loss
**Problem**: Important information is being removed by the filter.

**Solutions**:
1. **Review filter logic**: Check what the filter is removing
2. **Adjust filter rules**: Modify the filter to preserve important data
3. **Test with various inputs**: Try different input types to ensure nothing important is lost
4. **Add logging**: Log what the filter is doing for debugging

### ❌ Performance Issues
**Problem**: Filter is slowing down the handoff process.

**Solutions**:
1. **Optimize filter logic**: Simplify complex filtering operations
2. **Use built-in filters**: Built-in filters are optimized for performance
3. **Cache results**: For expensive operations, consider caching
4. **Profile the filter**: Identify bottlenecks in the filtering process

## 📚 Key Takeaways

1. **🧹 Data Cleaning**: Remove irrelevant or sensitive information before handoff
2. **🔒 Security**: Sanitize data to protect sensitive information
3. **🎯 Focus**: Ensure specialized agents receive only relevant information
4. **⚡ Performance**: Use built-in filters for optimal performance

## 🎓 Next Steps

Ready to learn the final handoff best practices? Move on to:
- **[Recommended Prompt](../5recomendedprompt/)**: Use best practices for reliable handoffs

## 🛠️ Real-World Applications

### 🏢 Customer Support Filtering
```python
def support_filter(input_text: str) -> str:
    """Filter customer support queries."""
    # Remove internal notes and metadata
    lines = input_text.split('\n')
    filtered_lines = []
    
    for line in lines:
        # Skip internal notes (marked with [INTERNAL])
        if '[INTERNAL]' not in line:
            # Remove customer ID references
            line = re.sub(r'Customer ID: \d+', '', line)
            filtered_lines.append(line)
    
    return '\n'.join(filtered_lines)

support_handoff = handoff(
    agent=support_agent,
    input_filter=support_filter
)
```

### 🏥 Medical Data Filtering
```python
def medical_filter(input_text: str) -> str:
    """Filter medical queries for privacy."""
    # Remove patient identifiers
    cleaned = re.sub(r'Patient ID: \w+', '[PATIENT_ID]', input_text)
    cleaned = re.sub(r'DOB: \d{2}/\d{2}/\d{4}', '[DOB]', cleaned)
    cleaned = re.sub(r'SSN: \d{3}-\d{2}-\d{4}', '[SSN]', cleaned)
    
    return cleaned

medical_handoff = handoff(
    agent=medical_agent,
    input_filter=medical_filter
)
```

### 🏦 Financial Data Filtering
```python
def financial_filter(input_text: str) -> str:
    """Filter financial queries for security."""
    # Remove account numbers
    cleaned = re.sub(r'Account: \d{10}', '[ACCOUNT]', input_text)
    # Remove amounts (keep context)
    cleaned = re.sub(r'\$[\d,]+\.\d{2}', '[AMOUNT]', cleaned)
    # Remove routing numbers
    cleaned = re.sub(r'Routing: \d{9}', '[ROUTING]', cleaned)
    
    return cleaned

financial_handoff = handoff(
    agent=financial_agent,
    input_filter=financial_filter
)
```

---

**🎉 Excellent!** You've now learned how to use input filters to clean and preprocess data before handoff. Your system can now ensure that specialized agents receive only the information they need! 🚀 