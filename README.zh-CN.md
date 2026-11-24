<div align="center">

[English](./README.md) | 简体中文

# 🎨 codex-image-gen

**在 Claude Code、Antigravity、Cursor 或 Codex CLI 中直接调用本地 ChatGPT 桌面端自带的 Codex 生图工具 —— 无需配置 `OPENAI_API_KEY`，直接走 ChatGPT 账号额度，零额外 API 费用。**

[![GitHub Stars](https://img.shields.io/github/stars/SikeFix/codex-image-gen?style=flat-square&color=f5c542)](https://github.com/SikeFix/codex-image-gen/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](./LICENSE)
![macOS](https://img.shields.io/badge/macOS-ChatGPT%20Desktop-000000?style=flat-square&logo=apple)
![Python](https://img.shields.io/badge/Python-3.10%2B%20零依赖-3776AB?style=flat-square&logo=python&logoColor=white)
![Agents](https://img.shields.io/badge/支持-Claude%20Code%20%7C%20Antigravity%20%7C%20Cursor-7C3AED?style=flat-square)

</div>

---

## ✨ 为什么做这个 Skill？

- **零额外 API 成本**：直接复用 `/Applications/ChatGPT.app` 内置的 Codex CLI 与 `~/.codex/auth.json` 登录态出图，不必额外购买或配置 `OPENAI_API_KEY` / 第三方中转站。
- **云端 `503` 拥塞时的稳定兜底**：当云端生图工具返回 `503 MODEL_CAPACITY_EXHAUSTED` 或限流时，Agent 可无缝切换本地 Codex 出图，不卡研发进度。
- **纯 Python 标准库零依赖**：仅使用标准库（`argparse`、`subprocess`、`tempfile`、`glob`），克隆即用，无需 `pip install`。
- **自动避开代理超时大坑**：终端常见的 `HTTPS_PROXY` / `HTTP_PROXY` / `ALL_PROXY` 会导致 `codex exec` 连不上 OpenAI 超时卡死，`gen.py` 已在子进程中自动剥离代理环境变量。
- **双重产物兜底回收**：优先收集临时工作区内的 PNG；若 Codex 未在当前目录落盘，会自动按修改时间从 `~/.codex/generated_images/*/*.png` 精准捞回最新成图。
- **支持参考图编辑（`-i`）**：可传入一张或多张参考图进行局部重绘或风格迁移。

---

## 🖼️ 实测出图展示

下面两张竖版原画均直接由本 Skill 的 `scripts/gen.py`（`--size tall --effort low`）生成，原图 `941×1672` PNG 耗时约 48～53 秒，随后经 macOS 自带 `sips` 压缩为 `648×1152` JPEG：

<div align="center">
<table>
  <tr>
    <td align="center">
      <img src="./examples/sample-obsidian-prism.jpg" width="260" alt="黑曜晶棱与鎏金星盘环" />
      <br />
      <strong>黑曜晶棱 · 鎏金星盘</strong>
      <br />
      <sub><code>--size tall --effort low</code> · 48s</sub>
    </td>
    <td align="center">
      <img src="./examples/sample-crimson-diamond.jpg" width="260" alt="七彩棱晶钻与赤金翼芒" />
      <br />
      <strong>绯金翼芒 · 棱晶钻徽</strong>
      <br />
      <sub><code>--size tall --effort low</code> · 53s</sub>
    </td>
  </tr>
</table>
</div>

<details>
<summary>查看两张样图使用的原始提示词（Prompt）</summary>

- **黑曜晶棱**：
  > Luxury collectible trading card pack flat background illustration, full-bleed edge-to-edge portrait artwork, NOT a 3D pouch mockup, NO package edges, NO crimp seals, NO frames or borders. Centered in the middle area: a luminous faceted dark obsidian and deep indigo-violet translucent crystal prism core suspended in shadow, encircled by delicate precision-engraved champagne-gold celestial astrolabe rings, flowing molten gold light ribbons, subtle ice-cyan prismatic refraction flares, and ultra-fine brushed metallic foil depth. Keep the top 18% and bottom 30% smoothly darker in deep obsidian-indigo shadow gradient so overlaid typography reads crisply. Strictly zero text, zero letters, zero numbers, zero logos, zero watermarks.

- **绯金翼芒**：
  > Luxury limited-edition master collector trading card pack flat background illustration, full-bleed edge-to-edge portrait artwork, NOT a 3D pouch mockup, NO package edges, NO crimp seals, NO frames or borders. Centered in the middle area: a radiant faceted prismatic diamond-crystal medallion bursting with 24k burnished gold aurora light wings, intricate gold celestial filigree rings, and crimson-magenta stardust energy flares set against deep obsidian-amethyst and imperial ruby-burgundy metallic foil. Keep the top 18% and bottom 30% smoothly darker in deep obsidian-burgundy shadow gradient so overlaid typography reads crisply. Strictly zero text, zero letters, zero numbers, zero logos, zero watermarks.

</details>

---

## 🚀 快速安装

按你常用的 AI 编程助手选择对应命令安装即可：

### 1. Skills CLI 一键安装（推荐）

```bash
npx skills add SikeFix/codex-image-gen
```

### 2. 安装到 Antigravity（全局 Skill）

```bash
git clone https://github.com/SikeFix/codex-image-gen.git ~/.gemini/config/skills/codex-image-gen
```

### 3. 安装到 Claude Code（全局 Skill）

```bash
git clone https://github.com/SikeFix/codex-image-gen.git ~/.claude/skills/codex-image-gen
```

### 4. 安装到单个项目内（Cursor / Codex / 团队仓库共享）

```bash
git clone https://github.com/SikeFix/codex-image-gen.git .agents/skills/codex-image-gen
```

安装完成后，直接跟 Agent 说：

> *“用 codex 生图，帮我画一张黑曜石流光质感的无字竖版背景，保存到 assets/bg.png”*

---

## 🔧 运行前提检查

1. 在 macOS 安装并登录 **[ChatGPT 桌面端](https://openai.com/chatgpt/desktop/)**；
2. 检查内嵌 Codex CLI 与登录凭证是否存在：

```bash
test -x /Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex || command -v codex
test -f ~/.codex/auth.json
```

> 如果你的 Codex CLI 不在 `ChatGPT.app` 默认路径或 `PATH` 中，可通过环境变量 `CODEX_BIN=/path/to/codex` 指定。

---

## 🛠️ 命令行用法与参数

```bash
# 生成竖版无字底图（适合 App 页面、封套、海报背景）
python3 scripts/gen.py \
  "Minimalist deep obsidian glass waves with warm gold rim lighting, strictly zero text" \
  -o ./out/cover.png \
  --size tall --effort low

# 传参考图（-i）做风格延续或局部微调
python3 scripts/gen.py \
  "Keep composition identical, shift lighting to icy cyan aurora reflections" \
  -i ./out/cover.png \
  -o ./out/cover_cyan.png \
  --size tall --effort medium
```

| 参数 | 默认值 | 说明 |
| :--- | :--- | :--- |
| `prompt` | 必填 | 画面描述（建议写明构图、光影、暗部留白区域，以及严禁出现文字/水印） |
| `-o`, `--out` | 必填 | 输出 PNG 文件路径（会自动创建缺失的父目录） |
| `--size` | `auto` | 比例倾向提示：`tall`、`wide`、`square` 或 `auto`（`tall` 实测约 `941×1672`，`wide` 约 3:1） |
| `-i`, `--image` | 无 | 参考图路径，可重复传入多个 `-i` |
| `--effort` | `low` | Codex 推理强度：`minimal` / `low` / `medium` / `high`（默认 `low` 出图最快） |
| `--timeout` | `600` | 超时秒数 |

---

## 🧠 踩坑总结与最佳实践

1. **多张图请顺序串行生成**：当需要从 `~/.codex/generated_images/*/*.png` 按时间兜底查找文件时，并发执行多条 `gen.py` 可能误抓彼此产物；让 Agent 单张依次生成并用看图工具验收后再出下一张最稳。
2. **已自动清零代理变量**：很多用户开着系统/终端代理导致 `codex exec` 卡死超时，脚本内已自动过滤 `HTTP_PROXY` / `HTTPS_PROXY` / `ALL_PROXY`。
3. **图里尽量不要带文字**：让模型生成无字纯画面 + 上下暗部渐变过渡，再用 SwiftUI / HTML / Remotion 叠加高清文字，效果最干净。
4. **体积压缩（macOS 自带 `sips`）**：App 资源打包可用一行命令从 2MB PNG 压到 ~160KB 高清 JPEG：
   ```bash
   sips -Z 1152 -s format jpeg -s formatOptions 88 raw.png --out cover.jpg
   ```

---

## 📂 目录结构

```text
codex-image-gen/
├── SKILL.md                        # Agent Skill 规范与工作流防踩坑规则
├── scripts/
│   └── gen.py                      # 零依赖 Python 封装脚本
├── examples/
│   ├── sample-obsidian-prism.jpg   # 实测生成样图（648×1152 JPEG）
│   └── sample-crimson-diamond.jpg  # 实测生成样图（648×1152 JPEG）
├── README.md
├── README.zh-CN.md
└── LICENSE
```

---

## ⭐ 求个 Star 支持一下

如果这个小工具刚好帮你省下了生图 API 费用、顶住了云端 `503` 拥塞，或者帮你排查掉了折磨半天的 Codex 代理超时问题 —— 欢迎点击右上角给仓库点个免费的 **⭐ Star**！也欢迎提 Issue / PR 补充更多比例预设或跨平台支持。

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=SikeFix/codex-image-gen&type=Date)](https://star-history.com/#SikeFix/codex-image-gen&Date)

Made with ❤️ by [@SikeFix](https://github.com/SikeFix) · [MIT License](./LICENSE)

</div>
