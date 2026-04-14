"""
Show command - Display profile details
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax

from ccenv.core.profile import ProfileManager


console = Console()


@click.command()
@click.argument("name")
@click.option("--yaml", "-y", is_flag=True, help="Show raw YAML content")
@click.pass_context
def show(ctx: click.Context, name: str, yaml: bool) -> None:
    """
    Show details of a ccenv profile.

    Examples:
        ccenv show eeg
        ccenv show eeg --yaml
    """
    manager = ProfileManager()

    try:
        profile = manager.load_profile(name)
    except FileNotFoundError:
        console.print(f"[red]✗[/red] Profile '{name}' not found")
        console.print(f"  Run 'ccenv list' to see available profiles")
        raise SystemExit(1)

    if yaml:
        # Show raw YAML
        path = manager.get_profile_path(name)
        if path:
            content = path.read_text()
            syntax = Syntax(content, "yaml", theme="monokai", line_numbers=True)
            console.print(syntax)
        return

    # Show formatted details
    console.print(Panel(f"[bold cyan]{profile.name}[/bold cyan] v{profile.version}", title="Profile"))
    console.print(f"[dim]Description:[/dim] {profile.description or '-'}")
    console.print(f"[dim]Mode:[/dim] {profile.mode}")

    # Plugins
    if profile.plugins and (profile.plugins.add or profile.plugins.remove):
        console.print("\n[bold]Plugins:[/bold]")
        if profile.plugins.add:
            console.print(f"  [green]+[/green] {', '.join(profile.plugins.add)}")
        if profile.plugins.remove:
            console.print(f"  [red]-[/red] {', '.join(profile.plugins.remove)}")

    # MCP Servers
    if profile.mcp:
        console.print("\n[bold]MCP Servers:[/bold]")
        table = Table(show_header=True, header_style="dim")
        table.add_column("Name", style="cyan")
        table.add_column("Source")
        table.add_column("Type")
        for mcp_name, config in profile.mcp.items():
            table.add_row(mcp_name, config.source, config.type)
        console.print(table)

    # Skills
    if profile.skills:
        console.print("\n[bold]Skills:[/bold]")
        for skill in profile.skills:
            version = f" (v{skill.version})" if skill.version else ""
            console.print(f"  • {skill.name} [{skill.source}]{version}")

    # Agents
    if profile.agents:
        console.print("\n[bold]Agents:[/bold]")
        for agent in profile.agents:
            model = f" [{agent.model}]" if agent.model else ""
            console.print(f"  • {agent.name} [{agent.source}]{model}")

    # Environment variables
    if profile.env:
        console.print("\n[bold]Environment:[/bold]")
        for key, value in profile.env.items():
            console.print(f"  {key}={value}")

    # Hooks
    if profile.hooks:
        console.print("\n[bold]Hooks:[/bold]")
        for hook_name in profile.hooks.keys():
            console.print(f"  • {hook_name}")