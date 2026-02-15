---
name: fal-api
description: Generate images, videos, and audio via fal.ai API (FLUX, SDXL, Whisper, etc.)
version: 0.1.0
metadata:
  {
    "openclaw": { "requires": { "env": ["FAL_KEY"] }, "primaryEnv": "FAL_KEY" },
  }
---

# fal.ai API Skill

Generate images, videos, and transcripts using fal.ai's API with support for FLUX, Stable Diffusion, Whisper, and more.

All image generation uses `./img/promo.png` as the default subject reference, so the virtual girlfriend's identity is preserved automatically. Use `--selfie` for selfie-style prompts, or `--no-ref` for plain text-to-image without a reference.

**Important:** When returning results, return only the image URL with no additional explanation or commentary.

**Important:** The word "selfie" is automatically stripped from the prompt. Since this is a virtual girlfriend app, when the user says "selfie" they mean "send me a picture of yourself" — not a literal selfie pose. Including "selfie" in the prompt would cause the model to generate an awkward selfie-pose photo instead of a natural scene. The `--selfie` flag already handles using the character reference; the prompt itself should just describe the scene/setting.

## Features

- Default subject reference (`./img/promo.png`) — every generated image preserves character identity
- `--selfie` mode for selfie/photo-of-herself prompts
- Queue-based async generation (submit → poll → result)
- Support for 600+ AI models
- Image generation (FLUX, SDXL, Recraft)
- Subject reference — generate new scenes preserving subject identity (FLUX Subject)
- Image-to-image pixel-level transforms (FLUX dev i2i, Redux)
- Video generation (MiniMax, WAN)
- Speech-to-text (Whisper)
- Stdlib-only dependencies (no `fal_client` required)

## Setup

1. Get your API key from https://fal.ai/dashboard/keys
2. Configure with:

```bash
export FAL_KEY="your-api-key"
```

Or via openclaw config:

```bash
openclaw config set skill.fal_api.key YOUR_API_KEY
```

## Usage

### Interactive Mode

```
You: Send me a photo of yourself at the beach
Klawf: Uses flux-subject with default reference to generate the girl at the beach

You: Generate a cyberpunk cityscape
Klawf: Uses --no-ref for plain text-to-image
```

### CLI

```bash
# Default: generates with character reference automatically
python3 fal_api.py --prompt "girl at a rooftop bar, city skyline"

# Selfie mode
python3 fal_api.py --selfie --prompt "the girl at the park, cherry blossoms falling"

# Plain text-to-image (no reference)
python3 fal_api.py --no-ref --prompt "a cyberpunk cityscape" --model flux-schnell
```

### Python Script

```python
from fal_api import FalAPI

api = FalAPI()

# Subject reference with default character (./img/promo.png)
DEFAULT_REF = "https://github.com/pichonkunusa/clawko/blob/master/img/promo.png?raw=true"
urls = api.generate_from_reference_and_wait(
    prompt="girl sitting in a cafe, warm lighting",
    image_url=DEFAULT_REF,
    model="flux-subject"
)

# Plain text-to-image (no reference)
urls = api.generate_and_wait(
    prompt="A serene Japanese garden",
    model="flux-dev"
)
print(urls)
```

### Available Models

| Model              | Endpoint                              | Type              |
| ------------------ | ------------------------------------- | ----------------- |
| flux-schnell       | `fal-ai/flux/schnell`                 | Image (fast)      |
| flux-dev           | `fal-ai/flux/dev`                     | Image             |
| flux-pro           | `fal-ai/flux-pro/v1.1-ultra`          | Image (2K)        |
| fast-sdxl          | `fal-ai/fast-sdxl`                    | Image             |
| recraft-v3         | `fal-ai/recraft-v3`                   | Image             |
| sd35-large         | `fal-ai/stable-diffusion-v35-large`   | Image             |
| flux-subject       | `fal-ai/flux-subject`                 | Subject reference |
| flux-dev-i2i       | `fal-ai/flux/dev/image-to-image`      | Image-to-image    |
| flux-schnell-redux | `fal-ai/flux/schnell/redux`           | Image-to-image    |
| flux-dev-redux     | `fal-ai/flux/dev/redux`               | Image-to-image    |
| minimax-video      | `fal-ai/minimax-video/image-to-video` | Video             |
| wan-video          | `fal-ai/wan/v2.1/1.3b/text-to-video`  | Video             |
| whisper            | `fal-ai/whisper`                      | Audio             |

For the full list, run:

```bash
python3 fal_api.py --list-models
```

## Parameters

| Parameter  | Type  | Default          | Description                                           |
| ---------- | ----- | ---------------- | ----------------------------------------------------- |
| prompt     | str   | required         | Image/video description                               |
| model      | str   | "flux-dev"       | Model name from table above                           |
| image_size | str   | "landscape_16_9" | Preset: square, portrait_4_3, landscape_16_9, etc.    |
| num_images | int   | 1                | Number of images to generate                          |
| seed       | int   | None             | Random seed for reproducibility                       |
| ref-image  | str   | ./img/promo.png  | Reference image URL (default: character sheet)        |
| selfie     | flag  | false            | Selfie mode (uses flux-subject + default reference)   |
| no-ref     | flag  | false            | Disable default reference for plain text-to-image     |
| strength   | float | 0.75             | Transform strength for i2i models (0.0-1.0)          |

## Credits

Built following the krea-api skill pattern. Uses fal.ai's queue-based API for reliable async generation.
