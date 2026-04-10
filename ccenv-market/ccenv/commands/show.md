---
name: show
description: Show details of a specific ccenv profile
---

# ccenv:show

Show detailed configuration of a specific ccenv profile.

## Usage

```bash
/ccenv:show PROFILE_NAME [--format FORMAT]
```

## Arguments

| Argument | Description |
|----------|-------------|
| `PROFILE_NAME` | Name of the profile to show (required) |
| `--format FORMAT` | Output format: `yaml`, `json`, or `table` (default: table) |
| `--raw` | Show raw YAML file content |

## Output

Shows:
- Profile metadata (name, version, description, mode)
- Plugins to add/remove
- MCP server configurations
- Skills and agents

## Examples

```bash
# Show profile in table format
/ccenv:show frontend

# Show raw YAML
/ccenv:show frontend --raw

# Export as JSON
/ccenv:show ml --format json
```

Sample output:
```
Profile: frontend
=================
Name:        frontend
Version:     1.0
Description: Frontend development environment
Mode:        overlay

Plugins:
  + superpowers@claude-plugins-official
  + playwright@claude-plugins-official

MCP Servers:
  playwright: npm:@anthropic/playwright-mcp

Skills:
  + frontend-design (global)

Agents:
  + ui-designer (claude-sonnet-4-6)
```