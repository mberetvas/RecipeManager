---
mode: agent
description: Convert plain class or dict schema to a dataclass
---

Input selection (`${selection}`) is either:
• A normal class definition  **or**  
• A dict-like schema comment.

Transform it into a `@dataclass(slots=True, frozen=True)` with:
1. Accurate field types (use `typing.Literal` for enums).
2. Default factory for mutable types.
3. A `from_dict` / `to_dict` pair.
4. Validation inside `__post_init__` using `pydantic`-style assertions.

Insert the dataclass **below** the selection in `${file}` and
highlight it with:

```python
# === GENERATED DATACLASS START ===
# === GENERATED DATACLASS END ===
```
