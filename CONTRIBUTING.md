# Contributing to ccenv

First off, thank you for considering contributing to ccenv! 🎉

We welcome contributions from everyone, regardless of experience level. This project is community-maintained, and we're excited to have you join us.

## Ways to Contribute

### 🐛 Report Bugs

Found a bug? Please open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Claude Code version)

### 💡 Suggest Features

Have an idea? We'd love to hear it! Open an issue with:
- A clear description of the feature
- Why it would be useful
- Any implementation ideas you have

### 📝 Improve Documentation

Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add examples
- Translate documentation

### 🔧 Submit Code

Ready to write some code?

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to your fork (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ccenv.git
cd ccenv

# The project structure
# ccenv-market/     - The installable marketplace
# docs/             - Documentation
```

## Project Structure

```
ccenv/
├── ccenv-market/              # Marketplace (what users install)
│   ├── .claude-plugin/
│   │   └── marketplace.json   # Marketplace catalog
│   └── ccenv/
│       ├── .claude-plugin/
│       │   └── plugin.json    # Plugin manifest
│       └── commands/          # Slash commands
│           ├── create.md
│           ├── extract.md
│           ├── list.md
│           ├── show.md
│           └── use.md
├── docs/
│   └── architecture.md
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

## Code Style

- Keep commands simple and focused
- Use clear, descriptive names
- Document command arguments in markdown tables
- Include practical examples

## Questions?

Feel free to open an issue with your question, or start a discussion!

---

**Remember: This is a community project. There are no silly questions, and all contributions are valued.**