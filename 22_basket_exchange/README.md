# 22 — Multi-Symbol Exchange + Basket Orders — Specification (S/M)

Sequel to 20 — C++, built on your OrderBook. Part 1 is trivial ON PURPOSE;
Part 2 kills the property that made it trivial.

## P1 — Exchange

`Exchange` = `map<Symbol, OrderBook>`; every order names one symbol; route
it. Deliverable is a three-line comment stating the independence proof: an
order touches exactly one book; books share no state; therefore ops on
different symbols commute and the exchange is embarrassingly parallel.
Writing the proof down is the point — P2 will negate it.

## P2 — Basket orders (the kill)

`submit_basket({leg...})` where a leg is (symbol, side, limit, qty): fill
EVERY leg or NONE, atomically. No partially-executed basket may ever be
observable. Symbols now couple.

The design decision, written down before code:
- **check-then-fill**: simulate every leg against current books (including
  walking multiple price levels), fill only if all pass. What could change
  between your check and your fill in this single-threaded world? Convince
  yourself — and say what breaks the argument the day matching gets
  concurrent.
- **fill-then-unwind**: fill legs in order; on a failed leg, roll back the
  earlier ones. Unwind = rollback, and you've built 17/19 — but trades
  already emitted are facts. Can you un-emit a trade? (This is why real
  exchanges mostly don't do it this way.)

## Required behavior

- check_rep after every op: no basket partially applied, plus all of 20's
  invariants per book.
- Two baskets sharing liquidity: either serial order is legal; interleaved
  half-states are not. Test both submission orders; assert all-or-nothing
  each time.
- A basket where each leg is fillable alone but not both together (shared
  liquidity through DIFFERENT symbols is impossible — say why; through the
  same symbol on both legs is the test case).

## P3 (stretch)

Resting baskets: a basket that waits until all legs are simultaneously
marketable. Contingent-order matching is genuinely hard — scope it, don't
finish it; the scoping writeup is the deliverable.
