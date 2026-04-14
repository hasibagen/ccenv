"""
YAML utilities for ccenv - safe loading and saving
"""

from pathlib import Path
from typing import Any, Dict
import yaml


def load_yaml(path: Path) -> Dict[str, Any]:
    """
    Safely load YAML file

    Args:
        path: Path to YAML file

    Returns:
        Dictionary with YAML contents

    Raises:
        FileNotFoundError: If file doesn't exist
        yaml.YAMLError: If YAML parsing fails
    """
    if not path.exists():
        raise FileNotFoundError(f"YAML file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        # Use safe_load to prevent code execution vulnerabilities
        data = yaml.safe_load(f)

    if data is None:
        return {}

    if not isinstance(data, dict):
        raise yaml.YAMLError(f"YAML content must be a dictionary, got {type(data)}")

    return data


def save_yaml(path: Path, data: Dict[str, Any]) -> None:
    """
    Save data to YAML file with consistent formatting

    Args:
        path: Path to YAML file
        data: Dictionary to save
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(
            data,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            indent=2,
        )


def validate_yaml_content(content: str) -> Dict[str, Any]:
    """
    Validate YAML content string

    Args:
        content: YAML content as string

    Returns:
        Dictionary with parsed contents

    Raises:
        yaml.YAMLError: If YAML parsing fails
    """
    data = yaml.safe_load(content)

    if data is None:
        return {}

    if not isinstance(data, dict):
        raise yaml.YAMLError(f"YAML content must be a dictionary, got {type(data)}")

    return data