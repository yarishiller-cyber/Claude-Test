#!/usr/bin/env python3
"""Generate an image via OpenAI's Images API and save it locally.

Usage:
    OPENAI_API_KEY=sk-... python3 scripts/generate_image.py "a red panda on a skateboard" [--out path.png] [--size 1024x1024] [--model gpt-image-1]
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an image with OpenAI.")
    parser.add_argument("prompt", help="Text prompt describing the image.")
    parser.add_argument("--out", default=None, help="Output file path (default: images/<slug>.png).")
    parser.add_argument("--size", default="1024x1024", help="Image size (e.g. 1024x1024, 1024x1536, 1536x1024).")
    parser.add_argument("--model", default="gpt-image-1", help="OpenAI image model.")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY env var is not set.", file=sys.stderr)
        return 2

    if args.out:
        out_path = Path(args.out)
    else:
        slug = "".join(c if c.isalnum() or c in "-_" else "-" for c in args.prompt.lower())[:60].strip("-")
        out_path = Path("images") / f"{slug or 'image'}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    body = json.dumps({
        "model": args.model,
        "prompt": args.prompt,
        "size": args.size,
        "n": 1,
    }).encode()

    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            payload = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode(errors='replace')}", file=sys.stderr)
        return 1

    item = payload["data"][0]
    if "b64_json" in item:
        out_path.write_bytes(base64.b64decode(item["b64_json"]))
    elif "url" in item:
        with urllib.request.urlopen(item["url"], timeout=120) as r:
            out_path.write_bytes(r.read())
    else:
        print(f"Unexpected response: {payload}", file=sys.stderr)
        return 1

    print(str(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
