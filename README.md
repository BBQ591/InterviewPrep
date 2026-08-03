# FP Preparation — Implement-Against-Tests

Practice projects that combine **functional-programming discipline** (pure functions,
immutability, composition) with **real data structures**. Each folder has:

- `README.md` — the spec + the interface you must implement
- `<name>.py` — a skeleton with the signatures (raises `NotImplementedError`)
- `test_<name>.py` — a test suite you code against (goes green as you implement)

## The one rule

Keep a **pure functional core**: no mutation, no I/O in the logic. Push effects
(printing, the REPL loop, file reads) into a thin outer shell. If a core function
mutates shared state or prints, refactor it to *return* a value instead.
"Functional core, imperative shell."

## How to use

```bash
cd 01_regex_engine
# read README.md, then fill in regex.py
python test_regex.py          # standalone, no dependencies
# or, if you have pytest:  pytest
```

The runner prints `PASS` / `FAIL` / `TODO` (still NotImplementedError) per test.
Green everything, then move to the next folder.

## Recommended order

| # | project | FP muscle | data structure |
|---|---------|-----------|----------------|
| 01 | **regex engine** | parser combinators, pure AST | automata (NFA), BFS over states |
| 02 | **lisp interpreter** | tree-walking eval, immutable envs | recursive AST, scope chain |
| 03 | **spreadsheet** | pure recompute, no mutation in logic | dependency DAG, topological order |
| 04 | **rope** | immutability → free undo | balanced tree, structural sharing |

## Discipline while building

- **Time-box it** (you did skip list in 45 min — keep that pressure).
- Make tests green **one at a time**.
- **Say the invariant out loud** before you code it ("the book is sorted by price";
  "each cell is a pure function of its refs"). That's the muscle interviewers grade.
- Add your own edge cases to each `test_*.py` — the suites are a floor, not a ceiling.
