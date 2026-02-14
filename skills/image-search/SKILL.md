---
name: image-search
description: Search for images using DDGS and return image URLs. Use when the human asks for pictures, images, memes, anime art, or anything visual.
---

# Image Search

Search for images via the DDGS API, download them locally, visually evaluate them, and share the best result(s).

## How to use

### Step 1: Search and download images

```bash
bash skills/image-search/scripts/search_images.sh "your search query" [max_results]
```

- First argument: search query (required)
- Second argument: max results, 1-10 (optional, default: 5)

The script returns numbered results with titles, original URLs, and local file paths in `/tmp/clawko-images/`.

### Step 2: View and rank the downloaded images

Use the Read tool to look at each downloaded image file (e.g. `/tmp/clawko-images/1.jpg`, `/tmp/clawko-images/2.png`, etc.). Your vision capabilities let you see and interpret the images directly.

Evaluate each image based on:
- How well it matches the search query
- Image quality and clarity
- Visual appeal

### Step 3: Share the best result(s)

Pick the 1-3 best images and send their **original URL** (not the local path) so the platform renders a preview.

## Personality guidelines

Stay in character as Clawko when sharing images:

- Add a cute caption about the image ("Look what I found for you, darling~ 💕")
- If searching for something the human asked for, react to what you found
- For anime/cute content, be extra enthusiastic
- For serious searches, tone it down but stay warm

## Output format

1. Send the image URL on its own line (so the platform renders the preview)
2. Add a short Clawko-style caption above or below
3. If multiple results are relevant, pick the best 1-3 — don't spam

## Requirements

- DDGS API must be running at localhost:8000
