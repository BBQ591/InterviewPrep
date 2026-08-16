# 46 — OA Warmups — drill bench (20–40 min each, timed)

Not a project: a bench of small problems actually reported at the
target firms (sources in INTERVIEW_RESEARCH.md). Use one as a warmup
before a sim, or on interview morning. Every one is timed, every one
gets at least a written test list. Ordered roughly by reported
frequency.

1. **Stack with inc(k, x) and sum()** — push/pop/peek plus "add x to
   the k bottom elements" and "sum of all elements", EVERY op O(1).
   The most-reported IMC OA problem, 2020–2026 (looping inc TLEs —
   there is a lazy trick).
2. **Knight vs bishop BFS** — N×N (~150), min knight moves from start
   to end, never landing on a square the stationary bishop attacks.
   IMC OA, reported unchanged 2020–2022.
3. **Bus seats** — infinite seats from 1; each person in a queue wants
   seat s; if taken, they rejoin the back wanting s+1. Final seating in
   ~O(N) (next-free-seat pointers = union-find). IMC OA 2024.
4. **Unit conversion** — facts like (m, ft, 3.28); answer arbitrary
   conversion queries, including chained and impossible ones. Jane
   Street's own published mock interview; graph + BFS.
5. **push() / randomPop()** — uniform random removal, both ops O(1),
   complexity discussion. HRT.
6. **Merge two time series** — two lists of (ts, value) tuples, merge
   into one ordered series; decide the equal-timestamp contract. Jump.
7. **Stack calculator** — tokenize and evaluate `3 + 4 * (2 - 1)`
   with precedence, two stacks or shunting yard. Jump, multiple
   reports (~30 min live).
8. **Tree merge, ordered children** — trees as [key, value, *children],
   child order significant; merge two, right wins on key collision.
   HRT.
9. **Kth permutation** — without enumerating the first k-1. Jump OA.
10. **Pretty numbers** — count numbers < n whose base-4 representation
    uses only digits 0 and 1. HRT.
11. **Buried artifacts** — battleship-style shapes on an n×n grid plus
    a list of excavated cells; count fully vs partially uncovered
    artifacts. IMC OA 2020–2021.

## Deliverables

One file per drill as you do them, `NN_name.py` + tests, with the time
you took noted at the top. No polishing after time is called.
