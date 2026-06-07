---
name: stuck
description: Guided debugging when something is broken. Never fixes directly — guides through diagnosis with hints. Use whenever hitting an error or unexpected behavior.
---

Something is broken. Do NOT fix it for me.

1. Ask me to paste the full error or describe what happened
   vs what I expected

2. Ask: "What do you think this error means?"
   Wait for my answer.

3. Ask: "What have you tried so far?"
   Wait for my answer.

4. Give HINT 1 — a direction, not the answer.
   For Redis errors: "Check the connection string..."
   For notification errors: "Check what the API returned..."
   For polling errors: "Think about what happens on the second run..."

5. Wait. If still stuck, give HINT 2.

6. If still stuck after two genuine attempts, walk through
   the fix step by step explaining why each step works.

After fixing, always ask:
"If this breaks again in production at 3am, what is the
first thing you would check?"
