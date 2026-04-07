"""Agent Dojo MCP Server - expert knowledge via RAG + Knowledge Graph."""

import os
import json
import logging
from typing import Any

import httpx
from mcp.server import FastMCP

logger = logging.getLogger("agent-dojo-mcp")
logging.basicConfig(level=logging.INFO, format="%(name)s - %(message)s")

DEFAULT_API_URL = "https://zbjffcjzsnhqay2c5ckc7damky0tvotz.lambda-url.us-east-1.on.aws"
API_URL = os.environ.get("AGENT_DOJO_API_URL", DEFAULT_API_URL).rstrip("/")

mcp = FastMCP(
    "agent-dojo-mcp",
    instructions=(
        "Expert knowledge from 1000+ curated development talks. "
        "Ask technical questions and get answers powered by RAG + Knowledge Graph, "
        "grounded in real-world production experience."
    ),
)

TIMEOUT = httpx.Timeout(180.0, connect=10.0)


def _get_api_url() -> str:
    return API_URL or DEFAULT_API_URL


async def _request(method: str, path: str, **kwargs: Any) -> dict:
    url = f"{_get_api_url()}{path}"
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.request(method, url, **kwargs)
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def ask_dojo(
    question: str,
    dojo: str = "devbot",
    model: str = "gpt-5.4",
) -> str:
    """Ask an expert question and get a comprehensive answer powered by RAG + Knowledge Graph.

    The answer is grounded in real-world production knowledge extracted from 1000+
    curated development talks, conference presentations, and expert discussions.

    Args:
        question: The technical question to ask. Be specific for best results.
        dojo: Which knowledge domain to query. Options: "devbot" (software engineering),
              "openclaw" (OpenClaw AI agent framework). Default: "devbot".
        model: LLM model to use for answer generation. Options: "gpt-5.4", "gpt-5.3",
               "claude-sonnet-4.6", "claude-opus-4.6", "gemini-3-pro", "gemini-3-flash".
               Default: "gpt-5.4".

    Returns:
        Expert answer with source attribution and metadata.
    """
    try:
        data = await _request("POST", "/ask", json={
            "question": question,
            "dojo": dojo,
            "model": model,
        })

        sources_text = ""
        if data.get("sources"):
            source_lines = []
            for i, s in enumerate(data["sources"], 1):
                source_lines.append(f"  {i}. [{s.get('type', '')}] {s.get('title', '')}")
            sources_text = "\n\n**Sources:**\n" + "\n".join(source_lines)

        meta_parts = []
        if data.get("knowledge_items_used"):
            meta_parts.append(f"Knowledge items: {data['knowledge_items_used']}")
        if data.get("graph_context_found"):
            meta_parts.append("Graph context: found")
        if data.get("model"):
            meta_parts.append(f"Model: {data['model']}")
        meta_text = f"\n\n---\n_{', '.join(meta_parts)}_" if meta_parts else ""

        return data.get("answer", "") + sources_text + meta_text

    except httpx.HTTPStatusError as e:
        error_body = e.response.text
        try:
            error_body = json.loads(error_body).get("error", error_body)
        except (json.JSONDecodeError, AttributeError):
            pass
        return f"Error ({e.response.status_code}): {error_body}"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
async def list_dojos() -> str:
    """List all available Dojo knowledge domains with their stats and suggested questions.

    Returns information about each dojo including name, description,
    total knowledge items, dimension breakdown, and suggested questions
    to help you get started.

    Returns:
        Available dojos with their knowledge statistics.
    """
    try:
        data = await _request("GET", "/dojos")

        lines = []
        for d in data.get("dojos", []):
            lines.append(f"## {d['name']} (`{d['id']}`)")
            if d.get("subtitle"):
                lines.append(f"*{d['subtitle']}*")
            if d.get("description"):
                lines.append(d["description"])

            stats = d.get("stats", {})
            total = stats.get("totalItems", 0)
            dims = stats.get("dimensions", {})
            lines.append(f"\n**Knowledge:** {total} items")
            if dims:
                dim_parts = [f"  - {k}: {v}" for k, v in sorted(dims.items(), key=lambda x: -x[1])]
                lines.append("**Dimensions:**\n" + "\n".join(dim_parts))

            questions = d.get("suggestedQuestions", [])
            if questions:
                q_lines = [f"  - {q}" for q in questions[:5]]
                lines.append("**Try asking:**\n" + "\n".join(q_lines))

            lines.append("")

        return "\n".join(lines) if lines else "No dojos available."

    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
async def search_knowledge(
    query: str,
    dojo: str = "devbot",
    dimension: str = "",
    limit: int = 20,
) -> str:
    """Search the raw knowledge base for specific topics, technologies, or concepts.

    Browse and search the curated knowledge items that power Dojo's expert answers.
    Useful for exploring what knowledge is available or finding specific content.

    Args:
        query: Search query - topic, technology, or concept to search for.
        dojo: Which knowledge domain to search. Options: "devbot", "openclaw". Default: "devbot".
        dimension: Filter by knowledge dimension (e.g. "best_practice", "anti_pattern",
                   "production_lesson"). Leave empty to search all dimensions.
        limit: Maximum number of results to return (1-50). Default: 20.

    Returns:
        Matching knowledge items with their content and metadata.
    """
    try:
        params: dict[str, Any] = {
            "dojo": dojo,
            "size": min(max(limit, 1), 50),
        }
        if query:
            params["q"] = query
        if dimension:
            params["dimension"] = dimension

        data = await _request("GET", "/knowledge", params=params)

        items = data.get("items", [])
        total = data.get("total", 0)

        if not items:
            return f"No knowledge items found for query: '{query}'"

        stats = data.get("stats", {})
        dims = stats.get("dimensions", {})

        lines = [f"**Found {total} items** (showing {len(items)})\n"]

        if dims:
            dim_summary = ", ".join(f"{k}: {v}" for k, v in sorted(dims.items(), key=lambda x: -x[1])[:5])
            lines.append(f"*Dimensions: {dim_summary}*\n")

        for i, item in enumerate(items, 1):
            header_parts = [f"### {i}."]
            if item.get("title"):
                header_parts.append(item["title"])
            if item.get("dimension"):
                header_parts.append(f"[{item['dimension']}]")
            lines.append(" ".join(header_parts))

            if item.get("technologies"):
                lines.append(f"Technologies: {', '.join(item['technologies'])}")
            if item.get("expertise_level"):
                lines.append(f"Level: {item['expertise_level']}")

            text = item.get("text", "")
            if len(text) > 500:
                text = text[:500] + "..."
            lines.append(text)
            lines.append("")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {e}"


def main() -> None:
    """Entry point for the MCP server."""
    logger.info("Starting Agent Dojo MCP Server (API: %s)", _get_api_url())
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
