---
name: quiz
description: Knowledge check on V3 concepts. Covers Redis, polling design, deduplication, and notification systems. Use after completing a session or concept.
---

Quiz me on what I have learned in V3 so far.

Ask 4-5 questions covering:

REDIS QUESTIONS:
- "Why do we use a Redis Set instead of a Redis List for
   storing seen job IDs?"
- "What happens to our Redis data if the container restarts?
   How do we handle that?"
- "Why is Redis faster than querying Postgres for
   the deduplication check?"

DESIGN QUESTIONS:
- "We poll every 3 minutes. A job posts at 3:01, gets taken
   down at 3:04. Do we catch it? Why or why not?"
- "What is the difference between what V2 does and what V3
   does? When would you use each?"
- "If Wuzzuf blocks our scraper at minute 45, what happens
   to our alert system? How would you make it resilient?"

NOTIFICATION QUESTIONS:
- "A new job matches our filters. Walk me through every step
   that happens from detection to notification."

One question at a time. Wait for my answer before continuing.
After each answer: confirm if right or wrong and why.

At the end give me an honest rating:
Redis understanding: solid / shaky / needs review
Polling design: solid / shaky / needs review
Overall V3 readiness: ready for next session / needs more work
