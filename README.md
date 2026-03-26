# Agent Dojo MCP Server

MCP (Model Context Protocol) server that gives AI agents access to expert knowledge from 1000+ curated development talks, powered by RAG + Knowledge Graph.

## Tools

### `ask_dojo`
Ask technical questions and get comprehensive, expert-grade answers grounded in real-world production knowledge.

**Parameters:**
- `question` (required) - The technical question to ask
- `dojo` (optional) - Knowledge domain: `devbot` (software engineering) or `openclaw` (OpenClaw framework). Default: `devbot`
- `model` (optional) - LLM model: `gpt-5.4`, `claude-sonnet-4.6`, `claude-opus-4.6`, `gemini-3-pro`, etc. Default: `gpt-5.4`

### `list_dojos`
Discover available knowledge domains, their statistics, and suggested questions.

### `search_knowledge`
Search and browse the raw knowledge base — useful for exploring available content by topic, technology, or dimension.

**Parameters:**
- `query` (required) - Search query
- `dojo` (optional) - Knowledge domain. Default: `devbot`
- `dimension` (optional) - Filter by dimension (e.g. `best_practice`, `anti_pattern`, `production_lesson`)
- `limit` (optional) - Max results (1-50). Default: 20

## Setup

### Environment Variable
```
AGENT_DOJO_API_URL=https://your-agent-dojo-api-url.com
```

### Run with uv
```bash
uv sync
uv run agent-dojo-mcp
```

### Cursor / Claude Desktop Config
```json
{
  "mcpServers": {
    "agent-dojo": {
      "command": "uv",
      "args": ["run", "agent-dojo-mcp"],
      "env": {
        "AGENT_DOJO_API_URL": "https://your-agent-dojo-api-url.com"
      }
    }
  }
}
```

## Publishing to MCP Hive

Automated via GitHub Actions on push to `main`. Requires secrets:
- `MCP_HIVE_API_KEY` - MCP Hive API key
- `MCP_HIVE_ID` - Hive instance ID (obtained after first publish)
