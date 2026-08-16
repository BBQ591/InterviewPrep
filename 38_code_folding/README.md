# 38 — Editor Code Folding — Specification (S/M, interview sim)

A recurring Jane Street phone screen, 2023–2026 (Glassdoor, 1point3acres,
PracHub — SWE and MLE variants). You are filling in the core of a code
editor, not building the whole thing. Protocol: parts in order; no
reading ahead. Python + pytest.

## Part 1 — blocks

`parse(lines)` — blocks are delimited by braces; a block spans its
opening line through its closing line; blocks nest. One pass, stack.
For each opening line report the matching closing line; unbalanced
input is an error carrying line and column.

## Part 2 — fold / unfold

`fold(line)` — collapse the block that opens at `line`. `unfold(line)`.
`toggle(line)`. Folding a block nested inside an already-folded block
is legal and must be remembered when the outer block unfolds.

## Part 3 — render

`visible() -> list[str]` — what the user sees: a folded block
contributes only its header line (with a `...` marker); nested folds
compose. This is where a wrong Part 2 representation shows — if render
is hard, say what you'd change and change it.

## Part 4 — edits (stretch)

`insert(line, text)` / `delete(line)` — existing folds survive edits
that don't touch their delimiters; edits that break a delimiter unfold
that block. Decide and defend the contract for edits inside a fold.

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
