"""
Tests for ccenv CLI
"""

import pytest
import uuid
from pathlib import Path
from click.testing import CliRunner

from ccenv.cli import main


@pytest.fixture
def runner():
    """CLI test runner"""
    return CliRunner()


@pytest.fixture
def unique_name():
    """Generate unique profile name for each test"""
    return f"test-{uuid.uuid4().hex[:8]}"


class TestCLI:
    """CLI command tests"""

    def test_version(self, runner):
        """Test --version flag"""
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "ccenv" in result.output

    def test_help(self, runner):
        """Test --help flag"""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "ccenv" in result.output.lower()
        assert "create" in result.output
        assert "list" in result.output
        assert "show" in result.output
        assert "use" in result.output

    def test_create_profile(self, runner, unique_name):
        """Test create command"""
        result = runner.invoke(main, [
            "create",
            "-n", unique_name,
            "-d", "Test description"
        ])

        assert result.exit_code == 0, f"Output: {result.output}"
        assert "Created profile" in result.output

    def test_list_profiles(self, runner, unique_name):
        """Test list command"""
        # First create a profile
        runner.invoke(main, ["create", "-n", unique_name, "-d", "Test"])

        result = runner.invoke(main, ["list"])
        assert result.exit_code == 0

    def test_show_profile_not_found(self, runner):
        """Test show command with non-existent profile"""
        result = runner.invoke(main, ["show", "nonexistent-profile-xyz"])
        assert result.exit_code != 0
        assert "not found" in result.output.lower()

    def test_show_profile(self, runner, unique_name):
        """Test show command"""
        # First create a profile
        runner.invoke(main, ["create", "-n", unique_name, "-d", "Test description"])

        result = runner.invoke(main, ["show", unique_name])
        assert result.exit_code == 0
        assert unique_name in result.output


class TestProfileCommands:
    """Profile command tests"""

    def test_create_with_mcp(self, runner, unique_name):
        """Test create with MCP configuration"""
        result = runner.invoke(main, [
            "create",
            "-n", unique_name,
            "-d", "MCP test profile",
            "--mcp", "server1:npm:pkg1"
        ])

        assert result.exit_code == 0, f"Output: {result.output}"

    def test_create_with_plugins(self, runner, unique_name):
        """Test create with plugins"""
        result = runner.invoke(main, [
            "create",
            "-n", unique_name,
            "-d", "Plugin test profile",
            "-p", "superpowers",
            "-p", "plan"
        ])

        assert result.exit_code == 0, f"Output: {result.output}"

    def test_create_with_skill(self, runner, unique_name):
        """Test create with skill"""
        result = runner.invoke(main, [
            "create",
            "-n", unique_name,
            "-d", "Skill test profile",
            "--skill", "test-skill"
        ])

        assert result.exit_code == 0, f"Output: {result.output}"

    def test_create_with_agent(self, runner, unique_name):
        """Test create with agent"""
        result = runner.invoke(main, [
            "create",
            "-n", unique_name,
            "-d", "Agent test profile",
            "--agent", "test-agent"
        ])

        assert result.exit_code == 0, f"Output: {result.output}"