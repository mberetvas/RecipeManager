---
description: "Condensed Python Code Review Checklist."
applyTo: "**/*.py"
---
# 🔎 Condensed Code Review Checklist

## Output Formatting
- Use Markdown headings as shown.
- Show code suggestions in `diff` format.
- If no issues: `✅ No issues found.`
- List most impactful feedback first.

---

## Review Categories

### 🐛 Correctness & Logic
- Check for bugs, logic errors, off-by-one, `None`, edge cases, race conditions.

### 🧹 Readability & Maintainability
- Ensure clear, Pythonic code and naming.
- Recommend idiomatic constructs and PEP 8.
- Suggest refactoring complex code.

### 🚀 Performance
- Spot inefficient loops, data structures, or repeated expensive computations.

### 🔒 Security
- Look for hardcoded secrets, injection risks, insecure functions (`eval`, `exec`, `pickle`).

### 📝 Documentation & Testability
- Require clear docstrings and comments (explain "why").
- Ensure code is easily testable, with minimal side effects.
