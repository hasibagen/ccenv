# ccenv - Claude Code Environment Manager

> A conda-like environment manager for Claude Code configurations

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Overview

**ccenv** is a profile management tool for [Claude Code](https://code.claude.com/) that lets you save, switch, and share development environments. Think of it as "conda for Claude Code configurations."

### Why ccenv?

- **Save your setup** - Export your plugins, MCP servers, skills, and agents into a reusable profile
- **Quick switching** - Switch between different project environments with a single command
- **Share configurations** - Share your favorite setups with teammates or the community
- **Version control friendly** - Profiles are YAML files that work great with git

## 📦 Installation

### Quick Install

```bash
# Add the marketplace
/plugin marketplace add https://github.com/YOUR_USERNAME/ccenv

# Install the plugin
/plugin install ccenv@ccenv-market
```

### Manual Install

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ccenv.git
   cd ccenv
   ```

2. Add as a local marketplace:
   ```bash
   /plugin marketplace add /path/to/ccenv/ccenv-market
   ```

3. Install the plugin:
   ```bash
   /plugin install ccenv@ccenv-market
   ```

## 🚀 Quick Start

### Create a Profile

```bash
# Create a profile for frontend development
/ccenv:create -n frontend -d "Frontend development" -p superpowers -p playwright

# Create a profile for ML/AI work
/ccenv:create -n ml -d "Machine learning" --mcp "python:npm:mcp-python-server"
```

### List Profiles

```bash
/ccenv:list
```

Output:
```
ccenv Profiles
==============
NAME        DESCRIPTION              MODIFIED
frontend    Frontend development     2026-04-10
ml          Machine learning         2026-04-10
eeg         EEG/fNIRS research       2026-04-09
```

### Apply a Profile

```bash
# Apply to current directory
/ccenv:use frontend .

# Apply to specific project
/ccenv:use ml /path/to/project

# Preview changes (dry run)
/ccenv:use frontend . --dry-run
```

### Extract & Update

After manually modifying your project's configuration:

```bash
# Update existing profile
/ccenv:extract . -n frontend --update

# Create new profile from current project
/ccenv:extract . -n new-profile -d "My new setup"
```

## 📖 Commands

| Command | Description |
|---------|-------------|
| `/ccenv:create` | Create a new profile with specified configuration |
| `/ccenv:list` | List all available profiles |
| `/ccenv:show` | Display details of a specific profile |
| `/ccenv:use` | Apply a profile to a project directory |
| `/ccenv:extract` | Extract configuration from a project to create/update a profile |

## 📁 Profile Structure

Profiles are stored as YAML files in `~/.claude/ccenv/profiles.d/`:

```yaml
# ~/.claude/ccenv/profiles.d/frontend.yml
name: frontend
version: "1.0"
description: Frontend development environment
mode: overlay  # overlay | replace

plugins:
  add:
    - superpowers@claude-plugins-official
    - playwright@claude-plugins-official

mcp:
  playwright:
    source: "npm:@anthropic/playwright-mcp"
    type: stdio

skills:
  - name: frontend-design
    source: global

agents:
  - name: ui-designer
    source: global
    model: claude-sonnet-4-6
```

## 🔧 Configuration

### Merge Modes

- **overlay** (default): Add to existing configuration
- **replace**: Replace configuration entirely

### MCP Sources

| Format | Example |
|--------|---------|
| Local path | `local:${MATLAB_MCP_PATH}` |
| npm package | `npm:@anthropic/playwright-mcp` |
| pip package | `pip:mcp-server-tool` |

## 🤝 Contributing

We welcome contributions! This project is maintained by the community.

### Ways to Contribute

- 🐛 Report bugs via [Issues](https://github.com/YOUR_USERNAME/ccenv/issues)
- 💡 Suggest features or improvements
- 📝 Improve documentation
- 🔧 Submit pull requests

### Development Setup

```bash
git clone https://github.com/YOUR_USERNAME/ccenv.git
cd ccenv
```

The project structure:
```
ccenv/
├── ccenv-market/           # Marketplace (installable)
│   ├── .claude-plugin/
│   │   └── marketplace.json
│   └── ccenv/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── commands/
│           ├── create.md
│           ├── extract.md
│           ├── list.md
│           ├── show.md
│           └── use.md
├── docs/
│   └── architecture.md
└── README.md
```

## 📋 Roadmap

- [ ] Python CLI implementation (currently using placeholder commands)
- [ ] Profile import/export from URLs
- [ ] Profile sharing via GitHub Gist
- [ ] Profile templates library
- [ ] Auto-detect and suggest profiles based on project type

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Inspired by [conda](https://docs.conda.io/) environment management
- Built for [Claude Code](https://code.claude.com/)
- Community-driven development

---

**Made with ❤️ by the community**

*Not a professional developer? Neither are we! Contributions of all skill levels are welcome.*