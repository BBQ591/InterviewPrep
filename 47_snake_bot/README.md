# 47 — Snake + Computer Player — Specification (S, interview sim)

Reported Jane Street SWE intern FINAL-round question (2021, direct
candidate report; medium confidence on details beyond the one-line
ask: "build Snake and add a computer-controlled player"). You already
built Snake (08) — this is the sequel that makes it interview-shaped.
Protocol: parts in order; no reading ahead. Python + pytest. Timed:
Parts 1–2 in 60 minutes.

## Part 1 — the engine (adapt from 08, but injectable)

Grid W×H. Snake = ordered body segments, head first. `step(direction)`
advances one tick: hitting a wall or your own body ends the game;
reaching the apple grows the snake by one and spawns a new apple on a
free cell. Randomness is a PARAMETER — the apple sequence comes from a
seeded RNG or an injected iterator, never a global. Same seed, same
game, forever.

Contract you decide and test: the head moving into the cell the TAIL
is vacating this same tick — collision or not? (Classic ambiguity;
real implementations differ. Pick, document, test.)

## Part 2 — bot v1: shortest path

`next_move(game) -> direction` — BFS from head to apple, treating the
current body as obstacles, respecting your Part 1 tail-vacating
contract. The bot plays a full game via the engine's own `step` — no
private state channels. Test: on a seeded game, bot reaches the first
N apples without dying.

## Part 3 — bot v2: don't trap yourself

Shortest-path bots die by walling themselves in. Upgrade: only take a
move if, after taking it, the snake can still reach its own tail
(reachability check = you are not sealed in a pocket); if no
apple-path satisfies this, stall by following your tail. Test target:
bot survives to length ≥ (W*H)/2 on a small board, seeded.

## Part 4 — the transcript

Golden test: seed in, full game transcript out (every move, every
apple, final length), byte-for-byte stable. This is the determinism
deliverable that makes the whole thing gradeable — and it's the
mini-git Milestone 5 skill, reused.

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
