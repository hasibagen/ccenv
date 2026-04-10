# ccenv - Claude Code Environment Manager

> A conda-like environment manager for Claude Code configurations

## Quick Links

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Commands](#commands)
- [Contributing](CONTRIBUTING.md)

## Features

- 📦 **Profile Management** - Save and switch between different Claude Code configurations
- 🔄 **Easy Switching** - Apply profiles to any project with a single command
- 🔗 **MCP Support** - Manage MCP servers in your profiles
- 🎯 **Skills & Agents** - Include skills and agents in your environments
- 📤 **Export & Share** - Extract configurations from projects and share with others

## Installation

Add the marketplace and install the plugin:

```bash
/plugin marketplace add https://github.com/YOUR_USERNAME/ccenv
/plugin install ccenv@ccenv-market
```

## Quick Start

```bash
# Create a profile
/ccenv:create -n frontend -d "Frontend development" -p superpowers

# List profiles
/ccenv:list

# Apply to current project
/ccenv:use frontend .

# Extract from project
/ccenv:extract . -n my-setup
```

## License

MIT License - see [LICENSE](LICENSE) for details.