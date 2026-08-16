# 40 — Position & P&L Tracker — Specification (M, interview sim)

Tier-1 item 3 from IMPLEMENTATION_PROBLEMS.md, materialized. HRT
reports the same shape ("process a stream of timestamped trades,
compute running profit"; "replay events, answer queries about state"),
and it is the most trading-relevant problem on the shelf for all five
firms. Protocol: parts in order; no reading ahead. Python + pytest.

## Part 1 — position

Feed of fills `(symbol, side, qty, price)`. `position(symbol) -> int`,
signed. Symbols are independent — say the proof in one sentence.

## Part 2 — realized P&L, FIFO

A sell closes the OLDEST open lots first; a sell may consume part of a
lot, exactly one lot, or span several. `realized(symbol) -> float`.
Lot-matching is the order-book matching loop wearing accounting
clothes — if you've done 11/20, say so and reuse the shape.

## Part 3 — flips and shorts

Selling more than you hold flips the position short (open lots of
negative qty); buying covers shorts FIFO before opening new longs. A
single fill may realize P&L AND open a lot on the other side.

## Part 4 — marks

`unrealized(symbol, mark) -> float`. Conservation invariant, asserted
in tests after EVERY fill: realized + unrealized-at-mark equals the
cash result of liquidating everything at mark. Sum of open lot
quantities equals net position, always.

## Part 5 — stretch

Corporate action: split ratio R on date D multiplies qty and divides
basis of every lot open before D. Or: per-strategy attribution — each
fill carries a strategy tag; P&L must decompose exactly.

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
