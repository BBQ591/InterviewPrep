# 37 — Connect-K — Specification (S/M, interview sim)

The most-reported Jane Street problem family of 2024–2026 (four variants
across SWE/MLE, intern and senior); Connect Four also appears in HRT's
board-game genre. Protocol: parts in order; no reading ahead. Python +
pytest. Timed: aim to finish Part 3 inside 60 minutes.

## Part 1 — Connect Four

Board W×H, two players alternating. `drop(col) -> row` — the piece
falls to the lowest empty cell; full column or bad index is rejected.
`winner() -> player | None` — four in a row, any direction.

## Part 2 — Connect-K

K is a constructor parameter. Win detection must check only lines
through the LAST move — no board rescans. State the complexity per move.

## Part 3 — unbounded columns

Column indices are arbitrary integers (negative fine); there is no
board edge left or right. Say out loud what representation this forces
before changing code.

## Part 4 — bottom push-up

New physics: a piece is inserted at the BOTTOM of its column, pushing
that column up one row. A single move can shift alignments in every row
the column touches — and can complete lines for BOTH players at once.
`play(moves) -> (index_of_first_winning_move, winners)` — winners is a
set; diagonals are excluded in this variant. Recheck only what could
have changed: the pushed column, plus the rows it intersects.

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
