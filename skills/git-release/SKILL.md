---
name: git-release
description: Create consistent releases and changelogs
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: github
---

## What I do
- Draft release notes from merged PRs since last release
- Propose a version bump (patch/minor/major) based on commit messages
- Provide a copy-pasteable `gh release create` command
- Tag the release with appropriate version

## When to use me
Use this when you are preparing a tagged release.

## Guidelines
- Follow Semantic Versioning (https://semver.org)
- Group changes by type: Features, Bug Fixes, Breaking Changes, Documentation
- Include PR numbers and authors where appropriate
- Ask clarifying questions if the target versioning scheme is unclear
- Check if there are any unmerged PRs that should be included