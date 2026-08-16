# 41 — Order Book from a Feed — Specification (M)

A real Jump Trading take-home, reconstructed from candidate reports
(the serialized format below is theirs), and tier-1 item 4 from
IMPLEMENTATION_PROBLEMS.md. C++ — that is the point. Your order book
from 20, inverted: consume events instead of producing them.

## Input

One message per line:

    A,order_id,side,qty,price     add resting order (side B or S)
    X,order_id,side,qty,price     cancel/delete
    T,qty,price                   trade report

## Required behavior

1. After every message, output the mid: (best_bid + best_ask) / 2, or
   `NAN` while either side is empty.
2. After every 10th message, print the full book — both sides, price
   levels with aggregate qty, best levels first.
3. Track total traded volume per price level from T messages.
4. Malformed or inconsistent input must never throw or crash: unknown
   order_id on X, duplicate order_id on A, a T with no plausible
   resting liquidity, garbage fields. Log and continue. Deciding what
   "inconsistent" means — and what recovery preserves — is part of
   the work.

## Killer test

Golden files: message log in, full output out, byte-for-byte diff
(your Milestone 5 skill from mini-git, reused). Plus a fuzz feed:
random valid + corrupted messages, asserting only invariants (best_bid
< best_ask when both exist; level qty == sum of resting orders).

## Stretch

Sequence numbers on messages; detect gaps, report them, and define
book state during a gap.

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
