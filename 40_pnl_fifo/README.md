# 40 — Position & P&L Tracker — Specification (M, interview sim)

Tier-1 item 3 from IMPLEMENTATION_PROBLEMS.md, materialized. HRT
reports the same shape ("process a stream of timestamped trades,
compute running profit"), and it is the most trading-relevant problem
on the shelf for all five firms. Protocol: parts in order; no reading
ahead. Python + pytest. Timed: aim for the end of Part 3 in 75 minutes.

## The domain — complete, no trading knowledge needed

A **fill** is an executed trade: `(symbol, side, qty, price)` — side is
BUY or SELL, qty is a positive integer, price a number. You receive a
stream of fills and answer questions about the resulting holdings.

Your **position** in a symbol is the net signed quantity you hold:
BUYs add, SELLs subtract. Position +6 = you own 6; −3 = you owe 3
(short — see Part 3). Symbols never interact.

A **lot** is a remembered parcel from one fill that you still hold:
"10 shares bought at $100." Open lots are your inventory *with the
prices you paid attached* — that's what makes profit computable later.

**Realized P&L** is profit locked in by closing inventory: when you
sell shares you bought at 100 for 120, you realize (120 − 100) per
share. Losses realize the same way and are negative. **FIFO** is the
matching rule: a sell consumes the OLDEST open lots first.

**Unrealized P&L** is the profit you would have if you closed all
remaining open lots at a given **mark** price — profit on paper.

## Part 1 — position

`fill(symbol, side, qty, price)` ; `position(symbol) -> int` (0 for a
symbol never seen). Symbols are independent — one sentence out loud on
why (footprint of every op is one symbol).

## Part 2 — realized P&L, FIFO

`realized(symbol) -> float` — cumulative, starts at 0.

Worked trace, one symbol:

    fill(BUY, 10, 100)    # open lots: [10 @ 100]
    fill(BUY,  5, 110)    # open lots: [10 @ 100, 5 @ 110]
    fill(SELL, 12, 120)
      # FIFO: consume the oldest first —
      #   10 from the 100-lot: (120 - 100) * 10 = 200
      #    2 from the 110-lot: (120 - 110) * 2  =  20
      # open lots now: [3 @ 110]
    realized() == 220
    position() == 3

That trace is your first test, verbatim. A sell may consume part of a
lot, exactly one lot, or span several — all three cases, plus a losing
sell (realized goes negative), belong in the tests. Lot-matching is the
order-book matching loop wearing accounting clothes — if you've done
11/20, say so and reuse the shape.

## Part 3 — flips and shorts

Selling more than you hold is legal: the excess opens a **short**
position — inventory you owe, recorded as a lot at the price you sold
it. You profit by buying it back cheaper. Buying while short covers the
oldest short lots first (FIFO both directions); a single fill may
realize P&L closing one side AND open a lot on the other side.

Worked trace:

    fill(BUY,  5, 100)    # lots: [5 @ 100]
    fill(SELL, 8, 110)
      # closes the 5 long: (110 - 100) * 5 = +50 realized
      # 3 unsold remain -> short lot: [-3 @ 110]; position -3
    fill(BUY,  2, 90)
      # covers short FIFO: (110 - 90) * 2 = +40 realized (total 90)
      # lots: [-1 @ 110]; position -1
    realized() == 90
    position() == -1

## Part 4 — marks and the conservation oracle

`unrealized(symbol, mark) -> float` — value of closing every open lot
at `mark`. With signed lot quantities one formula covers both sides:
`sum((mark - lot_price) * lot_qty)` — check it on the short lot above:
(90 − 110) × (−3) = +60.

The killer test — an oracle you can compute with a dumb cash tally,
asserted after EVERY fill, for any mark:

    realized(s) + unrealized(s, mark)
        == cash(s) + position(s) * mark

where `cash(s)` = all money received from sells minus all money spent
on buys (the oracle knows nothing about lots or FIFO). If your lot
machinery ever disagrees with this, the machinery is wrong. Second
invariant, same rhythm: sum of open lot qtys == position, always.

## Part 5 — stretch, pick one

Corporate action `split(symbol, ratio, ...)`: every open lot's qty
multiplies by the ratio, its price divides (10 @ 100 → 20 @ 50 on a
2:1 split); realized P&L is untouched. Decide what happens to a short
lot. — Or: per-strategy attribution — each fill carries a strategy
tag; realized must decompose exactly by tag.

## Deliverables

Implementation + tests. Test design is part of the work — the two
worked traces are tests one and two; the conservation oracle is the
property test that carries the file. Deliberately underspecified in
places — finding the ambiguities and deciding those contracts is part
of the work.
