# 42 — Rate Limiter — Specification (S, interview sim)

Everyone's interview list (tier-1 item 2 in IMPLEMENTATION_PROBLEMS.md);
a titled Jump question from 2025–2026 reports. Protocol: parts in
order; no reading ahead. Python + pytest. The clock is a parameter —
never time.time() inside the logic.

## Part 1 — token bucket

`allow(now) -> bool` — capacity C tokens, refill rate R per second,
continuous refill. Whether tokens refill fractionally and whether the
bucket starts full are contracts you decide and test.

## Part 2 — sliding window log

Exact limit: at most N allowed requests in ANY trailing window of W
seconds. Memory must not grow past O(N) — prune. A request exactly at
the window edge is a contract decision; make it and test it.

## Part 3 — per-key

`allow(key, now) -> bool` — independent limit per key. Millions of
keys that went quiet must not leak memory; say when and how state for
an idle key dies.

## Part 4 — composition

Per-key limit AND a global limit at once. A request must consume from
both or neither — no partial spend. This is the independence-death
move: per-key state no longer suffices; say which assumption broke.

## Deliverables

Implementation + tests. Test design is part of the work — fake clock
advancing, allow/deny asserted per tick, fully deterministic.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
