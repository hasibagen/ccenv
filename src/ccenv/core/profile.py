"""
Profile management module for ccenv
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, field_validator
import os

from ccenv.utils.yaml_utils import load_yaml, save_yaml


# Default ccenv directory
CCENV_DIR = Path.home() / ".claude" / "ccenv"
PROFILES_DIR = Path(os.environ.get("CCENV_PROFILES_DIR", str(CCENV_DIR / "profiles.d")))


class PluginConfig(BaseModel):
    """Plugin configuration"""
    add: List[str] = Field(default_factory=list)
    remove: List[str] = Field(default_factory=list)


class MCPServerConfig(BaseModel):
    """MCP server configuration"""
    source: str
    type: str = "stdio"
    args: List[str] = Field(default_factory=list)
    env: Dict[str, str] = Field(default_factory=dict)

    @field_validator("source")
    @classmethod
    def validate_source(cls, v: str) -> str:
        """Validate MCP source format"""
        valid_prefixes = ["local:", "marketplace:", "npm:", "pip:"]
        if not any(v.startswith(prefix) for prefix in valid_prefixes):
            if not Path(v).exists():
                # Allow plain paths for flexibility
                pass
        return v


class SkillConfig(BaseModel):
    """Skill configuration"""
    name: str
    source: str = "global"
    version: Optional[str] = None


class AgentConfig(BaseModel):
    """Agent configuration"""
    name: str
    source: str = "global"
    model: Optional[str] = None
    permission_mode: Optional[str] = None


class Profile(BaseModel):
    """
    Profile model for ccenv configuration

    A profile defines a set of MCP servers, plugins, skills, and agents
    that can be applied to a project.
    """
    name: str
    version: str = "1.0"
    description: str = ""
    mode: str = "overlay"  # overlay or replace

    plugins: Optional[PluginConfig] = None
    mcp: Dict[str, MCPServerConfig] = Field(default_factory=dict)
    skills: List[SkillConfig] = Field(default_factory=list)
    agents: List[AgentConfig] = Field(default_factory=list)
    env: Dict[str, str] = Field(default_factory=dict)
    hooks: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, v: str) -> str:
        """Validate merge mode"""
        if v not in ["overlay", "replace"]:
            raise ValueError(f"Invalid mode: {v}. Must be 'overlay' or 'replace'")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate profile name"""
        if not v:
            raise ValueError("Profile name cannot be empty")
        # Only allow alphanumeric, dash, underscore
        import re
        if not re.match(r"^[\w-]+$", v):
            raise ValueError(f"Invalid profile name: {v}. Use only alphanumeric, dash, underscore")
        return v

    def to_yaml_dict(self) -> Dict[str, Any]:
        """Convert to YAML-compatible dictionary"""
        data = {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "mode": self.mode,
        }

        if self.plugins:
            data["plugins"] = {
                "add": self.plugins.add,
                "remove": self.plugins.remove,
            }

        if self.mcp:
            data["mcp"] = {
                name: {
                    "source": config.source,
                    "type": config.type,
                    "args": config.args,
                    "env": config.env,
                }
                for name, config in self.mcp.items()
            }

        if self.skills:
            data["skills"] = [
                {
                    "name": skill.name,
                    "source": skill.source,
                    "version": skill.version,
                }
                for skill in self.skills
            ]

        if self.agents:
            data["agents"] = [
                {
                    "name": agent.name,
                    "source": agent.source,
                    "model": agent.model,
                    "permission_mode": agent.permission_mode,
                }
                for agent in self.agents
            ]

        if self.env:
            data["env"] = self.env

        if self.hooks:
            data["hooks"] = self.hooks

        return data


class ProfileManager:
    """
    Profile manager for loading, saving, and managing profiles
    """

    def __init__(self, profiles_dir: Optional[Path] = None):
        self.profiles_dir = profiles_dir or PROFILES_DIR
        self._ensure_dirs()

    def _ensure_dirs(self) -> None:
        """Ensure profile directories exist"""
        self.profiles_dir.mkdir(parents=True, exist_ok=True)

    def list_profiles(self) -> List[str]:
        """List all available profiles"""
        profiles = []
        for file in self.profiles_dir.glob("*.yml"):
            profiles.append(file.stem)
        for file in self.profiles_dir.glob("*.yaml"):
            if file.stem not in profiles:
                profiles.append(file.stem)
        return sorted(profiles)

    def load_profile(self, name: str) -> Profile:
        """Load a profile by name"""
        # Try both .yml and .yaml
        for ext in [".yml", ".yaml"]:
            path = self.profiles_dir / f"{name}{ext}"
            if path.exists():
                data = load_yaml(path)
                return Profile(**data)

        raise FileNotFoundError(f"Profile '{name}' not found in {self.profiles_dir}")

    def save_profile(self, profile: Profile) -> Path:
        """Save a profile to YAML file"""
        path = self.profiles_dir / f"{profile.name}.yml"
        data = profile.to_yaml_dict()
        save_yaml(path, data)
        return path

    def delete_profile(self, name: str) -> bool:
        """Delete a profile"""
        for ext in [".yml", ".yaml"]:
            path = self.profiles_dir / f"{name}{ext}"
            if path.exists():
                path.unlink()
                return True
        return False

    def profile_exists(self, name: str) -> bool:
        """Check if a profile exists"""
        for ext in [".yml", ".yaml"]:
            path = self.profiles_dir / f"{name}{ext}"
            if path.exists():
                return True
        return False

    def get_profile_path(self, name: str) -> Optional[Path]:
        """Get the path to a profile file"""
        for ext in [".yml", ".yaml"]:
            path = self.profiles_dir / f"{name}{ext}"
            if path.exists():
                return path
        return None