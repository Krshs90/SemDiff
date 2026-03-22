import requests  # type: ignore
import json
import sys

OLLAMA_URL = "http://localhost:11434/api/generate"

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
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
    except requests.exceptions.ConnectionError:
        rprint("[red]Error: Could not connect to local Ollama instance. Is it running?[/red]")
        sys.exit(1)
    except Exception as e:
        rprint(f"[red]AI Error: {e}[/red]")
        sys.exit(1)

def summarize_diff(diff_text: str, is_pr: bool = False, model: str = "llama3.2:1b") -> str:
    """Constructs prompt for either a summary or a PR template, and checks style mismatch."""
    
    system_instruction = (
        "Analyze this git diff and summarize the logical intent. "
        "Group changes by feature, not by file. Identify if this is a bug fix, a refactor, or a new feature. "
        "Also, perform a 'Vibe Check': check if the new code matches the 'style' of the existing file (e.g. check camelCase vs snake_case consistency). "
        "If you detect a style mismatch, prominently flag a 'Style Mismatch' in your output.\n"
    )

    if is_pr:
        system_instruction += (
            "\nOutput exactly a GitHub Pull Request template based on these changes.\n"
            "Include a Title, Description (with the logical summary), and a minor Checklist of things done. "
            "Do not output markdown codeblock ticks (```markdown) at the boundaries, just the raw markdown content."
        )
    else:
        system_instruction += (
            "\nOutput a nicely formatted Markdown summary containing short bullet points. "
            "Do not output markdown codeblock ticks at the boundaries, just the raw markdown content."
        )
        
    prompt = f"{system_instruction}\n\nHere is the Git Diff:\n```diff\n{diff_text}\n```"
    
    return ask_local_ai(prompt, model=model)
