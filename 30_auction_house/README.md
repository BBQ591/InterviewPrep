# 30 — Auction House with Proxy Bids — Specification (M, interview sim)

Protocol: parts in order; no reading ahead. Python + pytest. The clock
is a parameter everywhere.

## Part 1 — listings and proxy bids

`list_item(item_id, seller, min_bid, end_time)`
`place_bid(bidder, item_id, max_amount, now) -> current_price | None`

Proxy bidding: a bidder states the most they are willing to pay, and the
system bids on their behalf. The current price is
second_highest_max + 1, capped at the highest max; while there is only
one bidder, the current price is min_bid. The highest max is winning;
on equal maxes, the earlier bid wins. Bids after end_time or below
min_bid are rejected.

Worked example: min_bid 10. Alice bids max 50 → current price 10.
Bob bids max 80 → current price 51. Carol bids max 60 → current
price 61. If it closed now: Bob wins at 61.

## Part 2 — closing

`close(now) -> dict[item_id, (winner, price)]` — settles every auction
whose end_time <= now, exactly once each.

## Part 3 — retraction

`retract_bidder(bidder, now)` — a bidder is banned and all their bids
are withdrawn.
- Auctions not yet settled: proceed as if that bidder's bids had never
  been placed.
- Settled auctions this bidder won: the sale is voided and re-awarded
  to the correct winner at the correct price, as if the banned bidder
  had never bid. Settlements not performed through this instance are
  never touched.
- Returns the price changes / refunds per affected bidder.

## Part 4 (stretch) — exposure cap

Each bidder has a limit: the sum of their current-price commitments
across all open auctions may not exceed it. Bids that would exceed the
cap are rejected at placement time.

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
