---
name: extract
description: Extract configuration from a project to create a ccenv profile
---

# ccenv:extract

Extract configuration from an existing project and save it as a ccenv profile. This is the "sync back" feature - when you manually modify your project's plugins, you can extract and update your profile.

## Usage

```bash
/ccenv:extract PROJECT_PATH -n PROFILE_NAME [OPTIONS]
```

## Arguments

| Argument | Description |
|----------|-------------|
| `PROJECT_PATH` | Source project directory (default: current directory) |
| `-n, --name NAME` | Profile name (required) |
| `--update` | Update existing profile instead of creating new |
| `-d, --description DESC` | Profile description |
| `--mode MODE` | Merge mode: `overlay` or `replace` (default: overlay) |

## Workflow Example

1. Start with a profile: `/ccenv:use frontend .`
2. Manually add/remove plugins in `.claude/settings.json`
3. Add MCP servers to `.mcp.json`
4. Save changes back: `/ccenv:extract . -n frontend --update`

## Examples

```bash
# Create new profile from current project
/ccenv:extract . -n my-frontend

# Update existing profile
/ccenv:extract . -n frontend --update

# From specific project with description
/ccenv:extract /path/to/project -n ml -d "Machine learning setup"

# Create with replace mode
/ccenv:extract . -n clean-slate --mode replace
```

## What Gets Extracted

- Enabled plugins from `.claude/settings.json`
- MCP servers from `.mcp.json`
- Skills from `.claude/skills/`
- Agents from `.claude/agents/`

## Notes

- Use `--update` to modify an existing profile
- Without `--update`, fails if profile already exists
- Extracted profiles are saved to `~/.claude/ccenv/profiles.d/`