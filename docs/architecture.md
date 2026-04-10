# ccenv Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     ccenv System                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │   Profiles   │    │   Commands   │    │   Config     │   │
│  │   (YAML)     │    │   (CLI)      │    │   (JSON)     │   │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘   │
│         │                   │                   │           │
│         └───────────────────┼───────────────────┘           │
│                             ▼                               │
│                    ┌────────────────┐                       │
│                    │   Core Engine  │                       │
│                    │   (Python)     │                       │
│                    └────────┬───────┘                       │
│                             │                               │
│         ┌───────────────────┼───────────────────┐           │
│         ▼                   ▼                   ▼           │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │    MCP       │    │   Plugins    │    │   Skills     │   │
│  │   Manager    │    │   Manager    │    │   Manager    │   │
│  └──────────────┘    └──────────────┘    └──────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

### Profile Storage (`~/.claude/ccenv/`)

```
~/.claude/ccenv/
├── profiles.d/              # Profile definitions (YAML, git-syncable)
│   ├── frontend.yml
│   ├── ml.yml
│   └── eeg.yml
├── .cache/                  # Local cache (not synced)
│   └── skills/
└── config.json              # Global ccenv config
```

### Marketplace Structure

```
ccenv-market/                    # Marketplace root
├── .claude-plugin/
│   └── marketplace.json         # Marketplace catalog
└── ccenv/                       # Plugin directory
    ├── .claude-plugin/
    │   └── plugin.json          # Plugin manifest
    └── commands/                # Slash commands
        ├── create.md
        ├── list.md
        ├── show.md
        ├── use.md
        └── extract.md
```

## Core Components

### 1. Profile Manager

Manages YAML-based profile definitions:

```yaml
name: frontend
version: "1.0"
description: Frontend development environment
mode: overlay  # overlay | replace

plugins:
  add:
    - superpowers@claude-plugins-official
  remove:
    - github

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

### 2. Config Merger

Two merge modes:

- **Overlay**: Add to global config (default)
- **Replace**: Replace global config entirely

### 3. MCP Resolver

Resolves MCP sources:

| Source Format | Example |
|---------------|---------|
| `local:${VAR}` | `local:${MATLAB_MCP_PATH}` |
| `npm:package` | `npm:@anthropic/playwright-mcp` |
| `pip:package` | `pip:mcp-server-tool` |

## Data Flow

```
1. User runs: /ccenv:use frontend /path/to/project

2. ccenv loads:
   - ~/.claude/ccenv/profiles.d/frontend.yml
   - ~/.claude/settings.json (global)

3. ccenv merges:
   - Global plugins + Profile plugins
   - Global MCP + Profile MCP
   - Skills from profile

4. ccenv writes:
   - /path/to/project/.claude/settings.json
   - /path/to/project/.mcp.json
   - /path/to/project/.claude/skills/ (copies)
```

## Security Model

1. **YAML Parsing**: Use `yaml.safe_load()` only
2. **Path Validation**: No `..` traversal, no absolute paths outside allowed dirs
3. **Command Injection**: Validate MCP command paths, no shell metacharacters
4. **Sensitive Data**: Support `command_file` for external secret references