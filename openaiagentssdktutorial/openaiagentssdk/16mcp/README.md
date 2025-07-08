# MCP Basic Demo

This is a basic demonstration of the Model Context Protocol (MCP) using the OpenAI Agents SDK.

## What it does

The demo shows how an AI agent can:
1. Connect to an MCP filesystem server
2. Read files from a controlled directory
3. Process and summarize file contents
4. Provide helpful responses based on the files

## Setup

### 1. Install Dependencies

The project uses `uv` for dependency management. Make sure you have the required packages:

```bash
cd openaiagentssdktutorial
uv sync
```

### 2. Set up Environment Variables

Create a `.env` file in the `openaiagentssdktutorial` directory with your OpenAI API key:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

**Important:** Replace `sk-your-actual-openai-api-key-here` with your real OpenAI API key from https://platform.openai.com/account/api-keys

### 3. Sample Files

The demo includes a `sample_files` directory with a `demo.txt` file. You can add more `.txt` files to this directory for the agent to read.

## Running the Demo

From the `openaiagentssdktutorial` directory:

```bash
cd openaiagentssdk/16mcp
uv run python mcpbasic.py
```

## Expected Output

When you run the script with a valid API key, you should see:

```
Secure MCP Filesystem Server running on stdio
Allowed directories: [...]
Running: Please read the content of 'demo.txt' and summarize it.

🧠 Final Output:
[AI agent's summary of the demo.txt file content]
```

## How it Works

1. **MCP Server**: The script starts an MCP filesystem server using `npx @modelcontextprotocol/server-filesystem`
2. **Agent Creation**: Creates an AI agent with access to the MCP server's tools
3. **File Reading**: The agent uses MCP tools to read files from the `sample_files` directory
4. **Processing**: The agent processes the file content and provides a summary

## Troubleshooting

- **"Incorrect API key" error**: Make sure you've set a valid OpenAI API key in your `.env` file
- **"npx not found" error**: Install Node.js and npm, which includes npx
- **Permission errors**: The MCP server only has access to the `sample_files` directory for security

## Files Structure

```
16mcp/
├── mcpbasic.py          # Main demo script
├── sample_files/        # Directory with files for the agent to read
│   └── demo.txt         # Sample file with MCP information
└── README.md           # This file
``` 