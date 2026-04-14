"""
Pytest configuration for ccenv tests
"""

import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_profiles_dir():
    """Create a temporary directory for test profiles"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        project = Path(tmpdir)
        (project / ".claude").mkdir()
        yield project


@pytest.fixture
def sample_profile_yaml():
    """Sample profile YAML content"""
    return """
name: test-profile
version: "1.0"
description: Test profile for unit tests
mode: overlay

plugins:
  add:
    - superpowers
    - plan
  remove:
    - github

mcp:
  test-server:
    source: "npm:test-mcp-server"
    type: stdio

skills:
  - name: test-skill
    source: global
    version: "1.0"

agents:
  - name: test-agent
    source: global
    model: claude-sonnet-4-6

env:
  TEST_VAR: "test_value"
"""