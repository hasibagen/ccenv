---
name: use
description: Apply a ccenv profile to a project directory
---

# ccenv:use

Apply a ccenv profile to a project directory, configuring MCP servers, plugins, skills, and agents.

## Usage

```bash
/ccenv:use PROFILE_NAME PROJECT_PATH [OPTIONS]
```

## Arguments

| Argument | Description |
|----------|-------------|
| `PROFILE_NAME` | Name of the profile to apply (required) |
| `PROJECT_PATH` | Target project directory (default: current directory) |
| `--scope SCOPE` | Apply scope: `project` or `user` (default: project) |
| `--force` | Overwrite existing configuration without prompting |
| `--dry-run` | Preview changes without writing files |
| `--backup` | Create backup of existing configuration |

## Actions

1. Reads profile YAML from `~/.claude/ccenv/profiles.d/{name}.yml`
2. Merges with existing settings (overlay mode) or replaces (replace mode)
3. Writes to `PROJECT_PATH/.claude/settings.json`
4. Writes MCP config to `PROJECT_PATH/.mcp.json`
5. Copies skills/agents to project if specified
6. Creates backup if `--backup` flag is used

## Examples

```bash
# Apply to current directory
/ccenv:use frontend .

# Apply to specific project
/ccenv:use ml /path/to/project

# Preview changes
/ccenv:use frontend . --dry-run

# Force overwrite
/ccenv:use frontend . --force

# With backup
/ccenv:use eeg . --backup

# Apply to user-level settings
/ccenv:use base ~ --scope user
```

## Merge Behavior

### Overlay Mode (default)
- Adds new plugins to existing configuration
- Merges MCP servers (existing servers kept)
- Appends skills and agents

### Replace Mode
- Completely replaces `.claude/settings.json`
- Overwrites `.mcp.json`
- Removes existing project skills/agents