---
name: codex-image-gen
description: >-
  Generate images locally via the ChatGPT desktop app's bundled Codex CLI
  (`codex exec`) built-in image generator powered by the user's ChatGPT
  account quota with no OpenAI API key required. Use when the user asks to
  generate images with Codex or local Codex (e.g. "use codex to generate an
  image" or "用 codex 生图 / 用本地 codex 画图"), when cloud image tools return
  503 capacity limits or rate errors, or when creating text-free covers,
  illustrations, backgrounds, or concept art across Claude Code, Antigravity,
  Cursor, or Codex-compatible agent hosts.
---

# `codex-image-gen`

Generate high-craft images directly from coding agents using ChatGPT Desktop's
bundled Codex CLI (`/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex`,
or `codex` on `PATH` / `CODEX_BIN`) and your existing ChatGPT login in
`~/.codex/auth.json` — **zero API keys and zero pip dependencies**.

Helper script: [scripts/gen.py](./scripts/gen.py)

## Quick Start

Run [scripts/gen.py](./scripts/gen.py) from this skill's directory (or invoke it by its installed skill path):

```bash
python3 ./scripts/gen.py \
  "<visual description>" \
  -o /path/to/output.png \
  --size tall --effort low
```

### CLI Options

| Flag | Default | Description |
| :--- | :--- | :--- |
| `prompt` | required | Scene description including subject, lighting, framing, dark/negative-space regions, and `Strictly zero text, zero letters, zero numbers, zero watermarks`. |
| `-o`, `--out` | required | Destination PNG path (parent folders are created automatically). |
| `--size` | `auto` | Aspect-ratio hint: `tall`, `wide`, `square`, or `auto`. Dimensions are approximate (e.g., `tall` typically returns ~`941×1672`). |
| `-i`, `--image` | none | Reference image path for edits or style transfer (repeatable). |
| `--effort` | `low` | Codex reasoning effort: `minimal`, `low`, `medium`, `high` (`low` gives the fastest image turnaround). |
| `--timeout` | `600` | Execution timeout in seconds. |

On success, [scripts/gen.py](./scripts/gen.py) prints:

```text
OK /path/to/output.png  941x1672  (48s)
```

## Agent Workflow & Pitfalls

1. **Run one image at a time (sequentially)**: If Codex saves elsewhere, [scripts/gen.py](./scripts/gen.py) falls back to finding the newest `.png` by modification time inside `~/.codex/generated_images/`. Running multiple instances concurrently can race on the fallback lookup — wait for one image to complete and inspect it before generating the next.
2. **Strip proxy variables**: `HTTPS_PROXY`, `HTTP_PROXY`, and `ALL_PROXY` frequently make `codex exec` hang or time out. [scripts/gen.py](./scripts/gen.py) automatically clears them in the child environment; if invoking `codex` manually, prefix with `env -u HTTPS_PROXY -u https_proxy -u HTTP_PROXY -u http_proxy`.
3. **Run asynchronously without polling**: Expect roughly 45–180 seconds per image. In Claude Code or Antigravity, launch the command in the background (e.g., `WaitMsBeforeAsync: 5000` or `run_in_background`) and wait for the completion callback rather than polling.
4. **Never ask for rendered typography**: Image models still misspell UI copy and localized characters. Prompt for `Strictly zero text, zero letters, zero logos, zero watermarks` with darker clean zones, and overlay crisp labels in SwiftUI, CSS, or Remotion.
5. **Inspect every generated PNG**: Always open the produced image with your file/image viewer tool before integrating it to catch unintended borders, mockup frames, or stray artifacts.
6. **Resize & compress for production (macOS `sips`)**: Convert oversized PNGs into lightweight JPEG/PNG assets cleanly with `sips`:
   ```bash
   sips -Z 1152 -s format jpeg -s formatOptions 88 raw.png --out cover.jpg
   ```

## Prerequisites Check

Verify both the Codex CLI binary (or `CODEX_BIN` / `codex` in `PATH`) and ChatGPT login session exist before running:

```bash
test -x /Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex || command -v codex
test -f ~/.codex/auth.json
```

If Codex reports an expired session, sign out and back in inside the ChatGPT desktop app to refresh `~/.codex/auth.json`.

## Manual CLI Fallback

```bash
env -u HTTPS_PROXY -u https_proxy -u HTTP_PROXY -u http_proxy \
  /Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex exec \
  --skip-git-repo-check -s workspace-write -c model_reasoning_effort=low \
  "Use your built-in image generation tool to create ONE portrait image and save it into the current directory as out.png. Use image generation, not code. <description>"
```
