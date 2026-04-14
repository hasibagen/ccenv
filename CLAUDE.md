# ccenv - Claude Code Environment Manager

conda-like environment manager for Claude Code configurations (MCP, plugins, skills, agents).

## Development Environment

This project uses a conda environment named `ccenv`. All Python development should use this environment.

### Setup

```bash
# Activate the conda environment
conda activate ccenv

# Install in development mode
pip install -e ".[dev]"
```

### Running Commands

Always activate the conda environment before running any Python commands:

```bash
conda activate ccenv
ccenv --help
ccenv create -n my-profile
ccenv list
```

### Testing

```bash
conda activate ccenv
pytest tests/ -v
```

### Code Quality

```bash
conda activate ccenv
ruff check .
black .
mypy src/ccenv
```

## Project Structure

```
src/ccenv/
├── cli.py           # CLI entry point
├── commands/        # CLI commands (create, list, show, use)
├── core/            # Core modules (profile, plugins)
├── utils/           # Utilities (yaml_utils, validation)
└── schemas/         # JSON schemas
```

## Key Files

- `pyproject.toml` - Package configuration
- `src/ccenv/cli.py` - CLI entry point
- `src/ccenv/core/profile.py` - Profile management
- `tests/` - Test files

## Commands

| Command | Description |
|---------|-------------|
| `ccenv create -n NAME` | Create a new profile |
| `ccenv list` | List all profiles |
| `ccenv show NAME` | Show profile details |
| `ccenv use NAME PATH` | Apply profile to project |

## Profile Storage

Profiles are stored in `~/.claude/ccenv/profiles.d/` as YAML files.

Can be overridden with `CCENV_PROFILES_DIR` environment variable.

## PyPI Publishing

```bash
conda activate ccenv
pip install build twine
python -m build
twine upload dist/*
```

## License

MIT