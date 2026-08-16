# 36 — Memoizing Cache — Specification (S, interview sim)

Jane Street's canonical phone screen — self-published on their blog and
still the most-cited screen problem. Protocol: parts in order; don't
read Part N+1 until Part N is green. Python + pytest. Timed: 60 minutes
to the end of Part 3, narrating out loud.

## Part 1 — memoize

`memoize(f) -> g` — wrap an expensive pure function; `g(x)` computes
`f(x)` at most once per distinct input. Prove it with a call counter in
the tests, not by inspection.

## Part 2 — the memory leak

"We call f with millions of distinct inputs — that table grows
forever." `memoize(f, capacity)` — at most `capacity` entries; evict
FIFO. Every operation O(1).

## Part 3 — LRU

Eviction is now least-recently-USED: a cache hit refreshes recency.
Still O(1) per operation. (In the real round most candidates don't
finish this part; the interviewer probes the design — say the two
structures and why each exists before writing either.)

## Part 4 — stretch, pick one

TTL entries (clock as a parameter, never time.time()); or LFU eviction
(IMPLEMENTATION_PROBLEMS.md tier 1 — the much harder sequel); or
hit/miss/eviction stats without breaking O(1).

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
