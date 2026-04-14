"""
Tests for ccenv Profile management
"""

import pytest
from pathlib import Path

from ccenv.core.profile import (
    Profile,
    ProfileManager,
    PluginConfig,
    MCPServerConfig,
    SkillConfig,
    AgentConfig,
)
from ccenv.utils.yaml_utils import load_yaml, save_yaml


class TestProfileModel:
    """Profile Pydantic model tests"""

    def test_create_minimal_profile(self):
        """Test creating a minimal profile"""
        profile = Profile(name="test")
        assert profile.name == "test"
        assert profile.version == "1.0"
        assert profile.mode == "overlay"

    def test_create_full_profile(self):
        """Test creating a profile with all fields"""
        profile = Profile(
            name="full-test",
            version="2.0",
            description="Full test profile",
            mode="replace",
            plugins=PluginConfig(add=["plugin1"], remove=["plugin2"]),
            mcp={"server1": MCPServerConfig(source="npm:pkg")},
            skills=[SkillConfig(name="skill1")],
            agents=[AgentConfig(name="agent1", model="opus")],
            env={"VAR": "value"},
        )

        assert profile.name == "full-test"
        assert profile.mode == "replace"
        assert len(profile.plugins.add) == 1
        assert len(profile.mcp) == 1
        assert len(profile.skills) == 1
        assert len(profile.agents) == 1

    def test_invalid_profile_name(self):
        """Test that invalid profile names raise error"""
        with pytest.raises(Exception):  # Pydantic ValidationError
            Profile(name="invalid name!")

    def test_invalid_mode(self):
        """Test that invalid mode raises error"""
        with pytest.raises(Exception):  # Pydantic ValidationError
            Profile(name="test", mode="invalid")

    def test_to_yaml_dict(self):
        """Test converting profile to YAML dict"""
        profile = Profile(
            name="yaml-test",
            description="YAML test",
            plugins=PluginConfig(add=["p1"]),
        )

        data = profile.to_yaml_dict()
        assert data["name"] == "yaml-test"
        assert data["description"] == "YAML test"
        assert data["plugins"]["add"] == ["p1"]


class TestProfileManager:
    """ProfileManager tests"""

    def test_list_profiles_empty(self, tmp_path):
        """Test listing profiles when empty"""
        manager = ProfileManager(profiles_dir=tmp_path)
        assert manager.list_profiles() == []

    def test_save_and_load_profile(self, tmp_path):
        """Test saving and loading a profile"""
        manager = ProfileManager(profiles_dir=tmp_path)

        profile = Profile(
            name="save-test",
            description="Test saving",
        )

        # Save
        path = manager.save_profile(profile)
        assert path.exists()

        # Load
        loaded = manager.load_profile("save-test")
        assert loaded.name == "save-test"
        assert loaded.description == "Test saving"

    def test_profile_exists(self, tmp_path):
        """Test checking if profile exists"""
        manager = ProfileManager(profiles_dir=tmp_path)

        assert not manager.profile_exists("nonexistent")

        profile = Profile(name="exists-test")
        manager.save_profile(profile)

        assert manager.profile_exists("exists-test")

    def test_delete_profile(self, tmp_path):
        """Test deleting a profile"""
        manager = ProfileManager(profiles_dir=tmp_path)

        profile = Profile(name="delete-test")
        manager.save_profile(profile)

        assert manager.profile_exists("delete-test")

        manager.delete_profile("delete-test")
        assert not manager.profile_exists("delete-test")


class TestYAMLUtils:
    """YAML utility tests"""

    def test_save_and_load_yaml(self, tmp_path):
        """Test saving and loading YAML files"""
        data = {
            "name": "yaml-test",
            "version": "1.0",
            "nested": {"key": "value"},
            "list": [1, 2, 3],
        }

        path = tmp_path / "test.yml"
        save_yaml(path, data)

        loaded = load_yaml(path)
        assert loaded == data

    def test_load_nonexistent_yaml(self, tmp_path):
        """Test loading non-existent YAML file"""
        with pytest.raises(FileNotFoundError):
            load_yaml(tmp_path / "nonexistent.yml")