# ccenv - Claude Code 环境管理器

> 类 conda 的 Claude Code 配置环境管理工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

## 🌟 简介

**ccenv** 是一个为 [Claude Code](https://code.claude.com/) 设计的环境管理工具，让你可以保存、切换和分享开发环境配置。可以把它理解为"Claude Code 版的 conda"。

### 为什么选择 ccenv？

- **保存配置** - 将你的插件、MCP 服务器、技能和智能体导出为可复用的配置文件
- **快速切换** - 一条命令即可在不同项目环境之间切换
- **分享配置** - 与团队成员或社区分享你的常用配置
- **版本控制友好** - 配置文件采用 YAML 格式，非常适合 git 管理

## 📦 安装

### 方式一：作为 Claude Code 插件安装（推荐）

```bash
# 添加市场
/plugin marketplace add https://github.com/hasibagen/ccenv

# 安装插件
/plugin install ccenv@ccenv-market
```

### 方式二：作为 Python 包安装

```bash
pip install ccenv
```

### 方式三：手动安装

```bash
git clone https://github.com/hasibagen/ccenv.git
cd ccenv
pip install -e .
```

## 🚀 快速开始

### 创建配置文件

```bash
# 创建前端开发配置
/ccenv:create -n frontend -d "前端开发环境" -p superpowers -p playwright

# 创建机器学习配置
/ccenv:create -n ml -d "机器学习环境" --mcp "python:npm:mcp-python-server"
```

### 列出所有配置

```bash
/ccenv:list
```

输出：
```
ccenv Profiles
==============
NAME        DESCRIPTION              MODIFIED
frontend    前端开发环境             2026-04-10
ml          机器学习环境             2026-04-10
eeg         EEG/fNIRS 研究          2026-04-09
```

### 应用配置

```bash
# 应用到当前目录
/ccenv:use frontend .

# 应用到指定项目
/ccenv:use ml /path/to/project

# 预览变更（不实际写入）
/ccenv:use frontend . --dry-run
```

### 提取和更新

在手动修改项目配置后：

```bash
# 更新现有配置
/ccenv:extract . -n frontend --update

# 从当前项目创建新配置
/ccenv:extract . -n new-profile -d "我的新配置"
```

## 📖 命令参考

| 命令 | 说明 |
|------|------|
| `/ccenv:create` | 创建新的配置文件 |
| `/ccenv:list` | 列出所有可用配置 |
| `/ccenv:show` | 显示指定配置的详情 |
| `/ccenv:use` | 将配置应用到项目目录 |
| `/ccenv:extract` | 从项目提取配置创建配置文件 |

## 📁 配置文件结构

配置文件存储在 `~/.claude/ccenv/profiles.d/` 目录下，采用 YAML 格式：

```yaml
# ~/.claude/ccenv/profiles.d/frontend.yml
name: frontend
version: "1.0"
description: 前端开发环境
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

## 🔧 配置选项

### 合并模式

- **overlay**（默认）：添加到现有配置
- **replace**：完全替换配置

### MCP 来源格式

| 格式 | 示例 |
|------|------|
| 本地路径 | `local:${MATLAB_MCP_PATH}` |
| npm 包 | `npm:@anthropic/playwright-mcp` |
| pip 包 | `pip:mcp-server-tool` |

## 🤝 参与贡献

欢迎所有人参与！这是一个社区维护的项目。

### 贡献方式

- 🐛 通过 [Issues](https://github.com/hasibagen/ccenv/issues) 报告问题
- 💡 提出新功能或改进建议
- 📝 改进文档
- 🔧 提交 Pull Request

### 开发环境搭建

```bash
git clone https://github.com/hasibagen/ccenv.git
cd ccenv
pip install -e ".[dev]"
```

## 📋 开发路线

- [ ] Python CLI 完整实现
- [ ] 从 URL 导入/导出配置
- [ ] 通过 GitHub Gist 分享配置
- [ ] 配置模板库
- [ ] 根据项目类型自动推荐配置

## 📜 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 灵感来源于 [conda](https://docs.conda.io/) 环境管理
- 为 [Claude Code](https://code.claude.com/) 构建
- 社区驱动开发

---

**用 ❤️ 由社区制作**

*不是专业程序员？没关系！欢迎各种技能水平的贡献者。*

---

## English Version | 英文版本

### ccenv - Claude Code Environment Manager

> A conda-like environment manager for Claude Code configurations

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

## Overview

**ccenv** is a profile management tool for [Claude Code](https://code.claude.com/) that lets you save, switch, and share development environments. Think of it as "conda for Claude Code configurations."

### Why ccenv?

- **Save your setup** - Export your plugins, MCP servers, skills, and agents into a reusable profile
- **Quick switching** - Switch between different project environments with a single command
- **Share configurations** - Share your favorite setups with teammates or the community
- **Version control friendly** - Profiles are YAML files that work great with git

## Installation

### Option 1: Install as Claude Code Plugin (Recommended)

```bash
/plugin marketplace add https://github.com/hasibagen/ccenv
/plugin install ccenv@ccenv-market
```

### Option 2: Install as Python Package

```bash
pip install ccenv
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

## Commands

| Command | Description |
|---------|-------------|
| `/ccenv:create` | Create a new profile with specified configuration |
| `/ccenv:list` | List all available profiles |
| `/ccenv:show` | Display details of a specific profile |
| `/ccenv:use` | Apply a profile to a project directory |
| `/ccenv:extract` | Extract configuration from a project to create a profile |

## Profile Structure

```yaml
name: frontend
version: "1.0"
description: Frontend development environment
mode: overlay

plugins:
  add:
    - superpowers@claude-plugins-official

mcp:
  playwright:
    source: "npm:@anthropic/playwright-mcp"

skills:
  - name: frontend-design
    source: global
```

## Contributing

We welcome contributions from everyone!

- 🐛 Report bugs via [Issues](https://github.com/hasibagen/ccenv/issues)
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit pull requests

## License

MIT License - see [LICENSE](LICENSE) for details.