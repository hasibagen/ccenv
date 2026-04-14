"""
Use command - Apply a profile to a project
"""

from pathlib import Path
from typing import Optional
import json
import click
from rich.console import Console
from rich.prompt import Confirm

from ccenv.core.profile import ProfileManager
from ccenv.core.plugins import PluginManager
from ccenv.utils.validation import validate_path


console = Console()


@click.command()
@click.argument("name")
@click.argument("project_path", type=click.Path(exists=False), default=".")
@click.option("--scope", type=click.Choice(["project", "local"]), default="project", help="Configuration scope")
@click.option("--force", "-f", is_flag=True, help="Overwrite existing configuration")
@click.option("--dry-run", is_flag=True, help="Show what would be done without making changes")
@click.pass_context
def use(
    ctx: click.Context,
    name: str,
    project_path: str,
    scope: str,
    force: bool,
    dry_run: bool,
) -> None:
    """
    Apply a ccenv profile to a project.

    Examples:
        ccenv use eeg /path/to/project
        ccenv use eeg . --scope project
        ccenv use eeg . --dry-run
    """
    manager = ProfileManager()

    # Load profile
    try:
        profile = manager.load_profile(name)
    except FileNotFoundError:
        console.print(f"[red]✗[/red] Profile '{name}' not found")
        raise SystemExit(1)

    # Resolve project path
    project = Path(project_path).resolve()
    if not project.exists():
        if dry_run:
            console.print(f"[yellow]![/yellow] Project path does not exist: {project}")
        else:
            project.mkdir(parents=True, exist_ok=True)
            console.print(f"[green]✓[/green] Created project directory: {project}")

    if dry_run:
        console.print(f"\n[bold]Dry run for profile '{name}' on {project}[/bold]\n")

    # Apply MCP configuration
    if profile.mcp:
        mcp_path = project / ".mcp.json"
        if mcp_path.exists() and not force and not dry_run:
            if not Confirm.ask(f"Overwrite existing {mcp_path}?"):
                console.print("[yellow]Skipped MCP configuration[/yellow]")
            else:
                _apply_mcp_config(profile, mcp_path, dry_run)
        else:
            _apply_mcp_config(profile, mcp_path, dry_run)

    # Apply Plugin configuration
    if profile.plugins:
        plugin_manager = PluginManager(project)
        plugins_add = profile.plugins.add
        plugins_remove = profile.plugins.remove

        if dry_run:
            console.print(f"[dim]Plugins to add:[/dim] {plugins_add}")
            console.print(f"[dim]Plugins to remove:[/dim] {plugins_remove}")
        else:
            final_plugins = plugin_manager.merge_plugins(
                plugins_add,
                plugins_remove,
                mode=profile.mode,
                scope=scope
            )
            console.print(f"[green]✓[/green] Applied plugins: {', '.join(final_plugins) or 'none'}")

    # Apply environment variables
    if profile.env:
        env_example_path = project / ".env.ccenv"
        if dry_run:
            console.print(f"[dim]Would create:[/dim] {env_example_path}")
            for key, value in profile.env.items():
                console.print(f"  {key}={value}")
        else:
            env_content = "\n".join(f"{k}={v}" for k, v in profile.env.items())
            env_example_path.write_text(f"# ccenv environment variables\n{env_content}\n")
            console.print(f"[green]✓[/green] Created {env_example_path}")

    # Copy skills (if project-level)
    if profile.skills and scope == "project":
        _apply_skills(profile, project, dry_run)

    # Copy agents (if project-level)
    if profile.agents and scope == "project":
        _apply_agents(profile, project, dry_run)

    if dry_run:
        console.print("\n[dim]Run without --dry-run to apply changes[/dim]")
    else:
        console.print(f"\n[green]✓[/green] Profile '{name}' applied to {project}")


def _apply_mcp_config(profile, mcp_path: Path, dry_run: bool) -> None:
    """Apply MCP configuration to .mcp.json"""
    import os

    mcp_config = {"mcpServers": {}}

    for mcp_name, config in profile.mcp.items():
        source = config.source
        mcp_command = source
        mcp_args = list(config.args)

        # Resolve source
        if source.startswith("local:${") and source.endswith("}"):
            # Environment variable reference
            var_name = source[7:-1]
            resolved = os.environ.get(var_name)
            if not resolved:
                console.print(f"[yellow]![/yellow] Environment variable {var_name} not set, skipping {mcp_name}")
                continue
            mcp_command = resolved
        elif source.startswith("npm:"):
            # npm package -> use npx
            package = source[4:]
            mcp_command = "npx"
            mcp_args = ["-y", package] + mcp_args
        elif source.startswith("pip:"):
            # pip package -> use python -m
            package = source[4:]
            mcp_command = "python"
            mcp_args = ["-m", package] + mcp_args

        mcp_config["mcpServers"][mcp_name] = {
            "type": config.type,
            "command": mcp_command,
            "args": mcp_args,
        }

        if config.env:
            mcp_config["mcpServers"][mcp_name]["env"] = config.env

    if dry_run:
        console.print(f"[dim]Would create:[/dim] {mcp_path}")
        console.print(json.dumps(mcp_config, indent=2))
    else:
        mcp_path.write_text(json.dumps(mcp_config, indent=2))
        console.print(f"[green]✓[/green] Created {mcp_path}")


def _apply_skills(profile, project: Path, dry_run: bool) -> None:
    """Apply skills to project"""
    import shutil

    skills_dir = project / ".claude" / "skills"
    global_skills_dir = Path.home() / ".claude" / "skills"
    plugins_dir = Path.home() / ".claude" / "plugins" / "cache"

    if dry_run:
        console.print(f"[dim]Would copy skills to:[/dim] {skills_dir}")
        return

    skills_dir.mkdir(parents=True, exist_ok=True)

    for skill in profile.skills:
        src = None

        # Find skill source
        if skill.source == "global":
            src = global_skills_dir / skill.name
        elif skill.source == "project":
            continue  # Already in project
        elif skill.source.startswith("plugin:"):
            # Plugin source: plugin:plugin-name
            # Search in all versions of the plugin
            plugin_name = skill.source[7:]
            plugin_cache = plugins_dir / plugin_name
            if plugin_cache.exists():
                # Search recursively for skills/{skill.name}
                for potential in plugin_cache.rglob(f"skills/{skill.name}"):
                    if potential.is_dir():
                        src = potential
                        break
        else:
            # Try to find in plugins as fallback (search all plugins)
            for plugin_cache in plugins_dir.iterdir():
                if plugin_cache.is_dir():
                    for potential in plugin_cache.rglob(f"skills/{skill.name}"):
                        if potential.is_dir():
                            src = potential
                            break
                if src:
                    break

        if src and src.exists():
            dst = skills_dir / skill.name
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            console.print(f"[green]✓[/green] Copied skill: {skill.name}")
        else:
            console.print(f"[yellow]![/yellow] Skill not found: {skill.name} (source: {skill.source})")


def _apply_agents(profile, project: Path, dry_run: bool) -> None:
    """Apply agents to project"""
    import shutil

    agents_dir = project / ".claude" / "agents"
    global_agents_dir = Path.home() / ".claude" / "agents"

    if dry_run:
        console.print(f"[dim]Would copy agents to:[/dim] {agents_dir}")
        return

    agents_dir.mkdir(parents=True, exist_ok=True)

    for agent in profile.agents:
        # Find agent source
        if agent.source == "global":
            src = global_agents_dir / f"{agent.name}.md"
        elif agent.source == "project":
            continue  # Already in project
        else:
            console.print(f"[yellow]![/yellow] Agent source '{agent.source}' not supported yet for {agent.name}")
            continue

        if src.exists():
            dst = agents_dir / f"{agent.name}.md"
            shutil.copy2(src, dst)
            console.print(f"[green]✓[/green] Copied agent: {agent.name}")
        else:
            console.print(f"[yellow]![/yellow] Agent not found: {agent.name} at {src}")