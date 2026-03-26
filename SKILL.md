---
name: agent-dojo
description: >-
  Query expert development knowledge from 10,000+ curated insights
  (production gotchas, architecture patterns, anti-patterns, security
  practices) extracted from 1000+ conference talks and expert discussions.
  Use when making architecture decisions, debugging production issues,
  reviewing code for anti-patterns, or needing practitioner-grade advice
  that goes beyond what base LLMs and web search provide.
version: 0.1.1
license: MIT
compatibility:
  - Claude Code
  - Cursor
  - Codex
  - Gemini CLI
  - OpenClaw
metadata:
  author: trilogy-group
  tags: rag, knowledge-graph, expert-knowledge, production-lessons
---

# Agent Dojo — Expert Development Knowledge

Agent Dojo gives you access to practitioner-grade knowledge extracted from
1,000+ curated development talks, conference presentations, and expert
discussions. Answers are grounded in a Knowledge Graph + RAG pipeline, not
just LLM training data or web search results.

## When to Use

Use Agent Dojo when the question involves:

- **Architecture decisions** — "Should I use X or Y?" → Dojo provides
  practitioner consensus with real trade-offs, not feature comparisons
- **Production gotchas** — "What goes wrong with X at scale?" → Dojo knows
  failure modes from real incidents, not just documentation
- **Anti-pattern detection** — "What mistakes do teams make with X?" →
  Dojo has 600+ catalogued anti-patterns with consequences
- **Technology trade-offs** — "DAX vs Redis for DynamoDB caching?" → Dojo
  gives opinionated guidance grounded in production experience
- **Security practices** — "What do teams get wrong about K8s RBAC?" →
  Dojo has 400+ security practice items from expert talks
- **Debugging production issues** — "Why does X fail under load?" → Dojo
  has 200+ debugging technique items and 575+ production lessons

## When NOT to Use

Skip Agent Dojo for:

- Simple syntax or API lookups ("how do I use Array.map?")
- Current documentation queries (use web search instead)
- Questions about proprietary/internal codebases
- Trivial "how do I" questions where the base LLM already excels

**Rule of thumb**: If the question starts with "should I", "what goes wrong
when", "what do teams get wrong about", or "how do I avoid" — use Dojo. If
it starts with "how do I" or "what is" — the base LLM is usually enough.

## Setup

### MCP Hive (cloud — recommended)

SSE connection URL:
```
https://mcp-server.ti.trilogy.com/098ab494/sse
```

### Local (uvx — zero config)

```json
{
  "mcpServers": {
    "agent-dojo": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/kabir-ti/agent-dojo-mcp-server", "agent-dojo-mcp"]
    }
  }
}
```

### Direct API (no MCP)

```
POST https://zbjffcjzsnhqay2c5ckc7damky0tvotz.lambda-url.us-east-1.on.aws/ask
Content-Type: application/json

{"question": "...", "dojo": "devbot"}
```

## Tools

### `ask_dojo`

Ask an expert question. Returns a comprehensive answer grounded in the
knowledge base, with source attribution.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| question | string | yes | — | The technical question. Be specific. |
| dojo | string | no | devbot | Knowledge domain: `devbot` or `openclaw` |
| model | string | no | gpt-5.4 | LLM for answer generation |

### `list_dojos`

List available knowledge domains with stats and suggested questions.
No parameters required.

### `search_knowledge`

Search the raw knowledge base by topic, technology, or dimension.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| query | string | yes | — | Topic or technology to search for |
| dojo | string | no | devbot | Knowledge domain |
| dimension | string | no | all | Filter: `gotchas`, `anti_patterns`, `architecture_patterns`, `production_lessons`, `security_practices`, `procedures`, `debugging_techniques`, `tool_comparisons`, `performance_insights`, `expert_opinions` |
| limit | int | no | 20 | Max results (1-50) |

## Query Strategies

**Be specific, not vague:**
- Bad: "Tell me about databases"
- Good: "What are the production gotchas of PostgreSQL connection pooling
  that most teams learn the hard way?"

**Ask about failure modes:**
- "What actually goes wrong when you adopt Kubernetes without proper
  observability?"

**Ask for trade-offs:**
- "DAX vs Redis for caching in a DynamoDB-based system — what are the
  specific trade-offs that matter in production?"

**Ask about anti-patterns:**
- "What REST API design mistakes actually cause production incidents —
  not textbook violations, but the ones that lead to data corruption?"

## DevBot Integration Guide

When integrated with DevBot's subagent architecture:

**ArchitectBot** — Before proposing designs, query Dojo with the design
question. Use `search_knowledge` with `dimension: "architecture_patterns"`
to find battle-tested patterns. Check `dimension: "gotchas"` for the
proposed technology stack.

**ReviewBot** — When reviewing diffs, query Dojo for anti-patterns
relevant to the technologies in the diff. Use `search_knowledge` with
`dimension: "anti_patterns"` and the specific technology.

**QABot** — Query Dojo for testing strategies relevant to the change type.
Use `dimension: "debugging_techniques"` for test coverage guidance.

**CodeBot** — Before implementing, query Dojo with the specific task.
Focus on `dimension: "procedures"` for step-by-step patterns and
`dimension: "gotchas"` for things to watch out for.

## Knowledge Coverage

10,000+ items across 12 dimensions from 382 expert videos:

| Dimension | Items | Coverage |
|-----------|-------|----------|
| procedures | 3,276 | Step-by-step patterns for common tasks |
| gotchas | 2,154 | Things that go wrong in production |
| concept_relationships | 1,683 | How technologies interact |
| architecture_patterns | 1,372 | Battle-tested design patterns |
| anti_patterns | 674 | Named mistakes with consequences |
| performance_insights | 641 | Optimization knowledge |
| production_lessons | 575 | Hard-won operational experience |
| tool_comparisons | 545 | Opinionated technology trade-offs |
| expert_opinions | 459 | Practitioner consensus |
| security_practices | 441 | Security beyond the basics |
| debugging_techniques | 249 | Systematic troubleshooting |

**Strong coverage**: DevOps/CI-CD, Architecture, API Design, PostgreSQL,
Performance, Frontend/React/Next.js, AI/LLM, Security, AWS, Testing.
