#!/bin/sh

echo "Setting up Agent Dojo MCP Server..." >&2

echo "Installing dependencies..." >&2
uv sync > /dev/null 2>&1

echo "Installing agent_dojo_mcp package..." >&2
uv pip install -e . > /dev/null 2>&1

echo "Setup complete!" >&2

cat << EOF
{
  "command": "uv",
  "args": ["run", "agent-dojo-mcp"],
  "env": {},
  "cwd": "$(pwd)"
}
EOF
