---
name: start-session
description: Start a new V3 session. Reads project state, draws the current polling architecture, and proposes what to work on. Use at the beginning of every session.
---

Read CLAUDE.md for project context and teaching rules.
Then explore the current state of the codebase:

1. Run: git log --oneline -10
2. List the folder structure (focus on v3/ folder if it exists)
3. Read any recently changed files

Then tell me:

1. Draw the CURRENT architecture in ASCII showing what
   is actually built vs what is still planned.
   Use: [BUILT], [PARTIAL], [NOT YET]

2. Where we are in the V3 session map from CLAUDE.md

3. Two or three options for what to work on today,
   ordered by what makes most sense next

Wait for me to choose. Do NOT write code or make changes.
