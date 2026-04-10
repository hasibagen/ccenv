"""
Tests for ProfileManager
"""

import pytest
import tempfile
from pathlib import Path

from ccenv.core.profile import ProfileManager


class TestProfileManager:
    """Tests for ProfileManager class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = ProfileManager(Path(self.temp_dir))

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_profile(self):
        """Test creating a new profile."""
        self.manager.create_profile("test", {
            "name": "test",
            "description": "Test profile"
        })

        assert self.manager.profile_exists("test")

    def test_get_profile(self):
        """Test getting a profile."""
        self.manager.create_profile("test", {
            "name": "test",
            "description": "Test profile"
        })

        profile = self.manager.get_profile("test")
        assert profile is not None
        assert profile["name"] == "test"
        assert profile["description"] == "Test profile"

    def test_list_profiles(self):
        """Test listing profiles."""
        self.manager.create_profile("test1", {"name": "test1"})
        self.manager.create_profile("test2", {"name": "test2"})

        profiles = self.manager.list_profiles()
        assert len(profiles) == 2

    def test_delete_profile(self):
        """Test deleting a profile."""
        self.manager.create_profile("test", {"name": "test"})
        assert self.manager.profile_exists("test")

        self.manager.delete_profile("test")
        assert not self.manager.profile_exists("test")

    def test_get_nonexistent_profile(self):
        """Test getting a non-existent profile."""
        profile = self.manager.get_profile("nonexistent")
        assert profile is None