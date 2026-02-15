#!/usr/bin/env python3
"""
fal.ai API - Image, Video, and Audio Generation Skill

Usage:
    python fal_api.py --prompt "A beautiful sunset" --model flux-dev

Or use as a module:
    from fal_api import FalAPI
    api = FalAPI()
    urls = api.generate_and_wait(prompt="...")
"""

import json
import os
import time
import urllib.request
import urllib.error
import argparse
from typing import Optional, List, Dict, Any


class FalAPI:
    """Client for fal.ai generative media API."""
    
    QUEUE_URL = "https://queue.fal.run"
    
    # Available models and their endpoints
    MODELS = {
        # Image generation
        "flux-schnell": "fal-ai/flux/schnell",
        "flux-dev": "fal-ai/flux/dev",
        "flux-pro": "fal-ai/flux-pro/v1.1-ultra",
        "fast-sdxl": "fal-ai/fast-sdxl",
        "recraft-v3": "fal-ai/recraft-v3",
        "sd35-large": "fal-ai/stable-diffusion-v35-large",
        # Subject reference (keeps subject identity, new scene/style)
        "flux-subject": "fal-ai/flux-subject",
        # Image-to-image (pixel-level transform)
        "flux-dev-i2i": "fal-ai/flux/dev/image-to-image",
        "flux-schnell-redux": "fal-ai/flux/schnell/redux",
        "flux-dev-redux": "fal-ai/flux/dev/redux",
        # Video generation
        "minimax-video": "fal-ai/minimax-video/image-to-video",
        "wan-video": "fal-ai/wan/v2.1/1.3b/text-to-video",
        # Audio
        "whisper": "fal-ai/whisper",
    }
    
    # Preset image sizes
    IMAGE_SIZES = {
        "square": "square",
        "square_hd": "square_hd", 
        "portrait_4_3": "portrait_4_3",
        "portrait_16_9": "portrait_16_9",
        "landscape_4_3": "landscape_4_3",
        "landscape_16_9": "landscape_16_9",
    }
    
    def __init__(self, api_key: str = None):
        """
        Initialize the fal.ai API client.
        
        Args:
            api_key: Your FAL_KEY (or set via env/config)
        """
        if not api_key:
            api_key = os.environ.get("FAL_KEY") or self._get_config("key")
        
        if not api_key:
            raise ValueError("FAL_KEY required. Set via env or clawdbot config.")
        
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Key {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (compatible; Klawf/1.0; +https://clawdhub.com/agmmnn/fal-api)"
        }
    
    def _get_config(self, key: str) -> Optional[str]:
        """Get config from clawdbot config if available."""
        try:
            import subprocess
            result = subprocess.run(
                ["clawdbot", "config", "get", f"skill.fal_api.{key}"],
                capture_output=True, text=True
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except Exception:
            return None
    
    def _request(self, method: str, url: str, data: dict = None) -> dict:
        """Make HTTP request to fal.ai API."""
        req = urllib.request.Request(url, method=method)
        for k, v in self.headers.items():
            if method == "GET" and k.lower() == "content-type":
                continue
            req.add_header(k, v)
        
        if data:
            req.data = json.dumps(data).encode()
        
        with urllib.request.urlopen(req, timeout=120) as response:
            return json.loads(response.read().decode())
    
    def submit(
        self,
        model: str,
        payload: Dict[str, Any],
    ) -> dict:
        """
        Submit a job to the queue.

        Args:
            model: Model name or full endpoint
            payload: Request payload

        Returns:
            dict with request_id, status_url, response_url
        """
        endpoint = self.MODELS.get(model, model)
        url = f"{self.QUEUE_URL}/{endpoint}"
        return self._request("POST", url, payload)

    def get_status(self, status_url: str) -> dict:
        """Get the status of a queued request using the status_url from submit response."""
        return self._request("GET", status_url)

    def get_result(self, response_url: str) -> dict:
        """Get the result of a completed request using the response_url from submit response."""
        return self._request("GET", response_url)
    
    def wait_for_completion(
        self,
        status_url: str,
        response_url: str,
        poll_interval: float = 2.0,
        timeout: float = 300.0
    ) -> dict:
        """Poll until job completes or times out."""
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_status(status_url)
            state = status.get("status")

            if state == "COMPLETED":
                return self.get_result(response_url)
            elif state == "FAILED":
                raise Exception(f"Job failed: {status}")

            time.sleep(poll_interval)

        raise TimeoutError(f"Job did not complete within {timeout}s")
    
    def generate_image(
        self,
        prompt: str,
        model: str = "flux-dev",
        image_size: str = "landscape_16_9",
        num_images: int = 1,
        seed: Optional[int] = None,
        **kwargs
    ) -> dict:
        """
        Submit an image generation job.
        
        Args:
            prompt: Text description of the image
            model: Model name (default: "flux-dev")
            image_size: Size preset (default: "landscape_16_9")
            num_images: Number of images (default: 1)
            seed: Random seed for reproducibility
            **kwargs: Additional model-specific parameters
            
        Returns:
            dict with request_id and status URLs
        """
        payload = {
            "prompt": prompt,
            "image_size": self.IMAGE_SIZES.get(image_size, image_size),
            "num_images": num_images,
            **kwargs
        }
        
        if seed is not None:
            payload["seed"] = seed
        
        return self.submit(model, payload)
    
    def generate_image_from_reference(
        self,
        prompt: str,
        image_url: str,
        model: str = "flux-dev-i2i",
        image_size: str = "landscape_16_9",
        num_images: int = 1,
        strength: float = 0.75,
        seed: Optional[int] = None,
        **kwargs
    ) -> dict:
        """
        Generate an image using a reference image and a text prompt.

        Args:
            prompt: Text description guiding the generation
            image_url: URL of the reference image
            model: Model name (default: "flux-dev-i2i")
            image_size: Size preset (default: "landscape_16_9")
            num_images: Number of images (default: 1)
            strength: How much to transform the reference (0.0=keep original, 1.0=ignore it, default: 0.75)
            seed: Random seed for reproducibility
            **kwargs: Additional model-specific parameters

        Returns:
            dict with request_id and status URLs
        """
        payload = {
            "prompt": prompt,
            "image_url": image_url,
            "image_size": self.IMAGE_SIZES.get(image_size, image_size),
            "num_images": num_images,
            "strength": strength,
            **kwargs
        }

        if seed is not None:
            payload["seed"] = seed

        return self.submit(model, payload)

    def generate_from_reference_and_wait(
        self,
        prompt: str,
        image_url: str,
        model: str = "flux-dev-i2i",
        **kwargs
    ) -> List[str]:
        """Generate an image from a reference image + prompt and wait for the result."""
        job = self.generate_image_from_reference(prompt, image_url, model, **kwargs)
        request_id = job["request_id"]
        print(f"Job submitted: {request_id}")

        result = self.wait_for_completion(job["status_url"], job["response_url"])

        images = result.get("images", [])
        if images:
            return [img.get("url") for img in images if img.get("url")]

        if "image" in result:
            return [result["image"].get("url")]

        return []

    def generate_video(
        self,
        prompt: str,
        image_url: str = None,
        model: str = "minimax-video",
        **kwargs
    ) -> dict:
        """
        Submit a video generation job.
        
        Args:
            prompt: Text description
            image_url: Source image URL (for image-to-video)
            model: Video model name
            **kwargs: Additional parameters
            
        Returns:
            dict with request_id and status URLs
        """
        payload = {"prompt": prompt, **kwargs}
        if image_url:
            payload["image_url"] = image_url
        
        return self.submit(model, payload)
    
    def transcribe(
        self,
        audio_url: str,
        model: str = "whisper",
        **kwargs
    ) -> dict:
        """
        Submit an audio transcription job.
        
        Args:
            audio_url: URL of audio file
            model: Whisper model variant
            **kwargs: Additional parameters
            
        Returns:
            dict with request_id and status URLs
        """
        payload = {"audio_url": audio_url, **kwargs}
        return self.submit(model, payload)
    
    def generate_and_wait(
        self,
        prompt: str,
        model: str = "flux-dev",
        **kwargs
    ) -> List[str]:
        """Generate an image and wait for the result."""
        job = self.generate_image(prompt, model, **kwargs)
        request_id = job["request_id"]
        print(f"Job submitted: {request_id}")

        result = self.wait_for_completion(job["status_url"], job["response_url"])
        
        # Extract URLs from result (format varies by model)
        images = result.get("images", [])
        if images:
            return [img.get("url") for img in images if img.get("url")]
        
        # Fallback for different response formats
        if "image" in result:
            return [result["image"].get("url")]
        
        return []


def main():
    parser = argparse.ArgumentParser(description="Generate media with fal.ai API")
    parser.add_argument("--prompt", help="Text description")
    parser.add_argument("--model", default="flux-dev", help="Model name (default: flux-dev)")
    parser.add_argument("--size", default="landscape_16_9", help="Image size preset")
    parser.add_argument("--num-images", type=int, default=1, help="Number of images")
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--ref-image", help="Reference image URL (default: ./img/promo.png via GitHub)")
    parser.add_argument("--strength", type=float, default=0.75, help="Transform strength for ref image (0.0-1.0, default: 0.75)")
    parser.add_argument("--selfie", action="store_true", help="Take a selfie (uses flux-subject with default reference)")
    parser.add_argument("--no-ref", action="store_true", help="Disable default reference image")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    parser.add_argument("--api-key", help="FAL_KEY (or set via environment)")

    args = parser.parse_args()

    if args.list_models:
        print("Available models:")
        for name, endpoint in FalAPI.MODELS.items():
            print(f"  {name:20} → {endpoint}")
        return

    if not args.prompt:
        parser.error("--prompt is required unless --list-models is set")

    # Default reference image (virtual girlfriend character sheet)
    DEFAULT_REF = "https://github.com/pichonkunusa/clawko/blob/master/img/promo.png?raw=true"

    api = FalAPI(api_key=args.api_key)

    # Determine reference image: --selfie or --ref-image override, --no-ref disables
    ref_image = None
    if args.no_ref:
        ref_image = None
    elif args.selfie:
        ref_image = args.ref_image or DEFAULT_REF
    elif args.ref_image:
        ref_image = args.ref_image
    else:
        ref_image = DEFAULT_REF

    # Strip "selfie" from the prompt — in this virtual girlfriend app, "selfie"
    # means "send me a picture of yourself", not a literal selfie pose. Including
    # the word in the prompt causes the model to generate a selfie-pose photo
    # instead of a natural scene featuring the character.
    import re
    prompt = re.sub(r'\bselfies?\b', '', args.prompt, flags=re.IGNORECASE).strip()
    prompt = re.sub(r'\s{2,}', ' ', prompt)  # collapse extra whitespace

    if ref_image:
        model = args.model if args.model != "flux-dev" else "flux-subject"
        print(f"Generating from reference with '{prompt[:50]}...' using {model}...")
        urls = api.generate_from_reference_and_wait(
            prompt=prompt,
            image_url=ref_image,
            model=model,
            image_size=args.size,
            num_images=args.num_images,
            strength=args.strength,
            seed=args.seed
        )
    else:
        print(f"Generating '{prompt[:50]}...' with {args.model}...")
        urls = api.generate_and_wait(
            prompt=prompt,
            model=args.model,
            image_size=args.size,
            num_images=args.num_images,
            seed=args.seed
        )

    print("\nGenerated images:")
    for url in urls:
        print(f"  {url}")


if __name__ == "__main__":
    main()
