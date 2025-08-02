---
mode: agent
description: Add/Update Google-style docstrings to selection
---

File: `${file}`  
Selection: `${selection}`

For each function/class lacking a proper docstring:
1. Insert or rewrite a Google-style docstring.  
2. Include Args, Returns, Raises, Examples.  
3. Maintain line length ≤88 and correct indentation.

Return the modified file with highlights.
