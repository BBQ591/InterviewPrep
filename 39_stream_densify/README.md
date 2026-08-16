# 39 — Tick Stream Densifier — Specification (S, interview sim)

From a reported Jane Street new-grad screen (PracHub, 2026): the
market-data-shaped streaming genre. Protocol: parts in order; no
reading ahead. Python + pytest.

## Given

M code strings (they are the columns, in lexicographic order) and a
stream of batches of `(timestamp, code, value)` triples. Output: one
dense row per timestamp — `[ts, v_1 .. v_M]` — with `-1` for any code
that never ticked at that timestamp.

## Part 1 — ordered

Input fully ordered: timestamps nondecreasing, one timestamp never
reappears after the next begins. Emit each row as soon as it is
complete. At most one row of state in memory.

## Part 2 — disorder within a timestamp

Codes belonging to one timestamp arrive in any order; the same code may
tick twice in a timestamp — last write wins.

## Part 3 — bounded disorder

Timestamps arrive out of order, bounded by `max_lag`: once `t` is seen,
nothing older than `t - max_lag` will ever arrive. At each batch
boundary emit, in timestamp order, every row that is now safe
(`ts <= max_seen - max_lag`). Dict of open rows + a heap of timestamps;
this is watermark logic — name it.

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
