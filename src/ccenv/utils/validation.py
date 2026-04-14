"""
Validation utilities for ccenv
"""

import re
from pathlib import Path
from typing import List, Optional


def validate_profile_name(name: str) -> bool:
    """
    Validate profile name format

    Args:
        name: Profile name to validate

    Returns:
        True if valid, False otherwise
    """
    if not name:
        return False

    # Only allow alphanumeric, dash, underscore
    pattern = r"^[\w-]+$"
    return bool(re.match(pattern, name))


def validate_mcp_source(source: str) -> bool:
    """
    Validate MCP source format

    Valid formats:
        - local:${ENV_VAR}
        - local:/absolute/path
        - marketplace:org/name
        - npm:package-name
        - pip:package-name

    Args:
        source: MCP source string

    Returns:
        True if valid, False otherwise
    """
    valid_prefixes = [
        "local:${",
        "marketplace:",
        "npm:",
        "pip:",
    ]

    for prefix in valid_prefixes:
        if source.startswith(prefix):
            return True

    # Allow absolute paths
    if source.startswith("/") or source.startswith("~"):
        return True

    # Allow relative paths (will be resolved later)
    return True


def validate_plugin_name(name: str) -> bool:
    """
    Validate plugin name format

    Args:
        name: Plugin name to validate

    Returns:
        True if valid, False otherwise
    """
    if not name:
        return False

    # Plugin names: alphanumeric, dash, underscore, colon (for org:name)
    pattern = r"^[\w:-]+$"
    return bool(re.match(pattern, name))


def validate_skill_name(name: str) -> bool:
    """
    Validate skill name format

    Args:
        name: Skill name to validate

    Returns:
        True if valid, False otherwise
    """
    if not name:
        return False

    # Skill names: alphanumeric, dash, underscore
    pattern = r"^[\w-]+$"
    return bool(re.match(pattern, name))


def validate_agent_name(name: str) -> bool:
    """
    Validate agent name format

    Args:
        name: Agent name to validate

    Returns:
        True if valid, False otherwise
    """
    if not name:
        return False

    # Agent names: alphanumeric, dash, underscore
    pattern = r"^[\w-]+$"
    return bool(re.match(pattern, name))


def validate_path(path: str) -> bool:
    """
    Validate path exists and is accessible

    Args:
        path: Path to validate

    Returns:
        True if path is valid, False otherwise
    """
    try:
        p = Path(path)
        # Expand ~ and environment variables
        p = p.expanduser()
        return True
    except Exception:
        return False


def validate_version(version: str) -> bool:
    """
    Validate version string (semver-like)

    Args:
        version: Version string to validate

    Returns:
        True if valid, False otherwise
    """
    if not version:
        return True  # Empty version is allowed (means latest)

    # Simple semver pattern: X.Y.Z or X.Y
    pattern = r"^(\d+)(\.\d+)?(\.\d+)?$"
    return bool(re.match(pattern, version))


def get_validation_errors(name: str, **fields) -> List[str]:
    """
    Get all validation errors for profile fields

    Args:
        name: Profile name
        fields: Additional fields to validate

    Returns:
        List of validation error messages
    """
    errors = []

    if not validate_profile_name(name):
        errors.append(f"Invalid profile name: {name}")

    for key, value in fields.items():
        if key == "mcp_sources":
            for source in value:
                if not validate_mcp_source(source):
                    errors.append(f"Invalid MCP source: {source}")

        elif key == "plugins":
            for plugin in value:
                if not validate_plugin_name(plugin):
                    errors.append(f"Invalid plugin name: {plugin}")

        elif key == "skills":
            for skill in value:
                if not validate_skill_name(skill):
                    errors.append(f"Invalid skill name: {skill}")

        elif key == "agents":
            for agent in value:
                if not validate_agent_name(agent):
                    errors.append(f"Invalid agent name: {agent}")

        elif key == "versions":
            for version in value:
                if not validate_version(version):
                    errors.append(f"Invalid version: {version}")

    return errors