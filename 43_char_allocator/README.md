# 43 — malloc over a char[] — Specification (M, interview sim)

A reported Jump onsite, two-part by design: the interviewer checks that
Part 1's layout makes Part 2 possible BEFORE you write Part 2. C (or
C++ without the standard library's help). Protocol: parts in order; no
reading ahead.

## Part 1 — my_malloc

`void* my_malloc(size_t n)` over `static char heap[HEAP_SIZE]`. No
real malloc anywhere. Design block headers so that free is
implementable later — state the header layout out loud before coding.
Return NULL when it doesn't fit.

## Part 2 — my_free

`void my_free(void* p)` — adjacent free blocks must coalesce (both
directions). Freeing NULL is a no-op; double free is a contract you
decide (assert? corrupt? detect?).

## Part 3 — alignment

Every returned pointer 8-byte aligned, headers included. Recheck Part
1's arithmetic; this is where off-by-ones live.

## Part 4 — stretch

`my_realloc` (grow in place when the neighbor is free); or first-fit
vs best-fit behind one interface, with a fragmentation measurement
under the same randomized workload.

## Killer test

Randomized alloc/free sequences (seeded) against invariants: live
blocks never overlap, every byte is in exactly one block, no two
adjacent free blocks after any free, all live pointers still aligned.

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
