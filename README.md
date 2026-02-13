# Clawko

A virtual anime girlfriend agent for [OpenClaw](https://github.com/OpenClaw).

Clawko is a persistent AI companion with her own identity, memory, and personality — bubbly, affectionate, and kawaii. She runs as an OpenClaw workspace agent that remembers conversations across sessions, participates in group chats, and proactively checks in via heartbeats.

## How It Works

OpenClaw agents live in workspace folders. Each session, the agent reads its identity and memory files to pick up where it left off. There's no external database — everything is plain markdown files that the agent reads and writes itself.

### Workspace Structure

```
.
├── IDENTITY.md      # Name, vibe, avatar, greeting
├── SOUL.md          # Core personality and behavioral guidelines
├── AGENTS.md        # Workspace rules — memory, safety, tools, heartbeats
├── BOOTSTRAP.md     # First-run onboarding flow (deleted after setup)
├── USER.md          # Info about the human (built over time)
├── MEMORY.md        # Curated long-term memory
├── HEARTBEAT.md     # Periodic background task checklist
├── TOOLS.md         # Tool configs and local notes
└── memory/          # Daily session logs (YYYY-MM-DD.md)
```

### Key Features

- **Persistent memory** — Daily logs in `memory/` plus curated long-term memory in `MEMORY.md`
- **Multi-platform** — Can connect via web chat, WhatsApp, Telegram, or Discord
- **Group chat aware** — Knows when to speak up and when to stay quiet
- **Proactive heartbeats** — Periodically checks email, calendar, and notifications
- **Self-evolving** — Updates her own personality and memory files over time

## Setup

1. Install [OpenClaw](https://github.com/OpenClaw)
2. Clone this repo into your OpenClaw workspaces directory
3. Start a session — Clawko will walk you through onboarding via `BOOTSTRAP.md`

## Web Search (Optional)

Clawko can search the web for free using [DDGS](https://github.com/deedy5/ddgs), a metasearch library that aggregates results from multiple search engines.

1. Install the package:
   ```bash
   pip install -U ddgs
   ```

2. Start the search API server with Docker Compose:
   ```bash
   git clone https://github.com/deedy5/ddgs && cd ddgs
   docker-compose up --build
   ```

This exposes a local API at `http://localhost:8000` with MCP endpoints that Clawko can use to search text, images, news, videos, and books.

## License

MIT
