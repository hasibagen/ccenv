"""
Extract command - Extract configuration from project to profile
"""

from pathlib import Path
from typing import Optional, List, Dict
import json
import click
from rich.console import Console
from rich.table import Table

from ccenv.core.profile import Profile, ProfileManager, PluginConfig, MCPServerConfig, SkillConfig, AgentConfig
from ccenv.utils.mcp_utils import parse_mcp_json, extract_mcp_config


console = Console()


@click.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.option("-n", "--name", required=True, help="Profile name")
@click.option("-u", "--update", is_flag=True, help="Update existing profile instead of creating new")
@click.option("-d", "--description", help="Profile description")
@click.option("--mode", type=click.Choice(["overlay", "replace"]), default="overlay", help="Merge mode")
@click.pass_context
def extract(
    ctx: click.Context,
    project_path: str,
    name: str,
    update: bool,
    description: Optional[str],
    mode: str,
) -> None:
    """
    Extract configuration from a project to create or update a profile.

    Reads settings.json, .mcp.json, skills, and agents from the project
    and saves them as a ccenv profile.

    Examples:
        ccenv extract /path/to/project -n my-profile
        ccenv extract /path/to/project -n my-profile --update
        ccenv extract /path/to/project -n my-profile -d "My profile"
    """
    project = Path(project_path).resolve()
    manager = ProfileManager()

    # Check if profile exists
    if manager.profile_exists(name) and not update:
        console.print(f"[red]✗[/red] Profile '{name}' already exists. Use --update to overwrite.")
        raise SystemExit(1)

    console.print(f"[dim]Extracting configuration from:[/dim] {project}")

    # Extract plugins
    plugins_config = _extract_plugins(project)

    # Extract MCP
    mcp_config = _extract_mcp(project)

    # Extract skills
    skills_list = _extract_skills(project)

    # Extract agents
    agents_list = _extract_agents(project)

    # Build profile
    profile = Profile(
        name=name,
        description=description or f"Extracted from {project.name}",
        mode=mode,
        plugins=plugins_config,
        mcp=mcp_config,
        skills=skills_list,
        agents=agents_list,
    )

    # Save profile
    path = manager.save_profile(profile)

    # Show summary
    _show_summary(profile, project, update)


def _extract_plugins(project: Path) -> Optional[PluginConfig]:
    """Extract plugins from project settings.json"""
    settings_path = project / ".claude" / "settings.json"

    if not settings_path.exists():
        console.print("[dim]  No settings.json found[/dim]")
        return None

    with open(settings_path, "r", encoding="utf-8") as f:
        settings = json.load(f)

    enabled_plugins = settings.get("enabledPlugins", {})

    # Handle dict format {"plugin@marketplace": true}
    if isinstance(enabled_plugins, dict):
        add_list = [k for k, v in enabled_plugins.items() if v is True]
    # Handle legacy array format
    elif isinstance(enabled_plugins, list):
        add_list = enabled_plugins
    else:
        add_list = []

    if add_list:
        console.print(f"[green]  Found {len(add_list)} plugins[/green]")
        return PluginConfig(add=add_list)

    return None


def _extract_mcp(project: Path) -> Dict[str, MCPServerConfig]:
    """Extract MCP configuration from project .mcp.json"""
    mcp_path = project / ".mcp.json"

    if not mcp_path.exists():
        console.print("[dim]  No .mcp.json found[/dim]")
        return {}

    raw_mcp = parse_mcp_json(mcp_path)
    mcp_config = extract_mcp_config(raw_mcp)

    if mcp_config:
        console.print(f"[green]  Found {len(mcp_config)} MCP servers[/green]")
        return {
            name: MCPServerConfig(**config)
            for name, config in mcp_config.items()
        }

    return {}


def _extract_skills(project: Path) -> List[SkillConfig]:
    """Extract skills from project .claude/skills/"""
    skills_dir = project / ".claude" / "skills"
    skills_list = []

    if not skills_dir.exists():
        console.print("[dim]  No skills directory found[/dim]")
        return skills_list

    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir():
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                skills_list.append(SkillConfig(
                    name=skill_dir.name,
                    source="project"
                ))

    if skills_list:
        console.print(f"[green]  Found {len(skills_list)} skills[/green]")

    return skills_list


def _extract_agents(project: Path) -> List[AgentConfig]:
    """Extract agents from project .claude/agents/"""
    agents_dir = project / ".claude" / "agents"
    agents_list = []

    if not agents_dir.exists():
        console.print("[dim]  No agents directory found[/dim]")
        return agents_list

    for agent_file in agents_dir.glob("*.md"):
        agents_list.append(AgentConfig(
            name=agent_file.stem,
            source="project"
        ))

    if agents_list:
        console.print(f"[green]  Found {len(agents_list)} agents[/green]")

    return agents_list


def _show_summary(profile: Profile, project: Path, is_update: bool) -> None:
    """Show extraction summary"""
    action = "Updated" if is_update else "Created"
    console.print(f"\n[green]✓[/green] {action} profile '[cyan]{profile.name}[/cyan]'")

    table = Table(show_header=False, box=None)
    table.add_column("Key", style="dim")
    table.add_column("Value")

    table.add_row("Description:", profile.description)
    table.add_row("Mode:", profile.mode)

    if profile.plugins:
        table.add_row("Plugins:", str(len(profile.plugins.add)))

    if profile.mcp:
        table.add_row("MCP Servers:", str(len(profile.mcp)))

    if profile.skills:
        table.add_row("Skills:", str(len(profile.skills)))

    if profile.agents:
        table.add_row("Agents:", str(len(profile.agents)))

    console.print(table)
    console.print(f"\n[dim]Profile saved to: ~/.claude/ccenv/profiles.d/{profile.name}.yml[/dim]")