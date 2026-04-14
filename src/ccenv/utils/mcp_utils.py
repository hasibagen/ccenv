"""
MCP utilities for ccenv - parse and resolve MCP configurations
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import os


def parse_mcp_json(path: Path) -> Dict[str, Any]:
    """
    Parse .mcp.json file

    Args:
        path: Path to .mcp.json file

    Returns:
        Dictionary with MCP server configurations
    """
    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("mcpServers", {})


def resolve_mcp_command_to_source(command: str, args: List[str]) -> Tuple[str, str]:
    """
    Resolve MCP command and args to source format

    Examples:
        ("npx", ["-y", "@anthropic/playwright-mcp"]) -> ("npm:@anthropic/playwright-mcp", "stdio")
        ("python", ["-m", "mcp-server"]) -> ("pip:mcp-server", "stdio")
        ("/absolute/path", []) -> ("/absolute/path", "stdio")

    Args:
        command: The command to execute
        args: Command arguments

    Returns:
        Tuple of (source, type)
    """
    mcp_type = "stdio"

    # Check for npx
    if command == "npx":
        # Find the package in args
        for i, arg in enumerate(args):
            if arg.startswith("-"):
                continue
            if arg.startswith("@"):
                # Scoped package like @anthropic/playwright-mcp
                return f"npm:{arg}", mcp_type
            elif not arg.startswith("-"):
                return f"npm:{arg}", mcp_type
        return f"npm:{args[-1] if args else 'unknown'}", mcp_type

    # Check for python -m
    if command == "python" or command == "python3":
        if args and args[0] == "-m" and len(args) > 1:
            return f"pip:{args[1]}", mcp_type

    # Check for uvx
    if command == "uvx":
        if args:
            return f"pip:{args[0]}", mcp_type

    # Absolute path or other command
    if command.startswith("/") or command.startswith("~"):
        # Check if it matches an environment variable
        env_var = find_matching_env_var(command)
        if env_var:
            return f"local:${{{env_var}}}", mcp_type
        return command, mcp_type

    # Default: treat as-is
    return command, mcp_type


def find_matching_env_var(path: str) -> Optional[str]:
    """
    Check if path matches any environment variable value

    Args:
        path: The path to check

    Returns:
        Environment variable name if found, None otherwise
    """
    for var_name, var_value in os.environ.items():
        if var_value and path.startswith(var_value):
            return var_name
    return None


def extract_mcp_config(mcp_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Extract MCP configuration from .mcp.json data

    Args:
        mcp_data: Raw MCP server data from .mcp.json

    Returns:
        Dictionary of MCP configurations with source format
    """
    result = {}

    for name, config in mcp_data.items():
        command = config.get("command", "")
        args = config.get("args", [])
        mcp_type = config.get("type", "stdio")
        env = config.get("env", {})

        source, resolved_type = resolve_mcp_command_to_source(command, args)

        result[name] = {
            "source": source,
            "type": resolved_type,
            "args": [] if source.startswith(("npm:", "pip:")) else args,
            "env": env,
        }

    return result


def get_mcp_type_from_config(config: Dict[str, Any]) -> str:
    """
    Get MCP type from configuration

    Args:
        config: MCP server configuration

    Returns:
        MCP type (stdio, http, sse)
    """
    if "url" in config:
        return "http"
    return config.get("type", "stdio")