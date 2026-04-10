"""
ccenv - Claude Code Environment Manager

A conda-like environment manager for Claude Code configurations.
"""

__version__ = "1.0.0"
__author__ = "ccenv contributors"

from .core.profile import ProfileManager
from .core.merger import ConfigMerger
from .core.resolver import MCPResolver

__all__ = ["ProfileManager", "ConfigMerger", "MCPResolver"]