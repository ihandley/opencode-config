# OpenCode Project

My OpenCode configuration, agents, skills, and commands for AI-assisted development.

## Overview

This repository contains my personalized OpenCode setup including:
- Custom agents for specific tasks
- Agent skills for reusable behaviors
- Custom commands for common workflows
- Coding standards and instructions

## Structure

```
opencode/
├── .opencode/
│   ├── agents/          # Custom agent definitions
│   │   ├── code-reviewer.md
│   │   └── docs-writer.md
│   ├── skills/          # Reusable skill definitions
│   │   └── git-release/
│   │       └── SKILL.md
│   ├── commands/        # Custom command templates
│   │   ├── test.md
│   │   └── lint.md
│   └── instructions/    # Project rules and standards
│       └── coding-standards.md
├── opencode.json        # OpenCode configuration
├── .env.example        # Environment variables template
└── .gitignore
```

## Setup

1. Clone this repository to `~/code/github/opencode`
2. Copy `.env.example` to `.env` and add your API keys
3. Add to your shell profile:
   ```bash
   export OPENCODE_CONFIG_DIR="$HOME/code/github/opencode"
   ```
4. Run `/connect` in OpenCode to authenticate

## Default Model

Uses `opencode/minimax-m2.5-free` for all agents.

## Agents

- **code-reviewer**: Read-only code review agent
- **docs-writer**: Documentation specialist

## Commands

- `/test`: Run full test suite with coverage
- `/lint`: Run linter and formatter checks

## Skills

- **git-release**: Automated release workflow

## License

MIT