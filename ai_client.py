import requests  # type: ignore
import json
import sys

OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT_SUMMARY = """Act as a Senior Software Architect performing a code review.
Below is a git diff. Your task:

1. Summarize the **logical intent** of these changes using concise bullet points.
2. Group changes **by feature or purpose**, not by file.
3. Classify each group as one of: New Feature, Bug Fix, Refactor, Configuration Change, or Documentation.
4. If there are breaking changes to APIs, database schemas, or configuration files, start your response with a "WARNING: BREAKING CHANGE" section.
5. Perform a **Style Consistency Check**: if the new code uses a different naming convention (e.g., snake_case vs camelCase) than the existing code in the same file, flag it as a "STYLE MISMATCH".
6. Keep the summary concise and actionable. Write like an architect briefing a team lead, not a verbose summary bot.

Do not wrap your output in markdown code fences. Output raw markdown directly."""

SYSTEM_PROMPT_PR = """Act as a Senior Software Architect writing a Pull Request description.
Below is a git diff. Generate a complete GitHub Pull Request template with the following sections:

## Title
A concise, descriptive PR title.

## Description
A clear summary of what this PR accomplishes, grouped by feature or purpose. Mention if this is a bug fix, refactor, or new feature.

## Changes
Bullet points of the logical changes made.

## Risk Assessment
Note any breaking changes, schema modifications, or configuration changes.

## Checklist
- [ ] Code follows project style conventions
- [ ] No breaking changes introduced (or documented above)
- [ ] Tests updated if applicable

Do not wrap your output in markdown code fences. Output raw markdown directly."""


def ask_local_ai(prompt: str, model: str = "llama3.2:1b") -> str:
    """Call local Ollama instance with the given prompt and return the response."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        from rich import print as rprint  # type: ignore
    except ImportError:
        rprint = print

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
    except requests.exceptions.ConnectionError:
        rprint("[bold red]Error:[/bold red] Could not connect to Ollama. Is it running?")
        rprint("[dim]Start it with: ollama serve[/dim]")
        sys.exit(1)
    except requests.exceptions.Timeout:
        rprint("[bold red]Error:[/bold red] Ollama request timed out. The diff may be too large for the model.")
        sys.exit(1)
    except Exception as e:
        rprint(f"[bold red]AI Error:[/bold red] {e}")
        sys.exit(1)


def summarize_diff(diff_text: str, is_pr: bool = False, model: str = "llama3.2:1b") -> str:
    """Constructs prompt for either a summary or a PR template."""

    system_instruction = SYSTEM_PROMPT_PR if is_pr else SYSTEM_PROMPT_SUMMARY
    prompt = f"{system_instruction}\n\n---\n\nGit Diff:\n```diff\n{diff_text}\n```"

    return ask_local_ai(prompt, model=model)
