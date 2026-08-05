# 21 — Marketplace with Wallets — Specification (S)

Sequel to 17 — build directly on that code. This is the problem where the
independence you found in 17 dies. Python + pytest.

## Change

`register_buyer(name, budget)` — each buyer has a wallet. Total spend across
ALL of a buyer's purchases must never exceed their budget. `buy_items` skips
any item the remaining budget can't cover. `remove_buyers` keeps its
signature; refunds are credited back to wallets.

## The point

In 17, replay decomposed by item_name — a request touched only its name's
items and history, so requests for different names commuted. The wallet is
shared across names: two requests by the same buyer for different names no
longer commute. Per-name replay is dead; replay goes global, surviving
requests in original order, wallet-aware.

## Required behavior

1. Conservation, checked after every op: each buyer's total spend <= budget.
2. Refund = original spend − replay spend, per remaining buyer.
3. Fold oracle (as in 17): final state == folding surviving requests, in
   original order, over the initial state, wallets included.

## The killer test — the deliverable that proves you get it

Construct a concrete case where per-name replay and global replay give
DIFFERENT allocations, and commit it as a test against the (correct) global
version. Shape hint: one buyer, tight budget, two names — a removal frees a
cheaper item in name A, which frees budget that changes the outcome in
name B. Per-name replay of B can't see the freed budget. If you can't build
this case, you don't yet understand why the wallet broke the factoring.

## Contracts to decide (?)

- ? Within one buy_items call, names process in what order? (Dict insertion
  order is the honest answer — write it down; it now MATTERS, budget drains
  as you go.)
- ? An item is affordable by max_price but not by remaining budget: skip
  that name, or abort the whole call?
- ? remove_buyers on a buyer whose refund would overdraw... can that even
  happen? Convince yourself, in a comment.
