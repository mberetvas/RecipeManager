---
mode: agent
description: Turn the current selection into an executable CLI script
---

Context: `${selection}` comes from `${file}`.

Produce a **stand-alone** script that:

1. Exposes a rich command-line interface via `argparse` (or `typer`
   if advanced features required).  
2. Adds `--verbose` and `--dry-run` flags automatically.  
3. Includes proper exit codes and colored logging (`rich` pkg).  
4. Ends with `if __name__ == "__main__": main()` guard.  
5. Supplies an installation comment (`# pip install ...`).

Return only the new script wrapped in a Python code fence.
