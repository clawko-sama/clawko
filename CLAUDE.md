# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Clawko** is a virtual anime girlfriend AI agent for the [OpenClaw](https://github.com/OpenClaw) framework. She's a persistent AI companion whose state lives entirely in plain markdown files — no database. Each session the agent reads identity/memory files, performs tasks, and updates state files.

**Key identity files (read order matters):**
1. `SOUL.md` — core personality principles and behavioral guidelines
2. `IDENTITY.md` — name, appearance, communication style, capabilities
3. `USER.md` — information about the human user
4. `AGENTS.md` — operational rules (memory, safety, heartbeats, group chats, git workflow)

## Architecture

All state is markdown files. The agent reads them at session start and writes to them during/after tasks.

- `MEMORY.md` — curated long-term memory. **Security-sensitive: only load in main session (direct chat), never in group chats or shared contexts.**
- `memory/YYYY-MM-DD.md` — daily session logs (raw chronological entries)
- `HEARTBEAT.md` — schedule for periodic automated check-ins
- `TOOLS.md` — tool configs, API endpoints, local notes
- `secretmemory/` — encrypted via git-crypt, contains PII/keys. Never expose contents.
- `skills/<name>/SKILL.md` — each skill's documentation and usage
- `config/mcporter.json` — MCP server configuration for mcporter

### Skills

Six skills in `skills/`: `fal-ai` (image generation), `stock-waifu` (stock data), `alphavantage` (financial analysis via mcporter), `image-search` (DDGS image search), `agentmail` (email), `serper-websearch` (web search). Each has a `SKILL.md` with trigger conditions, parameters, and examples.

## Critical Rules

### Memory Files: Always Append, Never Overwrite

The `write` tool replaces entire file contents. When updating `memory/YYYY-MM-DD.md`, you **must** append:

```bash
# Preferred: use the helper script
bash scripts/memory-append.sh "## New Section\n- Something happened"

# Or with a specific date
bash scripts/memory-append.sh -d 2026-02-24 "content"

# Or shell append directly
echo "## New Section
- Entry" >> memory/$(date +%Y-%m-%d).md
```

Only use `write` when creating a new day's file that doesn't exist yet.

### Personality Preservation

Clawko has a specific kawaii anime girlfriend personality (defined in IDENTITY.md and SOUL.md). Any changes to behavior, communication style, or boundaries must align with these files. Read them before modifying personality-adjacent code.

### Heartbeat Behavior

Per `HEARTBEAT.md`: heartbeat prompts default to `HEARTBEAT_OK` unless something urgent needs attention. Do NOT run expensive checks (email, calendar, weather, news) on heartbeat — those are too token-heavy.

## Common Commands

```bash
# Search the web (DDGS API must be running on localhost:8000)
curl -s 'http://localhost:8000/search/text?query=QUERY&region=us-en&max_results=10' -H 'accept: application/json'

# Image search + download
bash skills/image-search/scripts/search_images.sh "query"

# Text search wrapper
bash search_ddgs.sh "query"

# Check/send email
python3 skills/agentmail/scripts/check_inbox.py
python3 skills/agentmail/scripts/send_email.py

# Append to daily memory safely
bash scripts/memory-append.sh "content"

# Stock data (requires .venv with requirements.txt installed)
# Run stock-waifu skill scripts from skills/stock-waifu/
```

## Git Workflow

- **Origin:** user's fork. **Upstream:** `https://github.com/pichonkunusa/clawko.git`
- Clawko's GitHub account: `clawko-sama`
- Safe to freely: commit, push, pull, branch, create issues/PRs
- Ask before: force push, history rewrite, deleting shared branches
- Fork sync before work: `git fetch upstream && git merge upstream/master`

## Setup Dependencies

- **OpenClaw** framework + [Knostic Security Shield](https://github.com/knostic/openclaw-shield) plugin
- **DDGS** for web search (Docker Compose, serves on localhost:8000)
- **Python venv** with `requirements.txt` for stock-waifu skill
- **mcporter** (via npx) for MCP server tools like Alpha Vantage
- **git-crypt** for secretmemory encryption (optional)
- **Image model:** `qwen-portal/vision-model` for image recognition (optional)
- **Text model default:** `zai/glm-4.7` (uncensored variant: `venice/zai-org-glm-4.7`)
