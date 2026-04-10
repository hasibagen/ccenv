"""
Validators for ccenv
"""

import re
from pathlib import Path
from typing import Tuple


def validate_profile_name(name: str) -> Tuple[bool, str]:
    """Validate a profile name.

    Args:
        name: Profile name to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "Profile name cannot be empty"

    if not re.match(r"^[a-z][a-z0-9-]*$", name):
        return False, "Profile name must start with lowercase letter and contain only lowercase letters, numbers, and hyphens"

    if len(name) > 50:
        return False, "Profile name must be 50 characters or less"

    return True, ""


def validate_path(path: Path, must_exist: bool = True) -> Tuple[bool, str]:
    """Validate a file path.

    Args:
        path: Path to validate
        must_exist: Whether the path must exist

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        resolved = path.resolve()
    except Exception as e:
        return False, f"Invalid path: {e}"

    if must_exist and not resolved.exists():
        return False, f"Path does not exist: {resolved}"

    # Check for path traversal
    if ".." in str(path):
        return False, "Path traversal not allowed"

    return True, ""