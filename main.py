import typer  # type: ignore
import pyperclip  # type: ignore
from git_utils import get_staged_diff, check_for_breaking_changes  # type: ignore
from ai_client import summarize_diff  # type: ignore
from output_formatter import console, print_summary  # type: ignore

app = typer.Typer(help="CLI tool to summarize git diffs with local AI.")

@app.command()
def diff(
    pr: bool = typer.Option(False, "--pr", help="Generate a GitHub Pull Request template and copy it to the clipboard."),
    model: str = typer.Option("llama3.2:1b", "--model", help="The Ollama model to use (e.g. llama3.2:1b, mistral).")
):
    """
    Replaces the 'wall of code' in git diff with a high-level 'Executive Summary' of logical changes powered by local AI.
    """
    with console.status("[bold green]Fetching staged git diff...", spinner="dots"):
        diff_text = get_staged_diff()
        
    if not diff_text.strip():
        console.print("[yellow]No staged changes to summarize. Stage some files and try again![/yellow]")
        return
        
    is_breaking = check_for_breaking_changes(diff_text)
    
    with console.status(f"[bold green]Analyzing diff with {model}...", spinner="dots"):
        summary_md = summarize_diff(diff_text, is_pr=pr, model=model)

    print_summary(summary_md, is_breaking=is_breaking, is_pr=pr)
    
    if pr:
        pyperclip.copy(summary_md)
        console.print("[bold green]✅ Pull request template copied to clipboard![/bold green]")

if __name__ == "__main__":
    app()
