# 💻 Computer Tool (Browser Automation)

## 📋 Overview
This example demonstrates how to use the **ComputerTool** to enable agents to control web browsers and interact with web applications. The agent can navigate websites, click elements, type text, and perform complex web automation tasks using Playwright.

## 🎯 Key Concepts

### **ComputerTool**
- **Purpose**: Enables agents to control web browsers and interact with web applications
- **Browser Automation**: Uses Playwright for reliable web automation
- **Visual Interface**: Agents can see and interact with web pages visually
- **Real-time Control**: Direct mouse, keyboard, and browser control

### **AsyncComputer Interface**
- **Screenshot**: Capture browser viewport images
- **Mouse Control**: Click, double-click, drag, scroll, move
- **Keyboard Input**: Type text and key combinations
- **Browser Management**: Navigate, wait, handle browser lifecycle

### **Playwright Integration**
- **Headless/Headed**: Can run with or without visible browser
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Multiple Browsers**: Supports Chromium, Firefox, WebKit
- **Reliable Automation**: Handles dynamic content and modern web apps

## 📁 Code Structure

```python
import asyncio
import base64
from typing import Literal, Union
import os
from dotenv import load_dotenv
from playwright.async_api import Browser, Page, Playwright, async_playwright

from agents import (
    Agent, AsyncComputer, Button, ComputerTool, Environment,
    ModelSettings, Runner, trace, set_default_openai_key
)

# Environment setup
load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
model = os.environ.get("OPENAI_MODEL")

# Main execution with computer tool
async def main():
    async with LocalPlaywrightComputer() as computer:
        with trace("Computer use example"):
            agent = Agent(
                name="Browser user",
                instructions="You are a helpful agent.",
                tools=[ComputerTool(computer)],
                model="computer-use-preview-2025-03-11",  # Special model for computer use
                model_settings=ModelSettings(truncation="auto"),
            )
            result = await Runner.run(agent, "Search for SF sports news and summarize.")
            print(result.final_output)
```

## 🔧 Configuration Options

### **ComputerTool Setup**
```python
# Basic computer tool configuration
ComputerTool(computer)

# With custom settings
ComputerTool(
    computer=computer,
    max_screenshot_size=1024,  # Max screenshot dimensions
    screenshot_format="png"    # Image format
)
```

### **Model Configuration**
```python
# Required model for computer use
model="computer-use-preview-2025-03-11"

# Model settings for computer interaction
model_settings=ModelSettings(
    truncation="auto",  # Required for computer use
    temperature=0.7     # Optional: control creativity
)
```

## 🚀 Usage

### **Basic Usage**
```bash
uv run 3computertool.py
```

### **Prerequisites**
```bash
# Install Playwright browsers
playwright install chromium
```

### **Example Tasks**
- "Search for SF sports news and summarize"
- "Go to weather.com and check the forecast"
- "Navigate to GitHub and search for Python projects"
- "Visit a news website and read the latest headlines"

## 🛠️ Customization Ideas

### **1. Custom Browser Configuration**
```python
class CustomPlaywrightComputer(LocalPlaywrightComputer):
    async def _get_browser_and_page(self) -> tuple[Browser, Page]:
        width, height = 1920, 1080  # Full HD
        launch_args = [
            f"--window-size={width},{height}",
            "--disable-web-security",  # Custom arguments
            "--no-sandbox"
        ]
        browser = await self.playwright.chromium.launch(
            headless=False, 
            args=launch_args
        )
        page = await browser.new_page()
        await page.set_viewport_size({"width": width, "height": height})
        await page.goto("https://www.google.com")
        return browser, page
```

### **2. Different Browser Engines**
```python
# Use Firefox instead of Chromium
browser = await self.playwright.firefox.launch(headless=False)

# Use WebKit (Safari engine)
browser = await self.playwright.webkit.launch(headless=False)
```

### **3. Custom Starting Page**
```python
# Start with a specific website
await page.goto("https://www.example.com")

# Start with multiple tabs
page1 = await browser.new_page()
page2 = await browser.new_page()
await page1.goto("https://www.google.com")
await page2.goto("https://www.github.com")
```

## 🔍 How It Works

### **Computer Control Flow**
1. **Agent Analysis**: Agent receives task and analyzes requirements
2. **Browser Launch**: Playwright starts browser instance
3. **Visual Processing**: Agent sees screenshots of web pages
4. **Action Planning**: Agent decides what actions to take
5. **Execution**: ComputerTool executes mouse/keyboard actions
6. **Feedback Loop**: Process repeats until task completion

### **Key Methods**
```python
# Screenshot capture
async def screenshot(self) -> str:
    png_bytes = await self.page.screenshot(full_page=False)
    return base64.b64encode(png_bytes).decode("utf-8")

# Mouse actions
async def click(self, x: int, y: int, button: Button = "left") -> None:
    await self.page.mouse.click(x, y, button=button)

# Keyboard input
async def type(self, text: str) -> None:
    await self.page.keyboard.type(text)

# Scrolling
async def scroll(self, x: int, y: int, scroll_x: int, scroll_y: int) -> None:
    await self.page.mouse.move(x, y)
    await self.page.evaluate(f"window.scrollBy({scroll_x}, {scroll_y})")
```

## 📊 Browser Capabilities

### **Supported Actions**
- **Navigation**: Go to URLs, back/forward, refresh
- **Mouse**: Click, double-click, right-click, drag, scroll
- **Keyboard**: Type text, key combinations, shortcuts
- **Screenshots**: Capture viewport or full page
- **Waiting**: Wait for elements, time delays
- **Form Interaction**: Fill forms, submit, select options

### **Web Element Interaction**
- **Buttons**: Click buttons and links
- **Forms**: Fill input fields, select dropdowns
- **Navigation**: Use menus, breadcrumbs, pagination
- **Content**: Read text, extract information
- **Media**: Handle images, videos, downloads

## ⚠️ Important Notes

### **Prerequisites**
- **Playwright Installation**: `pip install playwright`
- **Browser Installation**: `playwright install chromium`
- **Computer-Use Model**: Requires special model for visual understanding
- **System Resources**: Browser automation uses significant memory/CPU

### **Security Considerations**
- **Sandboxed Environment**: Runs in isolated browser context
- **No File System Access**: Limited to web interactions
- **Session Isolation**: Each run starts fresh browser session
- **Network Security**: Respects browser security policies

### **Performance**
- **Memory Usage**: Each browser instance uses ~100-200MB RAM
- **Startup Time**: Browser launch takes 2-5 seconds
- **Screenshot Processing**: Image encoding/decoding overhead
- **Network Dependencies**: Requires internet for web access

## 🐛 Troubleshooting

### **Common Issues**

1. **"Playwright not installed"**
   ```bash
   pip install playwright
   playwright install chromium
   ```

2. **"Model not found"**
   - Ensure using `computer-use-preview-2025-03-11` model
   - Check API key has access to computer-use models

3. **"Browser won't start"**
   - Check system has enough memory
   - Verify no other browser instances running
   - Try running in headless mode

4. **"Actions not working"**
   - Check website structure hasn't changed
   - Verify elements are visible and clickable
   - Add wait times for dynamic content

### **Debug Mode**
```python
# Enable verbose logging
import logging
logging.getLogger("openai.agents").setLevel(logging.DEBUG)
logging.getLogger("openai.agents").addHandler(logging.StreamHandler())

# Run in headless mode for debugging
browser = await self.playwright.chromium.launch(headless=True)
```

## 🔗 Related Examples

- **WebSearchTool**: Search web without browser control
- **CodeInterpreterTool**: Process data and run code
- **LocalShellTool**: Execute system commands

## 📚 Best Practices

1. **Start Simple**: Begin with basic navigation tasks
2. **Add Waits**: Include delays for dynamic content
3. **Error Handling**: Implement fallbacks for failed actions
4. **Resource Management**: Always close browser instances
5. **Testing**: Test on different websites and scenarios

## 🎓 Learning Path

1. **Basic Navigation**: Learn to navigate websites
2. **Form Interaction**: Fill forms and submit data
3. **Content Extraction**: Read and process web content
4. **Complex Workflows**: Multi-step automation tasks
5. **Advanced Features**: Custom browser configurations

## 🌟 Advanced Use Cases

### **E-commerce Automation**
```python
# Automated shopping assistant
result = await Runner.run(agent, """
    Go to Amazon.com, search for 'wireless headphones', 
    sort by price, and show me the top 3 options under $50
""")
```

### **Data Collection**
```python
# Web scraping with visual understanding
result = await Runner.run(agent, """
    Visit the news website, find the latest technology articles,
    and extract the headlines and publication dates
""")
```

### **Testing Automation**
```python
# Automated web testing
result = await Runner.run(agent, """
    Test the login form: enter invalid credentials,
    verify error message appears, then try valid login
""")
```

---

*This example demonstrates the power of AI agents controlling web browsers, enabling them to interact with web applications just like humans do, opening up possibilities for automated web testing, data collection, and complex web workflows.* 