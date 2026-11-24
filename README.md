<div align="center">

English | [简体中文](./README.zh-CN.md)

# 🎨 codex-image-gen

**Generate high-craft images directly from Claude Code, Antigravity, Cursor, or Codex CLI using ChatGPT Desktop's bundled Codex CLI — no `OPENAI_API_KEY`, \$0 extra API billing.**

[![GitHub Stars](https://img.shields.io/github/stars/SikeFix/codex-image-gen?style=flat-square&color=f5c542)](https://github.com/SikeFix/codex-image-gen/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](./LICENSE)
![macOS](https://img.shields.io/badge/macOS-ChatGPT%20Desktop-000000?style=flat-square&logo=apple)
![Python](https://img.shields.io/badge/Python-3.10%2B%20Zero--Deps-3776AB?style=flat-square&logo=python&logoColor=white)
![Agents](https://img.shields.io/badge/Works%20With-Claude%20Code%20%7C%20Antigravity%20%7C%20Cursor-7C3AED?style=flat-square)

</div>

---

## ✨ Why `codex-image-gen`?

- **Zero Extra API Cost**: Runs through `/Applications/ChatGPT.app`'s bundled Codex CLI (`~/.codex/auth.json`), using your existing ChatGPT account quota — no `OPENAI_API_KEY` or third-party relay tokens required.
- **Beat Cloud `503` Outages**: Gives your coding agent a reliable local fallback whenever cloud image generators hit `503 MODEL_CAPACITY_EXHAUSTED` or rate limits.
- **Zero Dependencies**: Built exclusively on the Python 3 standard library (`argparse`, `subprocess`, `tempfile`, `glob`). No `pip install`, no virtualenvs.
- **Fixes the Codex Proxy Timeout Trap**: Automatically strips `HTTPS_PROXY`, `HTTP_PROXY`, and `ALL_PROXY` from the child process environment so `codex exec` doesn't hang for 20 minutes on local proxy variables.
- **Bulletproof Output Discovery**: Generates inside an isolated temporary directory and automatically falls back to scanning `~/.codex/generated_images/*/*.png` by modification timestamp if Codex saves outside `cwd`.
- **Reference Image Support (`-i`)**: Attach one or more reference PNG/JPG files for style matching or iterative image edits.

---

## 🖼️ Live Showcase

Both vertical artworks below were generated directly via `scripts/gen.py` (`--size tall --effort low`, ~48–53s each at raw `941×1672` PNG, then downsized to `648×1152` JPEG via macOS `sips` for mobile app bundling):

<div align="center">
<table>
  <tr>
    <td align="center">
      <img src="./examples/sample-obsidian-prism.jpg" width="260" alt="Obsidian Prism & Gold Astrolabe" />
      <br />
      <strong>Obsidian Prism &amp; Astrolabe Rings</strong>
      <br />
      <sub><code>--size tall --effort low</code> · 48s</sub>
    </td>
    <td align="center">
      <img src="./examples/sample-crimson-diamond.jpg" width="260" alt="Prismatic Diamond & Gold Aurora Wings" />
      <br />
      <strong>Prismatic Diamond &amp; Gold Wings</strong>
      <br />
      <sub><code>--size tall --effort low</code> · 53s</sub>
    </td>
  </tr>
</table>
</div>

<details>
<summary>View prompts used for the showcase outputs</summary>

- **Obsidian Prism**:
  > Luxury collectible trading card pack flat background illustration, full-bleed edge-to-edge portrait artwork, NOT a 3D pouch mockup, NO package edges, NO crimp seals, NO frames or borders. Centered in the middle area: a luminous faceted dark obsidian and deep indigo-violet translucent crystal prism core suspended in shadow, encircled by delicate precision-engraved champagne-gold celestial astrolabe rings, flowing molten gold light ribbons, subtle ice-cyan prismatic refraction flares, and ultra-fine brushed metallic foil depth. Keep the top 18% and bottom 30% smoothly darker in deep obsidian-indigo shadow gradient so overlaid typography reads crisply. Strictly zero text, zero letters, zero numbers, zero logos, zero watermarks.

- **Prismatic Diamond**:
  > Luxury limited-edition master collector trading card pack flat background illustration, full-bleed edge-to-edge portrait artwork, NOT a 3D pouch mockup, NO package edges, NO crimp seals, NO frames or borders. Centered in the middle area: a radiant faceted prismatic diamond-crystal medallion bursting with 24k burnished gold aurora light wings, intricate gold celestial filigree rings, and crimson-magenta stardust energy flares set against deep obsidian-amethyst and imperial ruby-burgundy metallic foil. Keep the top 18% and bottom 30% smoothly darker in deep obsidian-burgundy shadow gradient so overlaid typography reads crisply. Strictly zero text, zero letters, zero numbers, zero logos, zero watermarks.

</details>

---

## 🚀 Quick Install

Pick the path matching your AI coding agent:

### 1. Skills CLI (Recommended)

```bash
npx skills add SikeFix/codex-image-gen
```

### 2. Antigravity (AGY Global Skill)

```bash
git clone https://github.com/SikeFix/codex-image-gen.git ~/.gemini/config/skills/codex-image-gen
```

### 3. Claude Code (Global Skill)

```bash
git clone https://github.com/SikeFix/codex-image-gen.git ~/.claude/skills/codex-image-gen
```

### 4. Project / Workspace Scope (Cursor, Codex, Team Repos)

```bash
git clone https://github.com/SikeFix/codex-image-gen.git .agents/skills/codex-image-gen
```

Once installed, ask your agent naturally:

> *"Use local codex to generate a dark metallic portrait background without text and save it to assets/bg.png"*
> *"用 codex 生图，画一张极简黑金流光质感竖版背景图"*

---

## 🔧 Prerequisites & Verification

1. Install and sign in to **[ChatGPT Desktop for macOS](https://openai.com/chatgpt/desktop/)**.
2. Verify both the bundled Codex binary and local auth session exist:

```bash
test -x /Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex || command -v codex
test -f ~/.codex/auth.json
```

> **Custom binary path**: Set `CODEX_BIN=/path/to/codex` if your Codex CLI lives outside `ChatGPT.app` and `PATH`.

---

## 🛠️ CLI Usage

```bash
# Portrait artwork (recommended for app screens, covers, posters)
python3 scripts/gen.py \
  "Minimalist deep obsidian glass waves with warm gold rim lighting, strictly zero text" \
  -o ./out/cover.png \
  --size tall --effort low

# Image editing / style reference with -i
python3 scripts/gen.py \
  "Keep composition identical, shift lighting to icy cyan aurora reflections" \
  -i ./out/cover.png \
  -o ./out/cover_cyan.png \
  --size tall --effort medium
```

### Parameters

| Option | Default | Description |
| :--- | :--- | :--- |
| `prompt` | required | Visual description (subject, lighting, safe dark zones, and zero-text constraints) |
| `-o`, `--out` | required | Destination PNG file path (parent directories created automatically) |
| `--size` | `auto` | Aspect hint: `tall`, `wide`, `square`, or `auto` (`tall` typically yields ~`941×1672`, `wide` ~3:1) |
| `-i`, `--image` | none | Reference image path for edits or style transfer (can be passed multiple times) |
| `--effort` | `low` | Codex reasoning effort: `minimal`, `low`, `medium`, or `high` (`low` gives fastest generation) |
| `--timeout` | `600` | Timeout in seconds |

---

## 🧠 Battle-Tested Pitfalls Solved

1. **Sequential runs only**: When Codex writes outside the working directory, `gen.py` falls back to scanning `~/.codex/generated_images/*/*.png` by timestamp. Run one generation at a time so concurrent runs never collide on the fallback file.
2. **Automatic proxy stripping**: Local `HTTP_PROXY` / `HTTPS_PROXY` / `ALL_PROXY` env vars routinely stall `codex exec`. `gen.py` strips them cleanly before spawning the subprocess.
3. **Overlay typography in code, not in pixels**: Ask the generator for `Strictly zero text, zero letters, zero logos, zero watermarks` with clean darker zones at the top/bottom, then render crisp localized titles in SwiftUI, CSS, or HTML.
4. **Fast mobile asset optimization (macOS `sips`)**:
   ```bash
   sips -Z 1152 -s format jpeg -s formatOptions 88 raw.png --out cover.jpg
   ```

---

## 📂 Repository Structure

```text
codex-image-gen/
├── SKILL.md                        # Agent skill definition & workflow guardrails
├── scripts/
│   └── gen.py                      # Zero-dependency Python CLI wrapper around Codex
├── examples/
│   ├── sample-obsidian-prism.jpg   # Live showcase output (648×1152 JPEG)
│   └── sample-crimson-diamond.jpg  # Live showcase output (648×1152 JPEG)
├── README.md
├── README.zh-CN.md
└── LICENSE
```

---

## ⭐ Support

If `codex-image-gen` saved you from API billing setup, cloud `503` outages, or mysterious `codex exec` proxy timeouts, please give this repo a free **⭐ Star** on GitHub! Issues and PRs for Linux/Windows paths or extra aspect presets are very welcome.

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=SikeFix/codex-image-gen&type=Date)](https://star-history.com/#SikeFix/codex-image-gen&Date)

Made with ❤️ by [@SikeFix](https://github.com/SikeFix) · Released under the [MIT License](./LICENSE)

</div>
