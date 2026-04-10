"""
Configuration merger for ccenv
"""

import json
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class ConfigMerger:
    """Merges ccenv profiles with Claude Code configurations."""

    SETTINGS_FILE = ".claude/settings.json"
    MCP_FILE = ".mcp.json"
    SKILLS_DIR = ".claude/skills"
    AGENTS_DIR = ".claude/agents"

    def apply_profile(
        self,
        project_path: Path,
        profile: Dict[str, Any],
        scope: str = "project",
        force: bool = False
    ) -> None:
        """Apply a profile to a project.

        Args:
            project_path: Target project directory
            profile: Profile data to apply
            scope: 'project' or 'user'
            force: Overwrite existing configuration
        """
        mode = profile.get("mode", "overlay")

        # Apply plugins
        if "plugins" in profile:
            self._apply_plugins(project_path, profile["plugins"], mode, force)

        # Apply MCP servers
        if "mcp" in profile:
            self._apply_mcp(project_path, profile["mcp"], mode, force)

        # Apply skills
        if "skills" in profile:
            self._apply_skills(project_path, profile["skills"])

        # Apply agents
        if "agents" in profile:
            self._apply_agents(project_path, profile["agents"])

    def _apply_plugins(
        self,
        project_path: Path,
        plugins: Dict[str, Any],
        mode: str,
        force: bool
    ) -> None:
        """Apply plugin configuration."""
        settings_path = project_path / self.SETTINGS_FILE
        settings = {}

        if settings_path.exists() and mode == "overlay":
            with open(settings_path, "r") as f:
                settings = json.load(f)

        enabled = settings.get("enabledPlugins", {})

        # Add plugins
        for plugin in plugins.get("add", []):
            enabled[plugin] = True

        # Remove plugins
        for plugin in plugins.get("remove", []):
            enabled.pop(plugin, None)

        settings["enabledPlugins"] = enabled

        settings_path.parent.mkdir(parents=True, exist_ok=True)
        with open(settings_path, "w") as f:
            json.dump(settings, f, indent=2)

    def _apply_mcp(
        self,
        project_path: Path,
        mcp: Dict[str, Any],
        mode: str,
        force: bool
    ) -> None:
        """Apply MCP server configuration."""
        mcp_path = project_path / self.MCP_FILE
        mcp_config = {}

        if mcp_path.exists() and mode == "overlay":
            with open(mcp_path, "r") as f:
                mcp_config = json.load(f)

        servers = mcp_config.get("mcpServers", {})

        for name, config in mcp.items():
            servers[name] = config

        mcp_config["mcpServers"] = servers

        with open(mcp_path, "w") as f:
            json.dump(mcp_config, f, indent=2)

    def _apply_skills(self, project_path: Path, skills: list) -> None:
        """Apply skills configuration."""
        # Skills are referenced in settings, actual files would need to be copied
        pass

    def _apply_agents(self, project_path: Path, agents: list) -> None:
        """Apply agents configuration."""
        # Agents are referenced in settings, actual files would need to be copied
        pass

    def extract_config(self, project_path: Path) -> Dict[str, Any]:
        """Extract configuration from a project.

        Args:
            project_path: Source project directory

        Returns:
            Extracted configuration dictionary
        """
        config = {
            "version": "1.0",
        }

        # Extract plugins
        settings_path = project_path / self.SETTINGS_FILE
        if settings_path.exists():
            with open(settings_path, "r") as f:
                settings = json.load(f)
            enabled = settings.get("enabledPlugins", {})
            if enabled:
                config["plugins"] = {"add": list(enabled.keys())}

        # Extract MCP servers
        mcp_path = project_path / self.MCP_FILE
        if mcp_path.exists():
            with open(mcp_path, "r") as f:
                mcp_config = json.load(f)
            servers = mcp_config.get("mcpServers", {})
            if servers:
                config["mcp"] = servers

        return config

    def create_backup(self, project_path: Path) -> Path:
        """Create backup of existing configuration.

        Args:
            project_path: Project directory

        Returns:
            Path to backup directory
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = project_path / ".claude" / "backups" / timestamp

        settings_path = project_path / self.SETTINGS_FILE
        mcp_path = project_path / self.MCP_FILE

        if settings_path.exists() or mcp_path.exists():
            backup_dir.mkdir(parents=True, exist_ok=True)

            if settings_path.exists():
                shutil.copy2(settings_path, backup_dir / "settings.json")

            if mcp_path.exists():
                shutil.copy2(mcp_path, backup_dir / ".mcp.json")

        return backup_dir