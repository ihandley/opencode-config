---
description: General coding standards and best practices for this project
---

# Coding Standards

## General Principles
- Write clean, readable code over clever code
- Keep functions small and focused (single responsibility)
- Use meaningful variable and function names
- Comment *why*, not *what*

## TypeScript/JavaScript
- Always use explicit types over `any`
- Prefer `const` over `let`, avoid `var`
- Use optional chaining (`?.`) and nullish coalescing (`??`)
- Prefer async/await over raw promises

## Error Handling
- Never swallow errors silently
- Use custom error classes for domain errors
- Log errors with appropriate context

## Git Commits
- Use conventional commits format
- Keep commits atomic and small
- Write meaningful commit messages

## Testing
- Write tests for business logic
- Use descriptive test names that explain the scenario
- Follow AAA pattern (Arrange, Act, Assert)