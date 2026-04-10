---
name: create
description: Create a new ccenv profile with specified configuration
---

# ccenv:create

Create a new ccenv profile with specified plugins, MCP servers, skills, and agents.

## Usage

```bash
/ccenv:create -n NAME [-d DESCRIPTION] [-p PLUGIN] [--mcp MCP] [--skill SKILL] [--agent AGENT]
```

## Arguments

| Argument | Description |
|----------|-------------|
| `-n, --name NAME` | Profile name (required) |
| `-d, --description DESC` | Profile description |
| `-p, --plugin PLUGIN` | Plugin to add (repeatable, format: `name@marketplace`) |
| `--mcp MCP` | MCP server spec (repeatable, format: `name:source`) |
| `--skill SKILL` | Skill to add (repeatable) |
| `--agent AGENT` | Agent to add (repeatable) |
| `--mode MODE` | Merge mode: `overlay` or `replace` (default: overlay) |

## Examples

```bash
# Create a basic profile
/ccenv:create -n frontend -d "Frontend development"

# Add plugins
/ccenv:create -n frontend -p superpowers@claude-plugins-official -p playwright@claude-plugins-official

# Add MCP server
/ccenv:create -n eeg --mcp "matlab:local:${MATLAB_MCP_PATH}"

# Full example
/ccenv:create -n fullstack -d "Full stack development" \
  -p superpowers@claude-plugins-official \
  --mcp "playwright:npm:@anthropic/playwright-mcp" \
  --skill frontend-design \
  --agent ui-designer
```

## Output

Creates a YAML profile file at `~/.claude/ccenv/profiles.d/{NAME}.yml`

## Notes

- Profile names must be lowercase with hyphens (e.g., `my-profile`)
- If a profile with the same name exists, use `--force` to overwrite
- MCP sources support: `local:${VAR}`, `npm:package`, `pip:package`