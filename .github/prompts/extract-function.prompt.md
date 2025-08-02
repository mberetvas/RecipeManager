---
mode: agent
description: Extract selection into a reusable function
---

Goal: improve readability & testability.

1. From `${file}`, wrap `${selection}` into
   `def ${input:func_name}(${input:params}): -> ${input:return_type}`.  
2. Preserve behavior; replace original code with the call.  
3. Insert Google-style docstring with side-effects & raises.  
4. Add a pytest test stub for the new function in
   `tests/test_${fileBasenameNoExtension}.py`.

Return the full diff in unified format.
