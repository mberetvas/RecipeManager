---
description: "Generate pytest unit tests for the selected Python function or class."
---
# Task: Generate Pytest Unit Tests

You are a Test Automation Engineer. Write a suite of unit tests for the following Python code using the `pytest` framework.

**Code to Test:**

`${selection}`

# Instructions:

- Create clear and descriptive test function names (e.g., test_my_function_with_valid_input).
- Use pytest fixtures if setup/teardown is required.
- Generate tests that cover:
-    The "happy path" with typical inputs.
-    Edge cases (e.g., empty lists, zero, None).
-    Expected failure conditions (e.g., invalid input raising a ValueError). Use pytest.raises for this.
- Reference our testing guidelines: [my-testing-conventions.instructions.md]
