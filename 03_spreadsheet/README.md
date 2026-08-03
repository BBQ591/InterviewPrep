# 03 — Spreadsheet Engine

Cells hold values or formulas; changing a cell recomputes everything downstream.
The core insight: each cell is a **pure function of the cells it references**, and
recompute is a pass over a **dependency DAG** in topological order.

## Interface (`spreadsheet.py`)

```python
class Spreadsheet:
    def set_cell(self, name: str, contents) -> None:
        """contents is a number (int/float) or a formula string starting with '='."""

    def get_value(self, name: str):
        """Return the computed value of a cell (0 if the cell is unset)."""
```

## Formula syntax

Formulas start with `=` and may contain:

- **cell references**: `A1`, `B2`, `C10` (letter(s) + digits)
- **integers**: `5`, `42`
- **operators**: `+ - * /` with **standard precedence** (`*`/`/` before `+`/`-`)
- **parentheses**: `=(A1 + B1) * 2`

Examples:
```
=A1 + B2
=A1 * B1 + 1
=(A1 + A2) / 2
```

## Requirements

- **References resolve to other cells' values**, recursively.
- **Recompute on change**: after `set_cell("A1", 10)`, any cell referencing A1
  returns the updated value the next time you `get_value` it.
- **Cycle detection**: `A1 = "=B1"`, `B1 = "=A1"` must NOT infinite-loop —
  raise `ValueError("cycle")` (or your own sentinel) when a cycle is detected.
- Unset cells evaluate to `0`.

## Suggested design

- Parse each formula once into an expression tree (you can reuse ideas from the
  regex/lisp parsers — this is a mini arithmetic-expression evaluator with refs).
- To get a value: evaluate the expression, resolving each reference by recursively
  getting *its* value. Track the set of cells currently being evaluated to catch
  cycles. (Memoizing per recompute is a nice optimization.)
- Keep the evaluation a **pure function of (cell, sheet-state)** — no hidden mutation.

## Run the tests

```bash
python test_spreadsheet.py    # or: pytest
```
