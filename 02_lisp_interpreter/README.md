# 02 — Lisp Interpreter

A tree-walking evaluator for a mini-Lisp. This is the classic "learn FP by building
it" project (SICP's metacircular evaluator).

## Interface (`lisp.py`)

```python
def run(source: str):
    """Evaluate a program (one or more expressions). Return the value of the LAST."""
```

## Supported language

| form | example | notes |
|------|---------|-------|
| integers | `42` | |
| arithmetic | `(+ 1 2 3)` `(* 2 3)` `(- 10 3)` `(/ 6 2)` | fold left; `+`/`*` variadic |
| comparison | `(< 1 2)` `(> 3 1)` `(= 2 2)` | return Python `True`/`False` |
| conditional | `(if (< 1 2) 10 20)` | |
| variables | `x` | looked up in the environment |
| define | `(define x 5)` | binds a name |
| lambda | `(lambda (a b) (+ a b))` | anonymous function |
| application | `((lambda (x) (* x x)) 5)` | |

Closures must work: a lambda captures the environment it was defined in.

Bonus: function-define sugar `(define (sq x) (* x x))`, and `let`.

## Suggested design (naturally functional)

1. **tokenize** `source` → tokens  (split on parens/whitespace).
2. **parse** tokens → nested lists (the AST) — a recursive descent; pure.
3. **eval(expr, env)** → value — a pure recursive function:
   - a number evaluates to itself
   - a symbol looks up `env`
   - `(if c t e)`, `(define n v)`, `(lambda ...)` are special forms
   - otherwise it's a call: eval the operator + args, then apply.
4. **env** = a dict with a pointer to its parent (scope chain). A lambda closes over
   its defining env. Keep `eval` from mutating anything except when `define` binds.

Try to keep `eval` a pure function of `(expr, env)`.

## Run the tests

```bash
python test_lisp.py       # or: pytest
```
