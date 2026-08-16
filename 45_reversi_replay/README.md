# 45 — Reversi Replay — Specification (S, interview sim)

Reported HRT question: given a list of Reversi (Othello) moves, return
the final piece count for each player. The HRT board-game genre in its
purest form — rules fidelity under time pressure. You are NOT expected
to know the game; the interviewer explains it exactly as below, and
asking clarifying questions about the rules is part of the exercise
(and scored well). Protocol: parts in order; no reading ahead. Python +
pytest. Timed: 45–60 minutes.

## The game — complete rules, no outside knowledge needed

8×8 board, rows and cols indexed 0–7. Two players, BLACK and WHITE.
BLACK always moves first. The game opens with four pieces in the
center:

             col 3   col 4
    row 3:     W       B
    row 4:     B       W

(This exact orientation is the contract your tests assume.)

A move is placing one piece of your color on an EMPTY cell. The move
must "bracket" at least one run of opponent pieces:

- From the placed cell, look along each of the 8 directions
  (horizontal, vertical, diagonal).
- A direction brackets a run when the cells immediately adjacent in
  that direction are one or more CONTIGUOUS opponent pieces, and the
  run is terminated by a piece of YOUR color — with no empty cell and
  no board edge before that terminator.
- Every bracketed run, in every qualifying direction at once, flips:
  those opponent pieces become your color. Flipping is simultaneous
  and does NOT cascade — a piece flipped this move never triggers
  re-checking of further runs.

Worked example: from the opening, BLACK plays (2, 3). Looking down:
(3,3) is White (contiguous opponent), then (4,3) is Black (own piece,
terminates) → the run {(3,3)} is bracketed and flips to Black. No
other direction brackets anything — e.g. down-right hits (3,4) which
is already Black, so there's no opponent run to bracket. Result:
Black 4, White 1.

Turns alternate. A player with NO legal move anywhere passes
automatically — the opponent moves again. The game ends when both
players pass consecutively, or the board is full. The output of this
problem is the final piece counts: a census of EVERY piece standing on
the board at the end — the opening four, plus each piece placed, with
all flips applied. It is not a count of flips or of moves. (That's why
the worked example ends 4–1: opening 2+2, black places a fifth piece,
one white piece converts.)

## Part 1 — flips

Apply one move for a given player: place the piece, flip every
bracketed run in all 8 directions. Get "contiguous opponent pieces
terminated by your own, no gaps, no edge" exactly right — this is
where the mirror bugs live, and a run of length ≥ 2 must flip in full.
First test: the worked example above.

## Part 2 — legality and passing

A move is legal only if it flips at least one piece (placement on an
occupied cell is likewise illegal). Implement `legal_moves(player)`.
A player with no legal move passes automatically — there is no pass
entry in a move list. Game over when both pass consecutively or the
board is full.

## Part 3 — replay

`replay(moves) -> (black_count, white_count)` — moves is an ordered
list of `(row, col)`. The owner of `moves[i]` is whoever's turn it is
AFTER applying automatic passes — NOT simple alternation by index; a
parity assumption here is the planted bug of this problem. An illegal
move is an error carrying its index. Decide and test: is a move list
that continues after the game has ended an error, or are the extra
moves ignored?

Test you can write immediately: `replay([(2, 3)]) == (4, 1)`.

## Part 4 — stretch

A greedy bot: maximize immediate flips, deterministic tie-break
(lowest row, then lowest col). Play it against itself from the opening
and golden-test the full game transcript.

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
