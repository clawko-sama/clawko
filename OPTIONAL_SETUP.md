# Optional Setup

Additional features you can enable for Clawko.

## Image Recognition

Clawko uses `qwen-portal/vision-model` for image recognition (e.g. when you send a photo on Telegram). This is completely free and requires the Qwen Portal auth plugin.

1. Enable the plugin and authenticate:
   ```bash
   openclaw plugins enable qwen-portal-auth
   openclaw gateway restart
   openclaw models auth login --provider qwen-portal
   ```

2. Set the image model for Clawko (this only changes the image model, the base text model stays unchanged):
   ```bash
   openclaw models set-image qwen-portal/vision-model --agent clawko
   ```

For full setup instructions, see the [Qwen provider docs](https://docs.openclaw.ai/providers/qwen).

## Web Search

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

## Stock Data

Clawko can fetch live stock market data from Yahoo Finance via the `stock-waifu` skill.

1. Create a Python virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   pip install -r requirements.txt
   ```

2. The `stock-waifu` skill in `skills/stock-waifu/` will automatically use the venv to fetch and present stock data in Clawko's personality.

## MCP Servers via MCPorter

Clawko can call tools on any MCP server using [mcporter](https://github.com/steipete/mcporter). This enables access to services like Alpha Vantage for deeper financial analysis (options, technicals, fundamentals, macro data).

1. Add a server (e.g. Alpha Vantage):
   ```bash
   npx mcporter config add alphavantage "https://mcp.alphavantage.co/mcp?apikey=YOUR_API_KEY"
   ```

2. The `mcporter` skill in `skills/mcporter/` handles tool discovery and invocation. No global install needed — `npx mcporter` auto-installs on first run.

Get a free Alpha Vantage API key at [alphavantage.co](https://www.alphavantage.co/support/#api-key).

## Secret Memory

Clawko includes a `secretmemory/` folder for private memories that you don't want committed to a public repository. By default, this folder is gitignored. To version control and backup your private memories with encryption, use **git-crypt**.

### Setup git-crypt

1. **Install git-crypt:**
   ```bash
   # Ubuntu/Debian
   sudo apt install git-crypt

   # macOS
   brew install git-crypt

   # Arch Linux
   sudo pacman -S git-crypt
   ```

2. **Initialize git-crypt in the repository:**
   ```bash
   cd /path/to/clawko
   git-crypt init
   ```

3. **Configure encryption for secretmemory:**

   Remove `secretmemory/` from `.gitignore`:
   ```bash
   # Edit .gitignore and remove the line: secretmemory/
   sed -i '/secretmemory\//d' .gitignore
   ```

   Create/edit `.gitattributes` to encrypt the folder:
   ```bash
   echo "secretmemory/** filter=git-crypt diff=git-crypt" >> .gitattributes
   git add .gitattributes
   git commit -m "Add git-crypt encryption for secretmemory"
   ```

4. **Export your encryption key (IMPORTANT - store this safely!):**
   ```bash
   git-crypt export-key ~/clawko-git-crypt.key

   # Store this key file in a safe place:
   # - Password manager (1Password, Bitwarden, etc.)
   # - Encrypted USB drive
   # - Secure cloud storage (encrypted)
   ```

5. **Add files to secretmemory and commit:**
   ```bash
   # Files in secretmemory/ are now automatically encrypted when committed
   echo "Private note" > secretmemory/private-note.md
   git add secretmemory/
   git commit -m "Add private memories (encrypted)"
   git push
   ```

### Using on Another Device

To access encrypted memories on a new device:

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/clawko.git
   cd clawko
   ```

2. Unlock with your key:
   ```bash
   git-crypt unlock ~/clawko-git-crypt.key
   ```

Now `secretmemory/` files are automatically decrypted locally and encrypted when pushed.

### How It Works

- **On GitHub:** Files in `secretmemory/` are stored **encrypted** (unreadable without the key)
- **Locally:** Files are **automatically decrypted** when you have the key unlocked
- **Transparent:** No manual encryption/decryption needed
- **Secure:** Even if someone gets access to your GitHub repo, they can't read secretmemory contents

⚠️ **IMPORTANT:** If you lose your git-crypt key, your encrypted data is **permanently unrecoverable**. Store the key safely!
