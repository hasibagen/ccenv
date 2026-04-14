"""
ccenv CLI - Command line interface for Claude Code environment manager
"""

import click
from rich.console import Console
from rich.table import Table

from ccenv import __version__
from ccenv.commands.create import create
from ccenv.commands.list import list_profiles
from ccenv.commands.show import show
from ccenv.commands.use import use
from ccenv.commands.extract import extract

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="ccenv")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """
    ccenv - Claude Code Environment Manager

    Manage Claude Code configurations (MCP, plugins, skills, agents)
    with conda-like profile system.

    Examples:
        ccenv create -n eeg --mcp matlab --skill eeg-analysis
        ccenv list
        ccenv show eeg
        ccenv use eeg /path/to/project
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["console"] = console


# Register commands
main.add_command(create)
main.add_command(list_profiles, name="list")
main.add_command(show)
main.add_command(use)
main.add_command(extract)


if __name__ == "__main__":
    main()