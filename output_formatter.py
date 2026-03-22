from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

def print_summary(summary_markdown: str, is_breaking: bool = False, is_pr: bool = False):
    """Prints the beautifully formatted Markdown summary to the terminal."""
    
    # If breaking change detected, print a warning box first.
    if is_breaking:
        console.print(Panel("[bold red]⚠️ HIGH RISK CHANGE DETECTED[/bold red]\nThis diff touches config or database schema files. Proceed with caution.", border_style="red"))
        console.print("")
        
    # Print the PR message or summary
    title = "📝 Pull Request Generated" if is_pr else "🧠 Semantic Diff Summary"
    
    md = Markdown(summary_markdown)
    console.print(Panel(md, title=f"[bold blue]{title}[/bold blue]", border_style="blue", padding=(1, 2)))
