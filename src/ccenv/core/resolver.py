"""
MCP server source resolver for ccenv
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, Optional, Tuple


class MCPResolver:
    """Resolves MCP server sources to executable configurations."""

    # Source patterns
    LOCAL_PATTERN = re.compile(r"^local:\$\{(.+)\}$")
    NPM_PATTERN = re.compile(r"^npm:(.+)$")
    PIP_PATTERN = re.compile(r"^pip:(.+)$")

    def resolve(self, source: str) -> Dict[str, Any]:
        """Resolve a source string to MCP server configuration.

        Args:
            source: Source string (e.g., "local:${VAR}", "npm:package")

        Returns:
            MCP server configuration dictionary
        """
        # Check for local path with environment variable
        local_match = self.LOCAL_PATTERN.match(source)
        if local_match:
            return self._resolve_local(local_match.group(1))

        # Check for npm package
        npm_match = self.NPM_PATTERN.match(source)
        if npm_match:
            return self._resolve_npm(npm_match.group(1))

        # Check for pip package
        pip_match = self.PIP_PATTERN.match(source)
        if pip_match:
            return self._resolve_pip(pip_match.group(1))

        # Unknown source type, return as-is
        return {"command": source}

    def _resolve_local(self, env_var: str) -> Dict[str, Any]:
        """Resolve local path from environment variable.

        Args:
            env_var: Environment variable name

        Returns:
            MCP server configuration
        """
        path = os.environ.get(env_var, "")
        if not path:
            raise ValueError(f"Environment variable {env_var} not set")

        path = Path(path).resolve()

        if not path.exists():
            raise ValueError(f"Path {path} does not exist")

        if path.is_dir():
            # Assume it's a Node.js project
            return {
                "command": "node",
                "args": [str(path / "index.js")],
                "cwd": str(path)
            }
        else:
            # Assume it's an executable
            return {
                "command": str(path)
            }

    def _resolve_npm(self, package: str) -> Dict[str, Any]:
        """Resolve npm package to MCP server configuration.

        Args:
            package: npm package name

        Returns:
            MCP server configuration
        """
        return {
            "command": "npx",
            "args": ["-y", package]
        }

    def _resolve_pip(self, package: str) -> Dict[str, Any]:
        """Resolve pip package to MCP server configuration.

        Args:
            package: pip package name

        Returns:
            MCP server configuration
        """
        return {
            "command": "python",
            "args": ["-m", package]
        }

    def validate_source(self, source: str) -> Tuple[bool, Optional[str]]:
        """Validate a source string.

        Args:
            source: Source string to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            self.resolve(source)
            return True, None
        except ValueError as e:
            return False, str(e)