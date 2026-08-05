# 29 — Versioned KV Store — Specification (S/M, interview sim)

Protocol: parts in order; no reading ahead. Python or C++ — your call.

## Part 1 — put / get, with time travel

`put(k, v) -> version` — a single global version counter increments on
every put.
`get(k) -> v | none` — the latest value.
`get(k, version) -> v | none` — the value as of that version: the latest
write to k whose version is <= the given one.

## Part 2 — snapshots

`snapshot() -> token` — must be O(1).
`get(k, token)` — reads at the snapshot; unaffected by any later writes.

## Part 3 — restore

`restore(token)` — the store's latest state becomes what it was at the
snapshot. History is never rewritten: afterward, `get(k, v)` for any
older version still answers exactly as before, and a later `restore` can
undo this one.

## Part 4 — diff

`diff(v1, v2) -> {added, removed, changed}` across all keys, comparing
the state as of v1 with the state as of v2.

## Part 5 (stretch) — delete

`delete(k) -> version` — afterward `get(k)` is none, while
`get(k, older_version)` still sees the value.

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
