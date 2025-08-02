---
mode: agent
tools: ["bandit", "safety"]
description: Security-centric review of Python code
---

Scope: `${file}` or pasted diff.

You must:
1. Run mental pass of OWASP Top-10 for APIs.  
2. Flag injection, deserialization, and secrets handling.  
3. Suggest safer libraries or patterns.  
4. Output Bandit rule IDs where relevant.

Return findings as a severity-sorted table plus mitigation notes.
