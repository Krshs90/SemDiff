import typer  # type: ignore
import pyperclip  # type: ignore
from git_utils import get_staged_diff, check_for_breaking_changes  # type: ignore
from ai_client import summarize_diff  # type: ignore
from output_formatter import console, print_summary  # type: ignore

app = typer.Typer(
    help="Semantic Diff — Replace the wall of code in git diff with a high-level Executive Summary, powered by local AI.",
    no_args_is_help=False,
)


@app.command()
def diff(
    pr: bool = typer.Option(False, "--pr", help="Generate a GitHub Pull Request template and copy it to the clipboard."),
    model: str = typer.Option("llama3.2:1b", "--model", "-m", help="The Ollama model to use (e.g. llama3.2:1b, mistral)."),
):
    """
    Analyze staged git changes and produce an AI-powered semantic summary.
    """
    # Phase 1: Fetch the diff
    with console.status("[bold cyan]Fetching staged changes...", spinner="dots"):
        diff_text = get_staged_diff()

    if not diff_text.strip():
        console.print()
        console.print("[bold yellow]No staged changes found.[/bold yellow]")
        console.print("[dim]Stage your files first with:[/dim]  [bold]git add <files>[/bold]")
        console.print("[dim]Then run:[/dim]  [bold]semdiff[/bold]")
        console.print()
        raise typer.Exit()

    # Phase 2: Check for breaking changes
    is_breaking = check_for_breaking_changes(diff_text)

    # Phase 3: Analyze with AI
    action = "Generating PR description" if pr else "Analyzing diff semantically"
    with console.status(f"[bold cyan]{action} with [green]{model}[/green]...", spinner="dots"):
        summary_md = summarize_diff(diff_text, is_pr=pr, model=model)

    # Phase 4: Output
    console.print()
    print_summary(summary_md, is_breaking=is_breaking, is_pr=pr)

    if pr:
        pyperclip.copy(summary_md)
        console.print()
        console.print("[bold green]PR template copied to clipboard. Paste it directly into GitHub.[/bold green]")


if __name__ == "__main__":
    app()
