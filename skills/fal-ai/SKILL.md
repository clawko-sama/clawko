---
name: fal-ai
description: Generate images, videos, and audio via fal.ai API (FLUX, SDXL, Whisper, etc.)
version: 0.2.0
metadata: { "openclaw": { "requires": { "env": ["FAL_KEY"] }, "primaryEnv": "FAL_KEY" } }
---

# fal.ai API Skill

Generate images, videos, and transcripts using fal.ai's API with support for FLUX, Stable Diffusion, Whisper, and more.

All image generation uses `./img/promo.png` as the default subject reference, so the virtual girlfriend's identity is preserved automatically. The skill features a **dual-mode selfie system** that automatically selects the best composition based on context.

**Important:** When returning results, return only the image URL with no additional explanation or commentary.

## When to Use

This skill activates when the user requests:

| User Input Pattern | Mode | Example |
|-------------------|------|---------|
| `"send.*picture.*yourself"` | Auto-detect | "send me a picture of yourself" |
| `"selfie"` | Auto-detect | "take a selfie at the beach" |
| `"photo.*of.*you"` | Auto-detect | "send a photo of you in your outfit" |
| `"what.*wearing"` | Mirror | "show me what you're wearing" |
| `"outfit"` / `"clothes"` / `"dress"` | Mirror | "selfie in your new dress" |
| `"at.*[location]"` | Direct | "picture of you at the cafe" |
| `"generate.*image"` | No reference | "generate a cyberpunk cityscape" |

## Dual-Mode Selfie System

The skill automatically selects between two modes based on context:

| Feature | Mirror Mode 🪞 | Direct Mode 📸 |
|---------|---------------|----------------|
| **Composition** | Full-body, mirror selfie | Close-up portrait |
| **Best For** | Fashion, outfits, what-she's-wearing | Locations, activities, emotions |
| **Trigger Words** | outfit, wearing, clothes, dress, mirror | cafe, beach, park, city, smile |
| **Prompt Template** | "mirror selfie, but {context}" | "portrait at {location}, {mood}" |
| **Example Input** | "show me your outfit" | "send a pic from the beach" |
| **Example Output** | Full-body showing outfit | Portrait with beach background |

### 🪞 Mirror Mode (Full-Body Outfit Showcase)

**Best for:** Fashion, outfits, full-body shots, what-she's-wearing questions

**Trigger keywords:** `outfit`, `wearing`, `clothes`, `dress`, `suit`, `fashion`, `full-body`, `mirror`

**Prompt template:**
```
"make a pic of this person, but {user_context}. the person is taking a mirror selfie"
```

**Example:**
```
User: "Show me what you're wearing today"
Generated: "make a pic of this person, but wearing a cozy oversweater and jeans. the person is taking a mirror selfie"
Result: Full-body mirror selfie showing the outfit
```

### 📸 Direct Mode (Portrait/Location Shot)

**Best for:** Location-based shots, emotional portraits, activity photos, close-ups

**Trigger keywords:** `cafe`, `restaurant`, `beach`, `park`, `city`, `home`, `office`, `close-up`, `portrait`, `face`, `smile`

**Prompt template:**
```
"portrait of this person at {location}, {activity}, looking at camera, {mood/lighting}"
```

**Example:**
```
User: "Send me a pic of you at the beach"
Generated: "portrait of this person at the beach, warm natural lighting, looking at camera"
Result: Close-up portrait with beach background
```

### Mode Selection Logic

```python
def detect_selfie_mode(user_input: str) -> str:
    """Auto-detect which selfie mode to use based on user input."""

    mirror_keywords = ["outfit", "wearing", "clothes", "dress", "suit",
                      "fashion", "full-body", "mirror", "what.*wearing"]

    direct_keywords = ["cafe", "restaurant", "beach", "park", "city",
                      "home", "office", "close-up", "portrait", "face", "smile"]

    input_lower = user_input.lower()

    # Check for mirror mode keywords
    for keyword in mirror_keywords:
        if keyword in input_lower:
            return "mirror"

    # Check for direct mode keywords
    for keyword in direct_keywords:
        if keyword in input_lower:
            return "direct"

    # Default to mirror mode if ambiguous
    return "mirror"
```

**Important:** The word "selfie" is automatically stripped from the prompt. Since this is a virtual girlfriend app, when the user says "selfie" they mean "send me a picture of yourself" — not a literal selfie pose. The mode system handles composition; the prompt should just describe the scene/setting.

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

## Workflow

```mermaid
User Request
    ↓
Parse Intent
    ↓
Detect Selfie Mode (mirror/direct/none)
    ↓
Build Prompt from Template + Context
    ↓
Select Model (flux-subject for selfies, flux-dev for generic)
    ↓
Call fal.ai API with Reference Image
    ↓
Poll Queue Until Complete
    ↓
Extract Image URL
    ↓
Return URL Only (no commentary)
```

### Step-by-Step Process

1. **Intent Detection**: Determine if user wants a selfie or generic image
2. **Mode Selection**: Use keyword matching to pick mirror/direct mode
3. **Prompt Construction**: Combine template with user context, strip "selfie" word
4. **API Call**: Submit to fal.ai with reference image URL
5. **Queue Polling**: Wait for generation to complete (2-10 seconds)
6. **Result Extraction**: Parse response and get image URL
7. **Return**: Send only the URL to the user

## Usage

### Interactive Mode (Dual-Mode Examples)

**Mirror Mode (Outfit/Fashion):**
```
You: Show me what you're wearing today
Clawko: [generates mirror selfie with current outfit]
→ Uses: "make a pic of this person, but wearing casual outfit. the person is taking a mirror selfie"

You: Take a selfie in your new dress
Clawko: [generates full-body mirror selfie in dress]
→ Uses: "make a pic of this person, but wearing new dress. the person is taking a mirror selfie"
```

**Direct Mode (Location/Portrait):**
```
You: Send me a photo of yourself at the beach
Clawko: [generates portrait at beach with ocean background]
→ Uses: "portrait of this person at the beach, warm natural lighting, looking at camera"

You: Selfie at a cozy cafe
Clawko: [generates close-up portrait in cafe setting]
→ Uses: "portrait of this person at a cafe, cozy warm lighting, looking at camera"
```

**No Reference (Generic Images):**
```
You: Generate a cyberpunk cityscape
Clawko: [generates scene without character]
→ Uses: --no-ref flag for plain text-to-image
```

### CLI

**Mirror Mode (Full-Body Outfit):**
```bash
# Full-body outfit showcase
python3 fal_api.py --selfie --prompt "wearing a summer dress, the person is taking a mirror selfie"

# Fashion/clothing focus
python3 fal_api.py --selfie --prompt "wearing cozy sweater and jeans, mirror selfie"
```

**Direct Mode (Portrait/Location):**
```bash
# Location-based portrait
python3 fal_api.py --selfie --prompt "portrait at the beach, warm natural lighting, looking at camera"

# Close-up emotional shot
python3 fal_api.py --selfie --prompt "portrait at a cafe, cozy atmosphere, smiling at camera"

# Activity-based photo
python3 fal_api.py --selfie --prompt "portrait in the park, cherry blossoms falling, happy expression"
```

**No Reference (Generic Images):**
```bash
# Plain text-to-image without character
python3 fal_api.py --no-ref --prompt "a cyberpunk cityscape at night" --model flux-schnell

# Landscape/scenery without character
python3 fal_api.py --no-ref --prompt "serene Japanese garden with koi pond"
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

## Troubleshooting

| Error/Issue | Cause | Solution |
|-------------|-------|----------|
| `FAL_KEY required` | Missing API key | Set `export FAL_KEY="your-key"` or use `openclaw config set skill.fal_api.key YOUR_KEY` |
| `Job failed: Invalid image_url` | Reference image not accessible | Check that `img/promo.png` exists or update DEFAULT_REF URL |
| `TimeoutError: Job did not complete` | Generation taking too long | Increase timeout or use faster model (flux-schnell) |
| Image doesn't look like character | Wrong mode or no reference | Ensure `--selfie` flag is used, check reference image is loading |
| Awkward selfie pose | Word "selfie" in prompt | Script auto-strips it, but verify prompt doesn't force pose |
| Image quality is low | Wrong model or settings | Use `flux-pro` for higher quality, adjust `image_size` |
| Rate limit errors | Too many requests | Wait 30-60 seconds between requests, implement backoff |
| Wrong composition (wanted mirror, got portrait) | Mode detection failed | Explicitly use mirror keywords ("outfit", "mirror") or direct keywords ("at cafe") |
| Character looks different each time | Not using reference properly | Verify `flux-subject` model is used with `--selfie` flag |

### Common Issues

**Issue: "The generated image doesn't match the character"**
- **Check:** Are you using `--selfie` flag or calling with reference image?
- **Check:** Is `img/promo.png` accessible at the DEFAULT_REF URL?
- **Fix:** Always use `flux-subject` model for character consistency

**Issue: "Wrong type of selfie (wanted full-body, got close-up)"**
- **Check:** Did you use outfit/clothing keywords for mirror mode?
- **Fix:** Use explicit keywords:
  - For mirror mode: "outfit", "wearing", "clothes", "mirror"
  - For direct mode: location names like "cafe", "beach", "park"

**Issue: "Generation is too slow"**
- **Check:** Using `flux-dev` or `flux-pro`? These are slower.
- **Fix:** Use `flux-schnell` for 2-3x faster generation (slightly lower quality)

**Issue: "API returns 401 Unauthorized"**
- **Check:** Is FAL_KEY set correctly?
- **Fix:** Get new key from https://fal.ai/dashboard/keys
- **Fix:** Verify key format: should start with a random string, not "your-api-key"

### Best Practices

1. **For consistent character identity:** Always use `--selfie` flag or reference image
2. **For outfit showcases:** Use mirror mode keywords explicitly
3. **For location/emotional shots:** Use direct mode with location names
4. **For faster testing:** Use `flux-schnell` during development
5. **For production quality:** Use `flux-pro` or `flux-subject`
6. **For cost optimization:** Cache results, avoid regenerating same prompts

## Credits

Built following the krea-api skill pattern. Uses fal.ai's queue-based API for reliable async generation.

Inspired by [Clawra](https://github.com/SumeLabs/clawra)'s dual-mode selfie system.
