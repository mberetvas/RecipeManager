---
mode: agent
tools: ["pytest"]
description: Generate pytest cases for selected code
---

Selection refers to `${file}`.

1. Detect public functions/classes in `${selection}`.  
2. For each, generate ≥3 test cases:
   • happy path  
   • edge case  
   • error/exception case  
3. Use `pytest.mark.parametrize` where possible.  
4. Follow *Arrange-Act-Assert* sections.  
5. Add `mypy` type-checking comment at top.

Put tests in `tests/test_${fileBasenameNoExtension}.py` fenced.
