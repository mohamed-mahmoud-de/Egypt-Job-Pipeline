---
name: start-session
description: Start a new development session. Reads the project state from git and files, then proposes what to work on next. Use at the beginning of every session.
---

Read CLAUDE.md for project context and teaching rules.
Then explore the current state of the codebase:

1. Run: git log --oneline -10
2. List the folder structure
3. Read any files that changed in the last few commits

Then tell me:
- Current state of the project (what is built, what is not)
- What we likely worked on last based on recent commits
- 2 or 3 options for what to tackle next

Wait for me to pick before doing anything.
Do NOT start writing code or making changes.
