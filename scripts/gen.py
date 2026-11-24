#!/usr/bin/env python3
"""Generate images using the local ChatGPT desktop app's bundled Codex CLI.

Uses your authenticated ChatGPT session (~/.codex/auth.json) with no API key
required. Automatically strips proxy variables (HTTPS_PROXY / HTTP_PROXY /
ALL_PROXY) that frequently cause Codex CLI requests to time out, captures the
generated PNG in a scratch workspace, and falls back to scanning
~/.codex/generated_images by timestamp if needed.

Examples:
  python3 scripts/gen.py "Minimalist aurora waves over dark glass" -o out.png --size tall
  python3 scripts/gen.py "Apply brushed gold foil border" -o out.png -i ref.png --effort low
"""

import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile
import time

DEFAULT_CODEX_BIN = "/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex"
GEN_DIR = os.path.expanduser("~/.codex/generated_images")
PROXY_VARS = {"https_proxy", "http_proxy", "all_proxy"}

SIZE_HINTS = {
    "wide": "a wide landscape image (widest aspect ratio you support)",
    "square": "a square image",
    "tall": "a tall portrait image (phone-screen proportions)",
    "auto": "one image",
}


def resolve_codex_binary() -> str | None:
    """Resolve Codex CLI from CODEX_BIN env, ChatGPT.app bundle, or PATH."""
    candidates = [
        os.environ.get("CODEX_BIN"),
        DEFAULT_CODEX_BIN,
        shutil.which("codex"),
    ]
    for path in candidates:
        if path and os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    return None


def newest_generated(since: float) -> str | None:
    """Locate the newest fallback PNG produced in ~/.codex/generated_images."""
    files = [
        f
        for f in glob.glob(os.path.join(GEN_DIR, "*", "*.png"))
        if os.path.getmtime(f) >= since
    ]
    return max(files, key=os.path.getmtime) if files else None


def read_image_dimensions(path: str) -> str:
    """Read pixel dimensions using macOS sips when available."""
    if not shutil.which("sips"):
        return "?x?"
    res = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", path],
        capture_output=True,
        text=True,
    )
    tokens = res.stdout.split()
    if len(tokens) >= 4:
        return f"{tokens[-3]}x{tokens[-1]}"
    return "?x?"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate images locally via ChatGPT Desktop's bundled Codex CLI."
    )
    parser.add_argument("prompt", help="Visual description for image generation")
    parser.add_argument("-o", "--out", required=True, help="Output PNG file path")
    parser.add_argument(
        "--size",
        default="auto",
        choices=list(SIZE_HINTS),
        help="Aspect ratio hint (default: auto)",
    )
    parser.add_argument(
        "-i",
        "--image",
        action="append",
        default=[],
        help="Optional reference image path (repeatable)",
    )
    parser.add_argument(
        "--effort",
        default="low",
        choices=["minimal", "low", "medium", "high"],
        help="Codex reasoning effort (default: low)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Timeout in seconds (default: 600)",
    )
    args = parser.parse_args()

    codex_bin = resolve_codex_binary()
    if not codex_bin:
        sys.exit(
            f"Codex CLI not found at {DEFAULT_CODEX_BIN} or in PATH. "
            "Install and sign in to ChatGPT Desktop, or set CODEX_BIN."
        )

    out_path = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    work_dir = tempfile.mkdtemp(prefix="codex_img_")
    output_name = "result.png"
    full_prompt = (
        f"Use your built-in image generation tool to create ONE image: "
        f"{SIZE_HINTS[args.size]}. Save it into the current directory as {output_name}. "
        "Use image generation, not code (do not draw it with a script). "
        "No text, letters, logos, UI or watermark in the image unless the description "
        f"explicitly asks for specific text.\n\nDescription: {args.prompt}"
    )

    cmd = [
        codex_bin,
        "exec",
        "--skip-git-repo-check",
        "-s",
        "workspace-write",
        "-c",
        f"model_reasoning_effort={args.effort}",
    ]
    for image_path in args.image:
        cmd.extend(["-i", os.path.abspath(image_path)])
    cmd.append(full_prompt)

    clean_env = {
        k: v for k, v in os.environ.items() if k.lower() not in PROXY_VARS
    }

    start_time = time.time()
    try:
        try:
            proc = subprocess.run(
                cmd,
                cwd=work_dir,
                env=clean_env,
                capture_output=True,
                text=True,
                timeout=args.timeout,
            )
        except subprocess.TimeoutExpired:
            sys.exit(
                f"Timed out after {args.timeout}s. Check network connectivity, proxy settings, "
                "or verify your ChatGPT Desktop login in ~/.codex/auth.json."
            )

        produced = os.path.join(work_dir, output_name)
        if not os.path.exists(produced):
            pngs = sorted(glob.glob(os.path.join(work_dir, "*.png")))
            produced = pngs[0] if pngs else newest_generated(start_time - 5)

        if not produced or not os.path.exists(produced):
            sys.stderr.write((proc.stdout or "")[-1500:] + (proc.stderr or "")[-1500:])
            sys.exit("Codex did not produce an image (see output above).")

        shutil.copyfile(produced, out_path)
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)

    dims = read_image_dimensions(out_path)
    elapsed = time.time() - start_time
    print(f"OK {out_path}  {dims}  ({elapsed:.0f}s)")


if __name__ == "__main__":
    main()
