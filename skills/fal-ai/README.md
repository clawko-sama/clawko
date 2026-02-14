![](https://i.imgur.com/tP0xHSp.png)

# fal.ai API Skill

See [SKILL.md](./SKILL.md) for full documentation.

## Quick Start

```bash
# Set your API key
export FAL_KEY="your-api-key"

# Generate an image (uses default reference ./img/promo.png automatically)
python3 fal_api.py --prompt "girl at a beach, sunset"

# Selfie mode
python3 fal_api.py --selfie --prompt "the girl at a rooftop bar, city lights"

# Use a custom reference image
python3 fal_api.py --prompt "girl in a cafe, warm lighting" --ref-image "https://example.com/character.png"

# Generate without reference (plain text-to-image)
python3 fal_api.py --prompt "A cute robot cat" --no-ref --model flux-schnell

# List available models
python3 fal_api.py --list-models
```

## Configure Credentials

```bash
# Via environment
export FAL_KEY="your-api-key"

# Or via openclaw config
openclaw config set skill.fal_api.key YOUR_API_KEY
```

## Requirements

- Python 3.7+
- No external dependencies (uses stdlib)
