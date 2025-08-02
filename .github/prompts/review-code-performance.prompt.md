---
description: "Review the selected code for performance bottlenecks and suggest optimizations."
---
# Task: Performance Code Review

You are a performance optimization expert. Analyze the selected Python code for performance bottlenecks.

**Code to Review:**
`${selection}`

# Instructions:

- Identify sections of code that are likely to be slow, such as nested loops, inefficient data structures, or repeated computations.
- Suggest specific, more performant alternatives.
- Examples:
    - Replacing list appends in a loop with a list comprehension.
    - Using a set for fast membership testing instead of a list.
    - Suggesting vectorized operations with libraries like NumPy/Pandas if applicable.
    - Recommending caching/memoization for expensive function calls.
- Present your findings as a list of "Potential Bottlenecks" and a corresponding list of "Suggested Optimizations."
