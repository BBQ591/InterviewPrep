# 25 — Substitutable Inventory — Specification (S)

The subtlest lesson in the genre: independence isn't yes/no — it lives at a
GRANULARITY, and finding the level where it holds is the design act.
(In 17 the level was item_name, not item.) Python.

## System

SKUs for sale, each with a price, quantity 1 (marketplace-style). Named
classes are sets of SKUs: "blue-shirt" = {s1, s3}, "medium-shirt" =
{s3, s5}. A request is `(class_name, max_price)`: buyer takes the cheapest
available SKU in the class, or nothing.

## P1 — disjoint classes

Guarantee (assert it): no SKU in two classes. Requests for different
classes are independent — say the proof. Greedy cheapest-per-request is
correct. This should take twenty minutes; it exists to set up P2.

## P2 — overlapping classes (the kill)

Drop the disjointness assert. Greedy now misallocates: construct the case —
two requests, small store, one shared SKU that greedy hands to the first
request, starving the second, when an allocation serving BOTH exists.
Commit that case as a failing test against greedy.

What happened: SKU-level independence was always false; class-level
independence was true only while classes were disjoint; the level that
survives overlap is CONNECTED COMPONENTS of the class-overlap graph.
Requests in different components still can't interact — say why.

## P3 — decide how correct to be

Within a component this is bipartite matching (requests vs SKUs). Options:
maximum matching via augmenting paths (~30 lines, worth having written
once), or documented-greedy with its failure cases stated. Choose,
justify in writing.

## Killer test

Brute-force oracle on small random instances (enumerate all allocations):
your allocator must fill the MAXIMUM number of requests. Property-test it
seeded. Per-component solve == whole-problem solve, always (the
independence claim, checked).

## Contracts to decide (?)

? Tie among cheapest eligible SKUs — deterministic rule, write it down.
? "Maximum requests filled" vs "minimum total price" can conflict —
  which wins? (Pick one; note the other as the stretch.)
