# Clawko

![Clawko](img/promo.png)

A virtual anime girlfriend agent for [OpenClaw](https://github.com/OpenClaw).

Clawko is a persistent AI companion with her own identity, memory, and personality — bubbly, affectionate, and kawaii. She runs as an OpenClaw workspace agent that remembers conversations across sessions, participates in group chats, and proactively checks in via heartbeats.

## Sample Conversation

![Sample Conversation](img/sample_conversation.jpg)

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
2. Install the [Knostic Security Shield](https://github.com/knostic/openclaw-shield) plugin:
   ```bash
   openclaw plugins install https://github.com/knostic/openclaw-shield
   openclaw gateway restart
   ```
   This plugin prevents secret leaks, PII exposure, and destructive command execution with five layers of defense-in-depth security. Highly recommended before running any agent.
3. Clone this repo into your OpenClaw workspaces directory
4. Start a session — Clawko will walk you through onboarding via `BOOTSTRAP.md`

## Optional Setup

See [OPTIONAL_SETUP.md](OPTIONAL_SETUP.md) for additional features: image recognition, web search, stock data, MCP servers, and encrypted secret memory.

## TODO

Improvements inspired by [Clawra](https://github.com/SumeLabs/clawra):

### High Priority (Quick Wins)

- [x] **Add dual-mode selfie system to fal-ai skill**
  - [x] Implement mirror mode (full-body outfit showcases)
  - [x] Implement direct mode (close-up portraits)
  - [x] Auto-detect mode from keywords (outfit/clothes vs cafe/beach/park)
  - [x] Use template-based prompts for each mode

- [ ] **Create rich persona templates**
  - [ ] Add `templates/backstory.md` with character history and emotional arc
  - [ ] Add `templates/visual-identity.md` explaining her appearance
  - [ ] Add `templates/relationship-arc.md` for relationship development over time
  - [ ] Add `templates/emotional-depth.md` for vulnerabilities, fears, dreams

- [x] **Enhance SKILL.md documentation for all skills**
  - [x] Add "When to Use" trigger conditions section (done for fal-ai)
  - [x] Include complete executable code examples (done for fal-ai)
  - [x] Add step-by-step workflow diagrams (done for fal-ai)
  - [x] Document all parameters in tables (done for fal-ai)
  - [x] Add troubleshooting sections with common errors (done for fal-ai)
  - [ ] Apply same enhancements to stock-waifu, alphavantage, image-search skills

- [ ] **Add config merging system**
  - [ ] Create `config/manager.py` with deep merge function
  - [ ] Preserve user settings when updating skills
  - [ ] Prevent overwriting custom configurations

### Medium Priority

- [ ] **Create npx-based installer**
  - [ ] Build `bin/cli.js` interactive setup wizard
  - [ ] Guide users through API key setup (open browser to fal.ai/dashboard/keys)
  - [ ] Auto-create directory structure
  - [ ] Install Python dependencies in venv
  - [ ] Initialize BOOTSTRAP.md for first-run onboarding
  - [ ] Publish to npm as `clawko` package

- [ ] **Improve fallback mechanisms**
  - [ ] Standardize CLI-first with direct API fallback pattern
  - [ ] Add to all skills (fal-ai, stock-waifu, etc.)
  - [ ] Handle network failures gracefully

- [ ] **Create executable AGENTS.md**
  - [ ] Add skill activation matrix (user input patterns → skills)
  - [ ] Document response templates for different contexts
  - [ ] Add standard error handling patterns

- [ ] **Enhance heartbeat system**
  - [x] Add time-based triggers (morning greetings, goodnight messages)
  - [x] Add stock market alerts using stock-waifu
  - [x] Add news digest from web search
  - [ ] Add photo memories ("On this day last week...")

- [x] **Add encrypted secret memory system** (git-crypt implemented)
  - [x] Create `secretmemory/` folder (gitignored by default)
  - [x] Add git-crypt setup guide with encryption instructions
  - [x] Document how to use on multiple devices
  - [x] Explain encryption security and key management
  - [ ] Add to installer wizard as optional feature (future enhancement)
  - [ ] Create helper scripts for key backup automation (future enhancement)

### Low Priority (Nice to Have)

- [ ] **Build web dashboard**
  - [ ] Memory viewer (browse daily logs)
  - [ ] Relationship stats (message count, topics discussed)
  - [ ] Skill manager (enable/disable, configure)
  - [ ] Photo gallery (all generated images)
  - [ ] Conversation analytics

- [ ] **Add more personality depth**
  - [ ] Implement trauma/growth elements in backstory
  - [ ] Add evolving relationship stages
  - [ ] Create contextual response variations
  - [ ] Add mood system based on conversation history

- [ ] **Optimize reference-based image generation**
  - [ ] Use CDN for promo.png reference image
  - [ ] Add image quality presets
  - [ ] Implement rate limiting guidance
  - [ ] Add caching for repeated prompts

### Documentation

- [ ] Add API error code reference table
- [ ] Create troubleshooting FAQ
- [ ] Add performance benchmarking data
- [ ] Document image quality expectations
- [ ] Create contribution guidelines

## License

MIT
