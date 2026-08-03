# 15 — Tiny Language Interpreter — Specification

## System

A small programming language, interpreted from source text. A program is a
sequence of statements. The language grows by phase (below), starting from
arithmetic and ending with user-defined functions.

Running a program produces output (from `print` statements) or a single error
message. It never crashes and never hangs.

## Input

- Source: a string of program text.
- Example (full language, P4):

      let n = 10;
      let fib = fn(k) {
        if (k < 2) { return k; }
        return fib(k - 1) + fib(k - 2);
      };
      print fib(n);

## Required behavior

1. `run(source) -> output`: output is the sequence of printed values, or an
   error. Every input — including garbage — produces exactly one of the two;
   no crashes, no exceptions escaping, no infinite loops on malformed input.
2. Errors carry a position: the line and column of the offending token.
3. **Reproducibility:** identical source must produce identical output, every
   run, byte for byte.

## Deliverables

1. The pipeline, as separately testable stages:
   - `lex(source) -> tokens`
   - `parse(tokens) -> AST`
   - `eval(AST) -> output`
   Each stage's input/output types are contracts — design them deliberately.
2. An AST printer: `parse` results rendered as text (e.g. `(* (+ 2 3) x)`),
   so parsing is testable without evaluating.
3. A REPL: read a line, evaluate, print, repeat. State persists across lines.
4. Tests per stage. Their design is part of the work.

## Later phases (same spec, growing scope)

- P1: integer arithmetic — `+ - * /`, parentheses, precedence. `print`.
- P2: `let` bindings, assignment, multi-statement programs, the REPL.
- P3: booleans, comparisons (`< > == !=`), `if`/`else`, `while`.
- P4: `fn` — user-defined functions with parameters, `return`, recursion,
  and proper scoping (a function's variables don't leak out; inner scopes
  see outer ones).
- P5: runtime error handling done properly — division by zero, undefined
  variable, calling a non-function, wrong argument count — each reported
  with position, each covered by tests.

## Notes

- This spec is deliberately underspecified in several places (what does
  `7 / 2` produce? is `0` true? may `let` re-declare an existing name? what
  is the value of an assignment?). Finding those places, deciding them, and
  writing the decisions down is part of the work.
- Process gate (your protocol): skeleton — stubs, one-sentence contracts, call
  graph, edge list — reviewed before any bodies are written. For this problem
  the critical skeleton decisions are the three data types: Token, the Expr/
  Stmt node hierarchy, and Value.
