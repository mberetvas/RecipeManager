---
mode: agent
description: Perform fast code-quality review of current diff
---

Paste a unified diff after running this prompt.

Checklist:
• Readability & naming  
• Complexity (cyclomatic, nesting)  
• Type safety  
• PEP8 via `ruff`  
• Missing tests/docstrings

Respond with:
1. Summary table (✔/✘ per category).  
2. Inline comments (GitHub review style).  
3. Recommended next actions (bullet list).
