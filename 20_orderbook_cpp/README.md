# 20 — Order Book, C++ — Specification

Port the 11_order_book matching core to C++. The design goal is stated up
front: mirror bugs (category 2) cost four defects in the Python book. This
port makes the mirror unrepresentable — ONE

```cpp
template <typename Compare> class BookSide;
```

written once, instantiated `BookSide<std::greater<Price>>` for bids and
`BookSide<std::less<Price>>` for asks. Success criterion: no bid/ask branch
exists anywhere inside BookSide. There is a single comparator expression
that decides "does taker limit L cross maker best B" for BOTH sides —
finding it is part of the work.

## Interface

```cpp
struct Order { OrderId id; Side side; Price price; Qty qty; };
struct Trade { OrderId taker_id; OrderId maker_id; Price price; Qty qty; };
// named structs at the boundary — principle 11; the Python 5-tuple stays dead

class OrderBook {
  // submit_limit(Order) -> std::vector<Trade>
  // cancel(OrderId) -> bool
  // best_bid() / best_ask() -> std::optional<Price>
  // depth(Side, Price) -> Qty
};
```

## Inside a side

`std::map<Price, std::deque<Order>, Compare>` — best level is begin();
price-time priority is the map order + FIFO within the level. Cancel needs
an id → location index: category 4, facts stored twice, back for round two.
C++ raises the stakes: std::map iterators are stable, std::deque's are
NOT — storing a deque iterator in the index is a segfault on schedule. That
asymmetry forces a real decision: `std::list` per level (stable iterators,
eager erase) vs deque + lazy tombstones (the corpse pattern from the event
scheduler). Choose, write it down.

## Required behavior

- Trade price is the MAKER's price (the bug you hit twice — golden-test it
  first).
- Partial fills; the remainder rests. FIFO within a level.
- cancel(unknown id) → false. cancel twice → the second is false. (Decided
  contracts, tested.)
- `check_rep()`, called after every op in tests: book never crossed
  (best_bid < best_ask when both exist), id-index and book agree exactly,
  no empty price levels linger, all resting qtys > 0. Principle 3 as
  executable code.

## Killer test — cross-language oracle

A tiny Python script emits a seeded random order stream as JSON lines. The
SAME stream runs through the Python book (the oracle you already trust) and
this book; trade logs and final depth snapshots must match byte for byte.
The golden-file skill from Milestone 5, promoted to cross-language. Keep the
stream files — they're regression tests forever.

## Phases

- P1: one `BookSide<std::less<Price>>` alone — add, best,
  pop-front-of-best, FIFO, check_rep.
- P2: OrderBook, both instantiations, the matching loop.
- P3: cancel + the id index (the decision above).
- P4: the cross-language oracle.
- P5 (stretch): IOC/FOK (the short-by-one lives here — boundaries) or a
  depth cache: facts-stored-twice on purpose, cross-checked in check_rep.

## Build

g++/clang++, `-std=c++20 -g -fsanitize=address,undefined`; asserts always
on in tests. Process gate: skeleton — stubs, one-sentence contracts, the
BookSide/OrderBook boundary — before any bodies. Narrate the invariants out
loud while writing; that's the IMC/Jump muscle.
