---
mode: agent
description: Optimize selected loop for speed & clarity
---

Inside `${file}`, analyze `${selection}`.

Refactor guidelines:
• Prefer list/dict comprehensions & generator expressions.  
• Use `itertools`, `collections`, `functools`.  
• Maintain identical output & side-effects.  
• Add micro-benchmark snippet (using `timeit`) as a comment block.

Show:
1. Original loop (as quoted block).  
2. Optimized replacement.  
3. Benchmark result table.

Produce patch ready to commit.
