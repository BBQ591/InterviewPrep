# 23 — Ledger with Transfer Undo — Specification (S/M)

Event-sourced bank. Python. The replay idea from 17, plus union-find to
replay LESS.

## System

An append-only log of events, ids in arrival order:
`deposit(acct, amt)`, `withdraw(acct, amt)`, `transfer(from, to, amt)`.
Balances are a fold over the log. `void(event_id)`: event never happened
(fraud); recompute the world — but you may only replay accounts whose
history could have changed.

## The independence

Deposits/withdrawals key by ONE account; a transfer keys by TWO — it welds
its accounts together. The affected set of a void is the connected
component (union-find over the log's transfer edges) containing the voided
event's account(s). Everything outside the component provably can't change
— that's move 2: say the disjointness.

## Required behavior

1. Killer property: component-only replay == full global replay, on seeded
   random logs, after every void. The global replay is your oracle; the
   component version is the product.
2. ? A withdraw that becomes invalid after the void (balance would go
   negative during replay): fail-and-drop it, cascade-void it, or allow
   negative balances? Decide, write it down, test the decision.
3. Second operation: void the same event twice; void an event that a
   cascade already dropped; void, then append new events, then void again.
4. get_balance never mutates; folds are pure (principle 6/13 — the log is
   the single source of truth, balances are derived).

## Phases

P1: fold + balances, no void. P2: void by full global replay (this is the
oracle forever). P3: union-find + component replay. P4: seeded fuzz of
random logs and random voids, property from (1) after every operation.
