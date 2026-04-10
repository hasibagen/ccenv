---
name: list
description: List all available ccenv profiles
---

# ccenv:list

List all available ccenv profiles stored in `~/.claude/ccenv/profiles.d/`.

## Usage

```bash
/ccenv:list [--format FORMAT]
```

## Arguments

| Argument | Description |
|----------|-------------|
| `--format FORMAT` | Output format: `table` or `json` (default: table) |

## Output

Shows a table of profiles with:
- **NAME** - Profile identifier
- **DESCRIPTION** - Brief description
- **ACTIVE** - Whether current project uses this profile
- **MODIFIED** - Last modification date

## Examples

```bash
/ccenv:list
```

Output:
```
ccenv Profiles
==============
NAME        DESCRIPTION              ACTIVE    MODIFIED
frontend    Frontend development     No        2026-04-10
ml          Machine learning         No        2026-04-09
eeg         EEG/fNIRS research       Yes       2026-04-10

3 profiles found
```

JSON output:
```bash
/ccenv:list --format json
```