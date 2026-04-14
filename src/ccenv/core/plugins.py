"""
Plugin handling module for ccenv
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
import json


class PluginManager:
    """
    Plugin manager for enabling/disabling Claude Code plugins

    Note: Claude Code uses a dict format for enabledPlugins:
    {
        "plugin-name@marketplace": true,
        "another-plugin@marketplace": true
    }
    """

    # Claude Code settings file locations
    USER_SETTINGS = Path.home() / ".claude" / "settings.json"
    PROJECT_SETTINGS = Path(".claude") / "settings.json"

    # Default marketplace
    DEFAULT_MARKETPLACE = "claude-plugins-official"

    def __init__(self, project_path: Optional[Path] = None):
        self.project_path = project_path

    def get_settings_path(self, scope: str = "project") -> Path:
        """Get settings file path for given scope"""
        if scope == "project" and self.project_path:
            return self.project_path / self.PROJECT_SETTINGS
        elif scope == "user":
            return self.USER_SETTINGS
        else:
            raise ValueError(f"Invalid scope: {scope}")

    def load_settings(self, scope: str = "project") -> Dict[str, Any]:
        """Load settings from file"""
        path = self.get_settings_path(scope)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_settings(self, settings: Dict[str, Any], scope: str = "project") -> None:
        """Save settings to file"""
        path = self.get_settings_path(scope)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)

    def get_enabled_plugins(self, scope: str = "project") -> Dict[str, bool]:
        """Get dict of enabled plugins"""
        settings = self.load_settings(scope)
        enabled = settings.get("enabledPlugins", {})
        # Handle legacy array format by converting to dict
        if isinstance(enabled, list):
            return {p: True for p in enabled}
        return enabled

    def get_enabled_plugin_names(self, scope: str = "project") -> List[str]:
        """Get list of enabled plugin names (without marketplace)"""
        enabled = self.get_enabled_plugins(scope)
        return [key.split("@")[0] for key in enabled.keys() if enabled.get(key)]

    def normalize_plugin_name(self, plugin: str) -> str:
        """
        Normalize plugin name to full format: plugin-name@marketplace

        Examples:
            "superpowers" -> "superpowers@claude-plugins-official"
            "superpowers@claude-plugins-official" -> "superpowers@claude-plugins-official"
            "omc-setup@omc" -> "omc-setup@omc"
        """
        if "@" in plugin:
            return plugin
        return f"{plugin}@{self.DEFAULT_MARKETPLACE}"

    def enable_plugin(self, plugin: str, scope: str = "project") -> None:
        """Enable a plugin"""
        settings = self.load_settings(scope)
        enabled = settings.get("enabledPlugins", {})

        # Handle legacy array format
        if isinstance(enabled, list):
            enabled = {p: True for p in enabled}

        full_name = self.normalize_plugin_name(plugin)
        enabled[full_name] = True
        settings["enabledPlugins"] = enabled
        self.save_settings(settings, scope)

    def disable_plugin(self, plugin: str, scope: str = "project") -> None:
        """Disable a plugin"""
        settings = self.load_settings(scope)
        enabled = settings.get("enabledPlugins", {})

        # Handle legacy array format
        if isinstance(enabled, list):
            enabled = {p: True for p in enabled}

        full_name = self.normalize_plugin_name(plugin)
        if full_name in enabled:
            enabled[full_name] = False
        else:
            # Try without marketplace
            plugin_name = plugin.split("@")[0]
            for key in list(enabled.keys()):
                if key.split("@")[0] == plugin_name:
                    enabled[key] = False

        settings["enabledPlugins"] = enabled
        self.save_settings(settings, scope)

    def merge_plugins(
        self,
        plugins_to_add: List[str],
        plugins_to_remove: List[str],
        mode: str = "overlay",
        scope: str = "project"
    ) -> Dict[str, bool]:
        """
        Merge plugins with existing settings

        Args:
            plugins_to_add: Plugins to enable
            plugins_to_remove: Plugins to disable
            mode: 'overlay' (merge with existing) or 'replace' (replace existing)
            scope: 'project' or 'user'

        Returns:
            Final dict of enabled plugins
        """
        settings = self.load_settings(scope)

        if mode == "replace":
            # Replace mode: only use plugins_to_add
            enabled = {}
            for plugin in plugins_to_add:
                full_name = self.normalize_plugin_name(plugin)
                enabled[full_name] = True
            settings["enabledPlugins"] = enabled
            self.save_settings(settings, scope)
            return enabled

        # Overlay mode: merge with existing
        enabled = settings.get("enabledPlugins", {})

        # Handle legacy array format
        if isinstance(enabled, list):
            enabled = {p: True for p in enabled}

        # Add plugins
        for plugin in plugins_to_add:
            full_name = self.normalize_plugin_name(plugin)
            enabled[full_name] = True

        # Remove plugins
        for plugin in plugins_to_remove:
            full_name = self.normalize_plugin_name(plugin)
            if full_name in enabled:
                enabled[full_name] = False
            else:
                # Try without marketplace
                plugin_name = plugin.split("@")[0]
                for key in list(enabled.keys()):
                    if key.split("@")[0] == plugin_name:
                        enabled[key] = False

        settings["enabledPlugins"] = enabled
        self.save_settings(settings, scope)

        return {k: v for k, v in enabled.items() if v}