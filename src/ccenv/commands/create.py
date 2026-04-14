"""
Create command - Create a new ccenv profile
"""

from pathlib import Path
from typing import Optional
import click
from rich.console import Console
from rich.prompt import Prompt

from ccenv.core.profile import Profile, ProfileManager, PluginConfig, MCPServerConfig, SkillConfig, AgentConfig
from ccenv.utils.validation import validate_profile_name, get_validation_errors


console = Console()


@click.command()
@click.option("-n", "--name", help="Profile name")
@click.option("-f", "--file", "file_path", type=click.Path(exists=True), help="Create from existing YAML file")
@click.option("--description", "-d", help="Profile description")
@click.option("--mode", type=click.Choice(["overlay", "replace"]), default="overlay", help="Merge mode")
@click.option("--plugin", "-p", multiple=True, help="Plugin to enable (can be used multiple times)")
@click.option("--mcp", multiple=True, help="MCP server to add (format: name:source)")
@click.option("--skill", multiple=True, help="Skill to add (format: name or name:source)")
@click.option("--agent", multiple=True, help="Agent to add (format: name or name:source)")
@click.pass_context
def create(
    ctx: click.Context,
    name: Optional[str],
    file_path: Optional[str],
    description: Optional[str],
    mode: str,
    plugin: tuple,
    mcp: tuple,
    skill: tuple,
    agent: tuple,
) -> None:
    """
    Create a new ccenv profile.

    Examples:
        ccenv create -n eeg --description "EEG analysis environment"
        ccenv create -n meta --plugin superpowers --mcp matlab:local:${MATLAB_MCP_PATH}
        ccenv create -f existing.yml -n new-profile
    """
    manager = ProfileManager()

    # If file provided, load from file
    if file_path:
        from ccenv.utils.yaml_utils import load_yaml
        data = load_yaml(Path(file_path))
        if name:
            data["name"] = name
        profile = Profile(**data)
        manager.save_profile(profile)
        console.print(f"[green]✓[/green] Created profile '{profile.name}' from {file_path}")
        return

    # Interactive mode if no name provided
    if not name:
        name = Prompt.ask("Profile name")

    # Validate name
    if not validate_profile_name(name):
        console.print(f"[red]✗[/red] Invalid profile name: {name}")
        console.print("  Use only alphanumeric characters, dashes, and underscores")
        raise SystemExit(1)

    # Check if profile already exists
    if manager.profile_exists(name):
        console.print(f"[red]✗[/red] Profile '{name}' already exists")
        raise SystemExit(1)

    # Interactive prompts for missing info
    if not description:
        description = Prompt.ask("Description (optional)", default="")

    # Build profile
    plugins_config = None
    if plugin:
        plugins_config = PluginConfig(add=list(plugin))

    mcp_config = {}
    for mcp_str in mcp:
        if ":" in mcp_str:
            mcp_name, mcp_source = mcp_str.split(":", 1)
            mcp_config[mcp_name] = MCPServerConfig(source=mcp_source)
        else:
            console.print(f"[yellow]![/yellow] Invalid MCP format: {mcp_str}. Use name:source")

    skills_list = []
    for skill_str in skill:
        if ":" in skill_str:
            skill_name, skill_source = skill_str.split(":", 1)
            skills_list.append(SkillConfig(name=skill_name, source=skill_source))
        else:
            skills_list.append(SkillConfig(name=skill_str))

    agents_list = []
    for agent_str in agent:
        if ":" in agent_str:
            agent_name, agent_source = agent_str.split(":", 1)
            agents_list.append(AgentConfig(name=agent_name, source=agent_source))
        else:
            agents_list.append(AgentConfig(name=agent_str))

    profile = Profile(
        name=name,
        description=description,
        mode=mode,
        plugins=plugins_config,
        mcp=mcp_config,
        skills=skills_list,
        agents=agents_list,
    )

    # Save profile
    path = manager.save_profile(profile)
    console.print(f"[green]✓[/green] Created profile '{name}' at {path}")