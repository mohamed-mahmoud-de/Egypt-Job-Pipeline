---
name: explain
description: Deep-dive a concept before writing code. Especially useful for Redis (the one new tool in V3), polling design patterns, deduplication strategies, and notification system design.
---

I want to understand a concept deeply before writing any code.

Follow this sequence:

1. ELI5 — one sentence, simple as possible

2. REAL EXPLANATION WITH ANALOGY
   Connect to something I already know from V1 or V2:
   - V2 Airflow deduplication (URL-based uniqueness)
   - V2 Discord webhook alerts (notification pattern)
   - Postgres querying (why Redis is faster for this)
   - Docker Compose services (Redis as another service)

3. IN V3 SPECIFICALLY
   Where exactly does this concept appear in our architecture?
   What breaks if I misunderstand it?

4. THE COMMON MISTAKE
   What do beginners usually get wrong about this?

5. TEST ME
   Ask me to explain it back. Wait for my answer.
   Correct if wrong and ask again.

No code until I can explain the concept back correctly.
