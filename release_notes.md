# 🚀 SemDiff v1.0 - The "Wow" Release

Say goodbye to the "wall of code" in `git diff`. **SemDiff 1.0** is here to transform your workflow by bringing local, completely private AI directly to your terminal.

## ✨ Highlights

* **🧠 Senior Architect AI:** SemDiff groups your code changes by logical intent (Feature, Bug Fix, Refactor) instead of a chaotic file-by-file view. It's like having a Senior Architect brief you on the PR in seconds.
* **🔒 100% Private (Powered by Ollama):** Your source code never leaves your machine. No API keys, no telemetry, no cloud costs. It runs entirely on your local hardware.
* **⚠️ Breaking Change Detector:** Automatically scans for modifications to config files, database schemas, Dockerfiles, and CI/CD pipelines, immediately surfacing a **HIGH RISK CHANGE** warning.
* **📋 Auto-PR Generator:** Run `semdiff --pr` to automatically generate a complete GitHub Pull Request description — complete with risk assessment — and copy it straight to your clipboard.
* **🎨 The Vibe Check:** The AI acts as a style enforcer, detecting naming convention mismatches (e.g., sneaking `snake_case` into a `camelCase` file) and flagging them automatically.

## 🛠️ Enhancements in v1.0

* **Stunning Terminal UX:** Beautiful loading spinners, rich markdown rendering, and warning panels using the `rich` Python library.
* **Safe Context Limits:** If a diff is too massive, SemDiff gracefully truncates it and prints character counts so the AI never chokes.
* **Frictionless Errors:** Helpful, actionable CLI messages (e.g., "No staged changes found. Use git add first!") instead of raw Python tracebacks.

---

### Installation

```bash
pip install git+https://github.com/Krshs90/SemDiff.git
```
*Requires Python 3.10+ and [Ollama](https://ollama.com/) running locally.*
