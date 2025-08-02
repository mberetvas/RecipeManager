---
applyTo: "**"
description: Guidelines for Python code generation, documentation, and testing using GitHub Copilot.
---

## 1. Python Coding Principles

- **KISS & YAGNI:** Keep code simple and avoid unnecessary features.
- **SoC & SRP:** Each function/class/module should have a single, clear responsibility.
- **DRY:** Reuse code and avoid duplication.
- **LEGB Rule:** Respect Python's Local, Enclosing, Global, Built-in scope order for variable resolution.
- **Readability:** Use descriptive names and break down complex logic into small, focused functions.
- **Edge Cases:** Proactively handle and document edge cases and exceptions.
- **External Libraries:** Use judiciously and document their purpose.

## 2. Documentation & Style

- Every function/class must have a PEP 257-compliant docstring.
- Use type annotations (`typing` module) for all public functions and methods.
- Follow PEP 8 for formatting (4 spaces, 79-char lines, blank lines between logical blocks).
- Place docstrings immediately after `def`/`class`.
- Add concise comments for non-obvious code and design choices.

## 3. Testing Guidelines (Pytest)

- **Organization:** Place all tests in `tests/`, name files as `test_<module>.py`.
- **Naming:** Test classes as `Test<ClassName>`, functions as `test_<functionality>`.
- **Structure:** Use `# Arrange`, `# Act`, `# Assert` comments. Prefer one logical assertion per test.
- **Type Hints:** Add to all test functions.
- **Fixtures:** Prefer function-scoped, named with `_fx`. Share in `conftest.py`.
- **Parametrize:** Use `pytest.mark.parametrize` for input matrices, including edge cases.
- **Async/IO:** Tag async tests, mock IO, use `pytest.raises` for exceptions.
- **Coverage:** Target ≥90% line coverage; document exclusions with comments.

## 4. Output & Example

- Return one fenced code block per file, using the filename as the info string (e.g., `filename=tests/test_math_utils.py`).

```python
# Example (SRP, KISS, DRY, LEGB):
def calculate_area(radius: float) -> float:
    """
    Calculate the area of a circle given the radius.

    Parameters:
    radius (float): The radius of the circle.

    Returns:
    float: The area of the circle, calculated as π * radius^2.
    """
    import math
    return math.pi * radius ** 2
```

## 5. AI Assistant Guidance

- Apply YAGNI, SoC, SRP, LEGB, KISS, and DRY in all code and suggestions.
- Prioritize clarity, maintainability, and idiomatic Python.
- Explicitly document and handle edge cases.
- When in doubt, prefer explicit, simple solutions over clever or concise ones.
