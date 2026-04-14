"""
List command - List all ccenv profiles
"""

import click
from rich.console import Console
from rich.table import Table

from ccenv.core.profile import ProfileManager


console = Console()


@click.command("list")
@click.pass_context
def list_profiles(ctx: click.Context) -> None:
    """
    List all available ccenv profiles.

    Examples:
        ccenv list
    """
    manager = ProfileManager()
    profiles = manager.list_profiles()

    if not profiles:
        console.print("[yellow]No profiles found.[/yellow]")
        console.print(f"  Create one with: ccenv create -n <name>")
        return

    table = Table(title="ccenv Profiles", show_header=True, header_style="bold cyan")
    table.add_column("Name", style="green")
    table.add_column("Description")
    table.add_column("Mode")

    for profile_name in profiles:
        try:
            profile = manager.load_profile(profile_name)
            table.add_row(
                profile.name,
                profile.description or "-",
                profile.mode
            )
        except Exception as e:
            table.add_row(profile_name, f"[red]Error: {e}[/red]", "-")

    console.print(table)
    console.print(f"\n[dim]Profiles directory: {manager.profiles_dir}[/dim]")