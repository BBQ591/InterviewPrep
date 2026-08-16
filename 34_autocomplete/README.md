# 34 — Autocomplete — Specification (S/M, interview sim)

Protocol: parts in order; no reading ahead. Python + pytest.

## Part 1 — suggest

`build(phrases)` — initial corpus; duplicates count.
`suggest(prefix, k) -> list[str]` — the k phrases starting with prefix,
ordered by frequency descending, ties broken lexicographically.

## Part 2 — learning

`select(phrase)` — the user picked this phrase (from a suggestion or by
typing it fully); its frequency increases by 1. Phrases never seen
before enter the system this way with frequency 1. Later suggests
reflect it immediately.

## Part 3 — banning

`ban(phrase)` / `unban(phrase)` — banned phrases are never suggested,
but their frequencies keep counting (selects still accumulate), and
unbanning restores them at full weight.

## Part 4 (stretch) — one typo

`suggest(prefix, k)` additionally tolerates exactly one typo in the
prefix (one substituted, inserted, or deleted character). Exact-prefix
matches always rank above typo matches; within each tier, the Part 1
order applies.

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
