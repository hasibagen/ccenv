"""
ccenv - Claude Code Environment Manager

A conda-like profile management tool for Claude Code configurations
(MCP, plugins, skills, agents).
"""

__version__ = "0.1.0"
__author__ = "hasibagen"

from ccenv.core.profile import Profile, ProfileManager
from ccenv.utils.yaml_utils import load_yaml, save_yaml

__all__ = [
    "__version__",
    "__author__",
    "Profile",
    "ProfileManager",
    "load_yaml",
    "save_yaml",
]