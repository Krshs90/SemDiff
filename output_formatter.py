from rich.console import Console  # type: ignore
from rich.markdown import Markdown  # type: ignore
from rich.panel import Panel  # type: ignore
from rich.text import Text  # type: ignore

console = Console()


def print_summary(summary_markdown: str, is_breaking: bool = False, is_pr: bool = False):
    """Prints the beautifully formatted Markdown summary to the terminal."""

    # Breaking change warning
    if is_breaking:
        warning = Text()
        warning.append("WARNING: HIGH RISK CHANGE DETECTED\n", style="bold red")
        warning.append(
            "This diff modifies config, schema, infrastructure, or CI/CD files.\n",
            style="red",
        )
        warning.append("Review these changes carefully before merging.", style="dim red")
        console.print(Panel(warning, border_style="red", title="[bold red]Risk Alert[/bold red]"))
        console.print()

    # Main output
    title = "Pull Request Description" if is_pr else "Semantic Diff Summary"
    subtitle = "Copied to clipboard" if is_pr else "Powered by local AI"

    md = Markdown(summary_markdown)
    console.print(
        Panel(
            md,
            title=f"[bold blue]{title}[/bold blue]",
            subtitle=f"[dim]{subtitle}[/dim]",
            border_style="blue",
            padding=(1, 2),
        )
    )
