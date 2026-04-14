# ccenv

[![PyPI version](https://badge.fury.io/py/ccenv.svg)](https://pypi.org/project/ccenv/)
[![CI](https://github.com/hasibagen/ccenv/actions/workflows/ci.yml/badge.svg)](https://github.com/hasibagen/ccenv/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**conda-like environment manager for Claude Code**

Manage Claude Code configurations (MCP, plugins, skills, agents) with profile-based templates. Define once, apply anywhere, sync across machines.

## Features

- 📦 **Profile-based configuration** - Define reusable environment templates
- 🔌 **Unified management** - MCP servers, plugins, skills, and agents in one place
- 🔄 **Multi-machine sync** - Profiles are YAML files, git-syncable
- 🛡️ **Safe configuration** - Schema validation, safe YAML parsing
- 🌍 **Cross-platform** - Linux, macOS, Windows support

## Installation

```bash
pip install ccenv
```

## Quick Start

```bash
# Create a profile
ccenv create -n eeg --description "EEG analysis environment" \
  --mcp matlab:local:${MATLAB_MCP_PATH} \
  --skill eeg-analysis \
  --plugin superpowers

# List all profiles
ccenv list

# Show profile details
ccenv show eeg

# Apply to a project
ccenv use eeg /path/to/project
```

## Profile YAML Structure

Profiles are stored in `~/.claude/ccenv/profiles.d/`:

```yaml
name: eeg
version: "1.0"
description: EEG/fNIRS 数据分析环境
mode: overlay  # overlay or replace

plugins:
  add:
    - superpowers
    - plan
  remove:
    - github

mcp:
  matlab:
    source: "local:${MATLAB_MCP_PATH}"
    type: stdio
  context7:
    source: "npm:@anthropic/context7-mcp"

skills:
  - name: eeg-analysis
    source: global
  - name: custom-skill
    source: project
    version: "1.2.0"

agents:
  - name: eeg-analyzer
    source: global
    model: claude-opus-4-6

env:
  CUSTOM_VAR: "value"

hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      command: "npm run lint:fix"
```

## Commands

| Command | Description |
|---------|-------------|
| `ccenv create -n NAME` | Create a new profile |
| `ccenv create -f FILE.yml` | Create from existing YAML |
| `ccenv list` | List all profiles |
| `ccenv show NAME` | Show profile details |
| `ccenv use NAME PATH` | Apply profile to project |
| `ccenv --help` | Show help |

## MCP Source Formats

| Format | Example | Description |
|--------|---------|-------------|
| `local:${VAR}` | `local:${MATLAB_MCP_PATH}` | Environment variable path |
| `marketplace:org/name` | `marketplace:claude-plugins-official/github` | From marketplace |
| `npm:package` | `npm:@playwright/mcp` | npm package |
| `pip:package` | `pip:mcp-server-mytool` | pip package |

## Multi-Machine Sync

Sync your profiles across machines using git:

```bash
# Initialize profiles repo
cd ~/.claude/ccenv
git init
git remote add origin git@github.com:yourname/ccenv-profiles.git
git push -u origin main

# On another machine
ccenv clone git@github.com:yourname/ccenv-profiles.git
```

## Configuration Precedence

When applying a profile with `mode: overlay`:

1. Profile settings are merged with existing project settings
2. Profile plugins are added to existing plugins
3. Profile MCP servers override same-name servers
4. Profile `plugins.remove` disables specified plugins

With `mode: replace`:

1. All existing settings are replaced
2. Only profile configuration is used

## Development

```bash
# Clone repository
git clone https://github.com/hasibagen/ccenv.git
cd ccenv

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run linting
ruff check .
black --check .
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions welcome! Please read the [Contributing Guide](CONTRIBUTING.md) for details.

## Related Projects

- [Claude Code](https://code.claude.com/) - Official Claude CLI
- [Claude Code Documentation](https://code.claude.com/docs) - Official docs
- [skills-manager](https://github.com/xingkongliang/skills-manager) - Skills management tool