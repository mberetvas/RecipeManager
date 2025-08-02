**Use Case:** Automatically add robust `try...except` blocks to code that might fail.
```md
---
description: "Add robust and specific error handling to the selected code."
---
# Task: Add Error Handling

Analyze the selected code block and add appropriate error handling.

**Code to Refactor:**
`${selection}`

# Instructions:

- Identify potential exceptions (e.g., FileNotFoundError, KeyError, requests.exceptions.RequestException, ValueError).
- Wrap the code in try...except blocks.
- Be specific. Avoid broad except Exception:. Catch the most likely exceptions explicitly.
- In each except block, add a comment like # TODO: Add logging here to indicate where logging should occur.
- If resources need to be cleaned up, ensure a finally block is used correctly.
- Return the modified code block.
