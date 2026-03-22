<div align="center">

# SemDiff

**Replace the wall of code in `git diff` with a high-level Executive Summary, powered by local AI.**

[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/AI-Ollama-FF6600?style=for-the-badge&logo=meta&logoColor=white)](https://ollama.com/)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)](https://github.com/Krshs90/SemDiff/pulls)

<br/>

<img src="demo.gif" alt="SemDiff in action" width="720"/>

*A messy 200-line git diff transformed into a clean 3-bullet-point summary in seconds.*

</div>

---

## The Problem

Every developer knows the pain: you run `git diff` and get hit with a **wall of raw code changes**. Hundreds of lines of insertions and deletions across multiple files, with no indication of *what actually changed* at a logical level. Code reviews slow down, context is lost, and writing PR descriptions becomes a chore.

## The Solution

**SemDiff** pipes your staged diff into a local AI model and returns a structured, human-readable summary. It groups changes **by feature, not by file**, identifies whether changes are bug fixes, refactors, or new features, and formats everything beautifully right in your terminal.

- **100% local and private** — runs on your machine via Ollama, no API keys, no cloud, no cost.
- **Fast** — uses lightweight models like `llama3.2:1b` that respond in seconds.
- **Zero config** — stage your code, run one command, done.

---

## Features

### Semantic Summarization
Groups code changes by logical intent. Instead of seeing "42 lines changed in `auth.py`", you see: *"Added JWT token refresh logic to handle expired sessions"*.

### Breaking Change Detector
If your diff touches architectural risk files like `config.py`, database schemas (`models.py`, `schema.py`, `.sql`), or migration files, SemDiff automatically surfaces a **HIGH RISK CHANGE** warning at the top of the output so nothing slips through review.

### Auto PR Description Generator
Run with `--pr` and SemDiff generates a complete GitHub Pull Request template — title, description, and checklist — based on the actual code changes. It copies the result to your clipboard so you can paste it directly into GitHub.

### Style Consistency Check (Vibe Check)
The AI scans for naming convention mismatches between the new code and the existing file. If your project uses `camelCase` but the new code introduces `snake_case`, SemDiff flags a **Style Mismatch** in the output.

### Context Window Safety
Large diffs are automatically truncated to fit within the model's context window. The tool handles this gracefully so the AI never chokes on oversized input.

---

## Installation

### Prerequisites
- **Python 3.10+**
- **[Ollama](https://ollama.com/)** installed and running locally
- A pulled model (e.g. `llama3.2:1b`)

### Setup

```bash
# Clone the repository
git clone https://github.com/Krshs90/SemDiff.git
cd SemDiff

# Install dependencies
pip install .

# Pull the default model
ollama pull llama3.2:1b
```

---

## Usage

### Basic: Summarize Staged Changes
Stage your changes in any git repository and run:

```bash
semdiff
```

> If not installed globally, run from the project directory:
> ```bash
> python main.py
> ```

### Generate a Pull Request Description
Generate a ready-to-paste PR template and copy it to your clipboard:

```bash
semdiff --pr
```

### Use a Different Model
Override the default model with any model you have pulled in Ollama:

```bash
semdiff --model mistral
```

### View Help

```bash
semdiff --help
```

---

## How It Works

```
git diff --staged
       |
       v
  +-----------+
  | Truncation |  (if diff exceeds context window limits)
  +-----------+
       |
       v
  +----------------+
  | Risk Detection |  (scans for config, schema, migration files)
  +----------------+
       |
       v
  +------------------+
  | Local AI (Ollama) |  (semantic analysis + style check)
  +------------------+
       |
       v
  +----------------+
  | Rich Formatter |  (terminal output with panels and markdown)
  +----------------+
```

1. **Capture** the staged diff via `git diff --staged`
2. **Truncate** if the diff exceeds the model's context window
3. **Detect** if any high-risk files were modified
4. **Analyze** the diff through Ollama with a carefully tuned prompt
5. **Render** the result as a formatted markdown panel in the terminal

---

## Project Structure

```
SemDiff/
├── main.py               # Typer CLI entry point
├── ai_client.py           # Ollama API integration and prompt logic
├── git_utils.py           # Git diff capture, truncation, risk detection
├── output_formatter.py    # Rich terminal rendering
├── pyproject.toml         # Package configuration and dependencies
└── README.md
```

---

## Tech Stack

| Component     | Choice            | Rationale                                      |
|---------------|-------------------|-------------------------------------------------|
| Language      | Python 3.10+      | Best ecosystem for AI orchestration and CLIs    |
| AI Engine     | Ollama (Local)    | Free, private, runs entirely on user hardware   |
| CLI Framework | Typer             | Modern, fast, auto-generates help text          |
| Formatting    | Rich              | Beautiful terminal output with panels and color |
| Model         | Llama 3.2 (1B)    | Small enough to be fast, smart enough for diffs |
| Clipboard     | Pyperclip         | Cross-platform clipboard access for PR export   |

---

## Configuration

SemDiff works out of the box with sensible defaults. No configuration files are needed.

| Parameter     | Default          | Override                  |
|---------------|------------------|---------------------------|
| Model         | `llama3.2:1b`    | `--model <name>`          |
| PR Mode       | Off              | `--pr`                    |
| Ollama URL    | `localhost:11434` | Edit `ai_client.py`       |
| Max Diff Size | 100,000 chars    | Edit `git_utils.py`       |

---

## Contributing

Contributions are welcome. Please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
  <sub>Built by <a href="https://github.com/Krshs90">Krshs90</a></sub>
</div>
