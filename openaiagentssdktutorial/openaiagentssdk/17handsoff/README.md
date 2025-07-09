# 🤝 Agent Handoff Tutorial

## 📋 Overview

Welcome to the **Agent Handoff** tutorial! This section teaches you how to create intelligent systems where one agent can automatically delegate tasks to specialized agents. Think of it like a smart receptionist who knows exactly which expert to connect you with based on your needs.

## 🎯 What is Agent Handoff?

Agent handoff is a powerful feature that allows you to build **modular, scalable AI systems** where:

- **One main agent** (like a triage agent) receives user queries
- **Specialized agents** handle specific types of requests
- **Automatic routing** ensures users get the right expert for their needs

### 🏥 Real-World Analogy

Imagine a hospital emergency room:
- **Triage Nurse** (Main Agent): Assesses patients and decides which specialist they need
- **Cardiologist** (Specialized Agent): Handles heart-related issues
- **Orthopedist** (Specialized Agent): Handles bone and joint problems
- **Neurologist** (Specialized Agent): Handles brain and nervous system issues

The triage nurse doesn't treat patients directly but ensures they see the right specialist!

## 🗂️ Tutorial Structure

This tutorial is organized into 5 progressive examples, each building on the previous one:

### 📁 1. [Basic Handoff](./1basichandsoff/)
**🎯 Goal**: Learn the fundamentals of agent handoff
- Create specialized agents (billing, refund)
- Set up a triage agent that routes queries
- Understand basic handoff syntax

### 📁 2. [Customizing Handoff](./2customizinghandsoff/)
**🎯 Goal**: Add custom behavior to handoffs
- Use callbacks to run custom code during handoff
- Customize tool names and descriptions
- Add logging and monitoring

### 📁 3. [Handoff Inputs](./3handsoffinputs/)
**🎯 Goal**: Pass structured data between agents
- Use Pydantic models for data validation
- Pass complex information during handoff
- Handle async callbacks with structured data

### 📁 4. [Input Filters](./4inputfilters/)
**🎯 Goal**: Clean and process data before handoff
- Filter out irrelevant information
- Sanitize sensitive data
- Preprocess input for specialized agents

### 📁 5. [Recommended Prompt](./5recomendedprompt/)
**🎯 Goal**: Use best practices for reliable handoffs
- Implement recommended prompt prefixes
- Ensure consistent handoff behavior
- Follow prompt engineering best practices

## 🚀 Quick Start

To get started with agent handoff:

1. **Set up your environment**:
   ```bash
   # Make sure you have the required dependencies
   pip install openai-agents-sdk pydantic python-dotenv
   ```

2. **Configure your API key**:
   ```bash
   # Create a .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   echo "OPENAI_MODEL=gpt-4" >> .env
   ```

3. **Start with the basic example**:
   ```bash
   cd 1basichandsoff
   python 1basichandsoff.py
   ```

## 🎨 Key Concepts Visualized

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Query    │───▶│  Triage Agent   │───▶│ Specialized     │
│                 │    │                 │    │ Agent           │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Handoff Logic  │
                       │                 │
                       │ • Callbacks     │
                       │ • Input Filters │
                       │ • Data Validation│
                       └─────────────────┘
```

## 🔧 Common Use Cases

### 🏢 Customer Support
- **General Support Agent** → Routes to billing, technical, or refund specialists
- **Escalation System** → Automatically escalates urgent issues to supervisors

### 🏥 Healthcare
- **Triage Bot** → Routes patients to appropriate medical specialists
- **Symptom Checker** → Directs to relevant health information

### 🏦 Banking
- **Account Assistant** → Routes to loan, investment, or fraud specialists
- **Transaction Support** → Directs to appropriate financial advisors

### 🎓 Education
- **Student Advisor** → Routes to academic, financial aid, or career counselors
- **Course Assistant** → Directs to subject-specific tutors

## 🛠️ Advanced Features

As you progress through the examples, you'll learn about:

- **🔄 Callbacks**: Run custom code when handoffs occur
- **📊 Structured Data**: Pass validated information between agents
- **🧹 Input Filtering**: Clean and process data before handoff
- **🎯 Prompt Engineering**: Use best practices for reliable routing
- **⚡ Async Operations**: Handle complex workflows efficiently

## 🐛 Troubleshooting

### Common Issues

1. **Agent not delegating properly**
   - Check the triage agent's instructions
   - Ensure handoff tools are properly configured
   - Verify the specialized agent's instructions are clear

2. **Handoff not triggering**
   - Review the prompt prefix usage
   - Check if the query matches the routing criteria
   - Verify API keys and model configuration

3. **Data validation errors**
   - Check Pydantic model definitions
   - Ensure input data matches expected schema
   - Review callback function signatures

## 📚 Best Practices

1. **🎯 Clear Instructions**: Make triage agent instructions explicit about when to handoff
2. **🔍 Test Thoroughly**: Try various query types to ensure proper routing
3. **📝 Document Handoffs**: Keep track of which agents handle what types of queries
4. **🛡️ Validate Input**: Use structured data and validation for complex handoffs
5. **📊 Monitor Performance**: Use callbacks to track handoff patterns and success rates

## 🎓 Next Steps

After completing this tutorial, you'll be ready to:

- Build complex multi-agent systems
- Implement intelligent routing in your applications
- Create scalable customer support systems
- Design modular AI architectures

## 📖 Additional Resources

- [OpenAI Agents SDK Documentation](https://docs.openai.com/agents-sdk)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Agent Handoff Best Practices](./5recomendedprompt/)

---

**Ready to start?** Begin with the [Basic Handoff](./1basichandsoff/) example to learn the fundamentals! 🚀 