"""
Profile management for ccenv
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class ProfileManager:
    """Manages ccenv profiles stored as YAML files."""

    def __init__(self, base_dir: Optional[Path] = None):
        """Initialize the profile manager.

        Args:
            base_dir: Base directory for profiles. Defaults to ~/.claude/ccenv/
        """
        if base_dir is None:
            base_dir = Path.home() / ".claude" / "ccenv"
        self.base_dir = base_dir
        self.profiles_dir = base_dir / "profiles.d"
        self._ensure_dirs()

    def _ensure_dirs(self) -> None:
        """Ensure required directories exist."""
        self.profiles_dir.mkdir(parents=True, exist_ok=True)

    def list_profiles(self) -> List[Dict[str, Any]]:
        """List all available profiles.

        Returns:
            List of profile metadata dictionaries
        """
        profiles = []
        for profile_file in self.profiles_dir.glob("*.yml"):
            try:
                profile = self.get_profile(profile_file.stem)
                if profile:
                    profile["modified"] = datetime.fromtimestamp(
                        profile_file.stat().st_mtime
                    ).strftime("%Y-%m-%d")
                    profiles.append(profile)
            except Exception:
                continue
        return profiles

    def get_profile(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific profile by name.

        Args:
            name: Profile name

        Returns:
            Profile dictionary or None if not found
        """
        profile_path = self.profiles_dir / f"{name}.yml"
        if not profile_path.exists():
            return None

        with open(profile_path, "r") as f:
            return yaml.safe_load(f)

    def get_raw_yaml(self, name: str) -> str:
        """Get raw YAML content of a profile.

        Args:
            name: Profile name

        Returns:
            Raw YAML string
        """
        profile_path = self.profiles_dir / f"{name}.yml"
        with open(profile_path, "r") as f:
            return f.read()

    def create_profile(self, name: str, data: Dict[str, Any], overwrite: bool = False) -> Path:
        """Create or update a profile.

        Args:
            name: Profile name
            data: Profile data
            overwrite: Whether to overwrite existing profile

        Returns:
            Path to created profile file
        """
        profile_path = self.profiles_dir / f"{name}.yml"

        if profile_path.exists() and not overwrite:
            raise FileExistsError(f"Profile '{name}' already exists")

        with open(profile_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

        return profile_path

    def profile_exists(self, name: str) -> bool:
        """Check if a profile exists.

        Args:
            name: Profile name

        Returns:
            True if profile exists
        """
        return (self.profiles_dir / f"{name}.yml").exists()

    def delete_profile(self, name: str) -> bool:
        """Delete a profile.

        Args:
            name: Profile name

        Returns:
            True if profile was deleted
        """
        profile_path = self.profiles_dir / f"{name}.yml"
        if profile_path.exists():
            profile_path.unlink()
            return True
        return False