"""
Tests for ccenv validation utilities
"""

import pytest

from ccenv.utils.validation import (
    validate_profile_name,
    validate_mcp_source,
    validate_plugin_name,
    validate_skill_name,
    validate_agent_name,
    validate_version,
    get_validation_errors,
)


class TestValidation:
    """Validation function tests"""

    def test_valid_profile_names(self):
        """Test valid profile names"""
        assert validate_profile_name("test")
        assert validate_profile_name("test-profile")
        assert validate_profile_name("test_profile")
        assert validate_profile_name("Test123")
        assert validate_profile_name("123test")

    def test_invalid_profile_names(self):
        """Test invalid profile names"""
        assert not validate_profile_name("")
        assert not validate_profile_name("test profile")
        assert not validate_profile_name("test!")
        assert not validate_profile_name("test@name")

    def test_valid_mcp_sources(self):
        """Test valid MCP source formats"""
        assert validate_mcp_source("local:${MATLAB_MCP_PATH}")
        assert validate_mcp_source("marketplace:org/name")
        assert validate_mcp_source("npm:@playwright/mcp")
        assert validate_mcp_source("pip:mcp-server")
        assert validate_mcp_source("/absolute/path")
        assert validate_mcp_source("~/home/path")

    def test_valid_plugin_names(self):
        """Test valid plugin names"""
        assert validate_plugin_name("superpowers")
        assert validate_plugin_name("plan")
        assert validate_plugin_name("org:plugin")

    def test_valid_skill_names(self):
        """Test valid skill names"""
        assert validate_skill_name("eeg-analysis")
        assert validate_skill_name("meta_analysis")
        assert validate_skill_name("skill123")

    def test_valid_agent_names(self):
        """Test valid agent names"""
        assert validate_agent_name("researcher")
        assert validate_agent_name("test-agent")
        assert validate_agent_name("agent_123")

    def test_valid_versions(self):
        """Test valid version strings"""
        assert validate_version("")
        assert validate_version("1")
        assert validate_version("1.0")
        assert validate_version("1.0.0")
        assert validate_version("2.3.4")

    def test_get_validation_errors(self):
        """Test getting validation errors"""
        errors = get_validation_errors("valid-name")
        assert len(errors) == 0

        errors = get_validation_errors("invalid name!")
        assert len(errors) == 1
        assert "Invalid profile name" in errors[0]