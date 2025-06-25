# 🔢 Code Interpreter Tool

## 📋 Overview
This example demonstrates how to use the **CodeInterpreterTool** to enable agents to write, execute, and analyze Python code. The agent can solve mathematical problems, process data, create visualizations, and perform complex computations in a sandboxed environment.

## 🎯 Key Concepts

### **CodeInterpreterTool**
- **Purpose**: Enables agents to write and execute Python code
- **Sandboxed Environment**: Safe execution environment for code
- **Data Analysis**: Process data, create charts, perform calculations
- **Interactive**: Can run multiple code blocks and build on previous results

### **CodeInterpreter**
- **Container Type**: Configurable execution environment
- **Auto Container**: Automatically manages Python environment
- **Package Management**: Can install and use Python packages
- **File Operations**: Read, write, and manipulate files

### **Code Execution Capabilities**
- **Mathematical Operations**: Complex calculations and formulas
- **Data Processing**: CSV, JSON, Excel file handling
- **Visualization**: Create charts, graphs, and plots
- **API Integration**: Make HTTP requests and process responses
- **File I/O**: Read and write files in the sandbox

## 📁 Code Structure

```python
import asyncio
from agents import Agent, Runner, set_default_openai_key
from agents.tool import CodeInterpreterTool, CodeInterpreter
from dotenv import load_dotenv
import os

# Environment setup
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
model = os.environ.get("OPENAI_MODEL")

# Define the agent with the code interpreter tool
agent = Agent(
    name="Code Genius",
    instructions="You can write and execute Python code to solve problems.",
    tools=[
        CodeInterpreterTool(CodeInterpreter(
            type='code_interpreter', 
            container={'type': 'auto'}
        )),
    ],
    model=model
)

# Main execution
async def main():
    result = await Runner.run(
        agent,
        input="Write Python code to calculate the sum of numbers from 1 to 100 and explain the result."
    )
    print("🔢 Final Output:\n", result.final_output)
```

## 🔧 Configuration Options

### **CodeInterpreterTool Setup**
```python
# Basic configuration
CodeInterpreterTool(CodeInterpreter(type='code_interpreter'))

# With custom container settings
CodeInterpreterTool(CodeInterpreter(
    type='code_interpreter',
    container={
        'type': 'auto',  # or 'custom'
        'python_version': '3.9',  # Specify Python version
        'packages': ['pandas', 'matplotlib', 'numpy']  # Pre-install packages
    }
))
```

### **Container Types**
```python
# Auto container (recommended)
container={'type': 'auto'}

# Custom container with specific settings
container={
    'type': 'custom',
    'image': 'python:3.9-slim',
    'requirements': ['pandas', 'numpy', 'matplotlib']
}
```

## 🚀 Usage

### **Basic Usage**
```bash
uv run 4codeinterpreter.py
```

### **Example Tasks**
- "Write Python code to calculate the sum of numbers from 1 to 100"
- "Create a bar chart of sales data for the last 6 months"
- "Analyze this CSV file and find the average values"
- "Write a function to calculate Fibonacci numbers"
- "Process this JSON data and extract specific information"

## 🛠️ Customization Ideas

### **1. Specialized Code Agents**
```python
# Data analysis agent
data_agent = Agent(
    name="Data Analyst",
    instructions="You are a data analyst. Write code to analyze and visualize data.",
    tools=[CodeInterpreterTool(CodeInterpreter(type='code_interpreter'))],
    model=model
)

# Mathematical computation agent
math_agent = Agent(
    name="Math Solver",
    instructions="You are a mathematical assistant. Solve complex equations and problems.",
    tools=[CodeInterpreterTool(CodeInterpreter(type='code_interpreter'))],
    model=model
)
```

### **2. Pre-configured Packages**
```python
# Agent with specific packages for data science
data_science_tool = CodeInterpreterTool(CodeInterpreter(
    type='code_interpreter',
    container={
        'type': 'auto',
        'packages': [
            'pandas', 'numpy', 'matplotlib', 'seaborn',
            'scikit-learn', 'plotly', 'jupyter'
        ]
    }
))
```

### **3. Custom Code Templates**
```python
# Agent with specific coding style
code_agent = Agent(
    name="Python Developer",
    instructions="""
    You are a Python developer. Write clean, well-documented code.
    Always include:
    - Clear variable names
    - Comments explaining complex logic
    - Error handling where appropriate
    - Type hints when possible
    """,
    tools=[CodeInterpreterTool(CodeInterpreter(type='code_interpreter'))],
    model=model
)
```

## 🔍 How It Works

### **Code Execution Flow**
1. **Task Analysis**: Agent receives coding task
2. **Code Generation**: Agent writes appropriate Python code
3. **Environment Setup**: CodeInterpreter prepares execution environment
4. **Code Execution**: Python code runs in sandboxed container
5. **Result Processing**: Output is captured and returned
6. **Iteration**: Agent can run additional code based on results

### **Supported Operations**
```python
# Mathematical operations
result = 2 + 2 * 3

# Data processing
import pandas as pd
df = pd.read_csv('data.csv')
summary = df.describe()

# Visualization
import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
plt.show()

# File operations
with open('output.txt', 'w') as f:
    f.write('Hello, World!')

# API requests
import requests
response = requests.get('https://api.example.com/data')
```

## 📊 Code Capabilities

### **Mathematical Operations**
- **Basic Math**: Addition, subtraction, multiplication, division
- **Advanced Math**: Logarithms, trigonometry, calculus
- **Statistics**: Mean, median, standard deviation, correlations
- **Linear Algebra**: Matrix operations, eigenvalues, eigenvectors

### **Data Processing**
- **CSV Files**: Read, write, analyze tabular data
- **JSON Data**: Parse and manipulate structured data
- **Excel Files**: Handle spreadsheet data
- **Text Processing**: String manipulation, regex, NLP

### **Visualization**
- **Charts**: Bar charts, line plots, scatter plots
- **Graphs**: Histograms, box plots, heatmaps
- **Interactive**: Plotly charts, dynamic visualizations
- **Custom**: Custom matplotlib/seaborn plots

### **File Operations**
- **Reading**: Open and read various file formats
- **Writing**: Create and write to files
- **Processing**: Transform and analyze file contents
- **Export**: Save results in different formats

## ⚠️ Important Notes

### **Prerequisites**
- **OpenAI API Key**: Valid API key with code interpreter access
- **Model Support**: Ensure model supports code interpretation
- **Container Access**: Internet access for package installation

### **Security Considerations**
- **Sandboxed Environment**: Code runs in isolated container
- **No System Access**: Cannot access host file system
- **Time Limits**: Code execution has time constraints
- **Memory Limits**: Limited memory allocation per execution

### **Performance**
- **Startup Time**: Container initialization takes 10-30 seconds
- **Package Installation**: First-time package installs add delay
- **Code Execution**: Simple operations are fast, complex ones slower
- **Memory Usage**: Each container uses significant memory

## 🐛 Troubleshooting

### **Common Issues**

1. **"Code interpreter not available"**
   - Check API key has code interpreter access
   - Verify model supports code interpretation
   - Ensure account has necessary permissions

2. **"Package not found"**
   - Install required packages in code
   - Use `pip install package_name` in code block
   - Check package name spelling

3. **"Code execution failed"**
   - Check Python syntax errors
   - Verify imports are correct
   - Ensure code is complete and runnable

4. **"Timeout error"**
   - Break complex operations into smaller parts
   - Optimize code for faster execution
   - Use simpler algorithms for large datasets

### **Debug Mode**
```python
# Enable detailed logging
import logging
logging.getLogger("openai.agents").setLevel(logging.DEBUG)

# Test simple code first
result = await Runner.run(agent, "Print 'Hello, World!'")
```

## 🔗 Related Examples

- **ComputerTool**: Control web browsers and applications
- **LocalShellTool**: Execute system commands
- **CustomFunctionTool**: Create custom Python functions

## 📚 Best Practices

1. **Start Simple**: Begin with basic calculations
2. **Test Incrementally**: Build complex solutions step by step
3. **Handle Errors**: Include try-catch blocks for robustness
4. **Document Code**: Add comments explaining complex logic
5. **Optimize Performance**: Use efficient algorithms and data structures

## 🎓 Learning Path

1. **Basic Operations**: Learn simple calculations and data types
2. **Data Processing**: Work with CSV, JSON, and other formats
3. **Visualization**: Create charts and graphs
4. **Advanced Analysis**: Statistical analysis and machine learning
5. **Custom Applications**: Build specialized code solutions

## 🌟 Advanced Use Cases

### **Data Analysis Pipeline**
```python
# Complete data analysis workflow
result = await Runner.run(agent, """
    Read the sales_data.csv file, clean the data, 
    calculate monthly totals, create a line chart,
    and provide insights about trends
""")
```

### **Machine Learning**
```python
# Simple ML model training
result = await Runner.run(agent, """
    Load the iris dataset, split into train/test sets,
    train a simple classifier, and show accuracy metrics
""")
```

### **API Integration**
```python
# Fetch and process external data
result = await Runner.run(agent, """
    Fetch weather data from an API, process the JSON response,
    create a temperature chart, and calculate averages
""")
```

---

*This example demonstrates the power of AI agents writing and executing code, enabling them to solve complex computational problems, analyze data, and create visualizations in a safe, sandboxed environment.* 