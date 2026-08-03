# 01 — Regex Engine

Implement a regular-expression matcher.

## Interface (`regex.py`)

```python
def match(pattern: str, text: str) -> bool:
    """Return True iff `pattern` matches the ENTIRE `text` (full match)."""
```

## Supported syntax

| syntax | meaning |
|--------|---------|
| `abc` | literal characters |
| `.` | any single character |
| `*` | zero-or-more of the preceding element |
| `a|b` | alternation (a or b) |
| `(...)` | grouping |

Bonus: add `+` (one-or-more) and `?` (zero-or-one).

## Suggested design (keep it functional)

The classic, clean approach — pure functions all the way down:

1. **parse** `pattern` → AST  (parser combinators: tiny functions like `char`,
   `alt`, `seq`, `many`, composed together — no mutation).
2. **compile** AST → NFA  (Thompson's construction: each AST node becomes a small
   state machine you wire together).
3. **simulate** NFA over `text`  — keep a *set* of active states, step it one char
   at a time (BFS over states), accept if an accepting state is in the set at the end.

A direct recursive matcher also works (see Russ Cox, "Regular Expression Matching
Can Be Simple And Fast"), but the parse→NFA→simulate pipeline is the better FP +
data-structures exercise.

## Run the tests

```bash
python test_regex.py      # or: pytest
```
