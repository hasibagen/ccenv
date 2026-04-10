"""
ccenv CLI main module
"""

import click
from pathlib import Path
from typing import Optional

from ..core.profile import ProfileManager
from ..core.merger import ConfigMerger
from ..core.resolver import MCPResolver


@click.group()
@click.version_option(version="1.0.0", prog_name="ccenv")
def cli():
    """ccenv - Claude Code Environment Manager

    A conda-like profile manager for Claude Code configurations.
    """
    pass


@cli.command()
@click.option("-n", "--name", required=True, help="Profile name")
@click.option("-d", "--description", default="", help="Profile description")
@click.option("-p", "--plugin", multiple=True, help="Plugin to add (format: name@marketplace)")
@click.option("--mcp", multiple=True, help="MCP server spec (format: name:source)")
@click.option("--skill", multiple=True, help="Skill to add")
@click.option("--agent", multiple=True, help="Agent to add")
@click.option("--mode", type=click.Choice(["overlay", "replace"]), default="overlay", help="Merge mode")
def create(name: str, description: str, plugin: tuple, mcp: tuple, skill: tuple, agent: tuple, mode: str):
    """Create a new ccenv profile."""
    manager = ProfileManager()

    profile_data = {
        "name": name,
        "version": "1.0",
        "description": description,
        "mode": mode,
    }

    if plugin:
        profile_data["plugins"] = {"add": list(plugin)}
    if mcp:
        profile_data["mcp"] = {}
        for spec in mcp:
            parts = spec.split(":", 1)
            if len(parts) == 2:
                profile_data["mcp"][parts[0]] = {"source": parts[1]}
    if skill:
        profile_data["skills"] = [{"name": s, "source": "global"} for s in skill]
    if agent:
        profile_data["agents"] = [{"name": a, "source": "global"} for a in agent]

    manager.create_profile(name, profile_data)
    click.echo(f"✓ Profile '{name}' created successfully")


@cli.command("list")
@click.option("--format", "fmt", type=click.Choice(["table", "json"]), default="table", help="Output format")
def list_profiles(fmt: str):
    """List all available ccenv profiles."""
    manager = ProfileManager()
    profiles = manager.list_profiles()

    if not profiles:
        click.echo("No profiles found. Create one with: ccenv create -n <name>")
        return

    if fmt == "json":
        import json
        click.echo(json.dumps(profiles, indent=2))
    else:
        click.echo("\nccenv Profiles")
        click.echo("=" * 50)
        click.echo(f"{'NAME':<15} {'DESCRIPTION':<30} {'MODIFIED':<12}")
        click.echo("-" * 50)
        for p in profiles:
            click.echo(f"{p['name']:<15} {p.get('description', '')[:28]:<30} {p.get('modified', 'N/A'):<12}")
        click.echo(f"\n{len(profiles)} profiles found")


@cli.command()
@click.argument("name")
@click.option("--format", "fmt", type=click.Choice(["table", "json", "yaml"]), default="table", help="Output format")
@click.option("--raw", is_flag=True, help="Show raw YAML content")
def show(name: str, fmt: str, raw: bool):
    """Show details of a specific profile."""
    manager = ProfileManager()
    profile = manager.get_profile(name)

    if not profile:
        click.echo(f"Profile '{name}' not found", err=True)
        raise SystemExit(1)

    if raw:
        click.echo(manager.get_raw_yaml(name))
    elif fmt == "json":
        import json
        click.echo(json.dumps(profile, indent=2))
    elif fmt == "yaml":
        import yaml
        click.echo(yaml.dump(profile, default_flow_style=False))
    else:
        click.echo(f"\nProfile: {name}")
        click.echo("=" * 50)
        click.echo(f"Name:        {profile.get('name', 'N/A')}")
        click.echo(f"Version:     {profile.get('version', 'N/A')}")
        click.echo(f"Description: {profile.get('description', 'N/A')}")
        click.echo(f"Mode:        {profile.get('mode', 'overlay')}")

        if "plugins" in profile:
            click.echo("\nPlugins:")
            for p in profile["plugins"].get("add", []):
                click.echo(f"  + {p}")
            for p in profile["plugins"].get("remove", []):
                click.echo(f"  - {p}")

        if "mcp" in profile:
            click.echo("\nMCP Servers:")
            for name, config in profile["mcp"].items():
                click.echo(f"  {name}: {config.get('source', 'N/A')}")


@cli.command()
@click.argument("name")
@click.argument("path", type=click.Path(), default=".")
@click.option("--scope", type=click.Choice(["project", "user"]), default="project", help="Apply scope")
@click.option("--force", is_flag=True, help="Overwrite existing configuration")
@click.option("--dry-run", is_flag=True, help="Preview changes without writing")
@click.option("--backup", is_flag=True, help="Create backup of existing configuration")
def use(name: str, path: str, scope: str, force: bool, dry_run: bool, backup: bool):
    """Apply a profile to a project directory."""
    manager = ProfileManager()
    merger = ConfigMerger()

    profile = manager.get_profile(name)
    if not profile:
        click.echo(f"Profile '{name}' not found", err=True)
        raise SystemExit(1)

    project_path = Path(path).resolve()

    if dry_run:
        click.echo(f"[DRY RUN] Would apply profile '{name}' to {project_path}")
        click.echo(f"Mode: {profile.get('mode', 'overlay')}")
        if "plugins" in profile:
            click.echo(f"Plugins: {profile['plugins'].get('add', [])}")
        if "mcp" in profile:
            click.echo(f"MCP servers: {list(profile['mcp'].keys())}")
        return

    if backup:
        merger.create_backup(project_path)

    merger.apply_profile(project_path, profile, scope, force)
    click.echo(f"✓ Profile '{name}' applied to {project_path}")


@cli.command()
@click.argument("path", type=click.Path(), default=".")
@click.option("-n", "--name", required=True, help="Profile name")
@click.option("--update", is_flag=True, help="Update existing profile")
@click.option("-d", "--description", default="", help="Profile description")
@click.option("--mode", type=click.Choice(["overlay", "replace"]), default="overlay", help="Merge mode")
def extract(path: str, name: str, update: bool, description: str, mode: str):
    """Extract configuration from a project to create a profile."""
    manager = ProfileManager()
    merger = ConfigMerger()

    project_path = Path(path).resolve()

    if not update and manager.profile_exists(name):
        click.echo(f"Profile '{name}' already exists. Use --update to overwrite.", err=True)
        raise SystemExit(1)

    config = merger.extract_config(project_path)
    config["name"] = name
    config["description"] = description
    config["mode"] = mode

    manager.create_profile(name, config, overwrite=update)
    click.echo(f"✓ Profile '{name}' {'updated' if update else 'created'} from {project_path}")


if __name__ == "__main__":
    cli()