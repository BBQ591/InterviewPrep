# 11 — Limit Order Book & Matching Engine

The project: an exchange's core. Orders come in ("buy 100 @ $10.50"), rest in a book,
and match against each other by price-time priority, producing trades.

Why this one, given your goals:

- **Unit testing** — the matching logic is 100% pure: `(book, order) -> (new_book, trades)`.
  No randomness anywhere. Every behavior pins down with exact `==` asserts.
- **Knowing what to test** — matching is dense with boundaries (exact-quantity fills,
  one-share-over, price ties, time ties) and rich in invariants (shares are conserved,
  the book is never crossed). Perfect terrain for practicing test *selection*.
- **Big projects** — it grows in layers: data structure -> matching -> order management ->
  event-driven replay -> simulator. Each layer has its own testing lesson.
- **Interviews** — order book questions are a staple at trading firms. Having built one,
  tested it, and being able to *talk about how you tested it* is directly bankable.

## Ground rules (lessons carried from 10_Match3)

1. **Functional core, imperative shell.** All matching logic is pure functions over
   plain data. Anything nondeterministic (clocks, IDs, randomness in the simulator)
   is passed IN as data, never generated inside the logic. If a function is hard to
   test, the shape is wrong — fix the function, not the test.
2. **TDD from line one.** Every behavior gets a failing test before the code exists.
   Watch it fail, make it pass, refactor.
3. **Before each milestone, write your edge-case list on paper first**, out loud,
   before opening the spoiler in that milestone. The gap between your list and the
   spoiler list is exactly the "knowing what to test" skill being measured.
4. Name the file `test_book.py` (pytest only auto-discovers `test_*.py`).
   `python3 -m venv .venv && source .venv/bin/activate && pip install pytest hypothesis`

## Milestone 1 — The book (no matching yet)

Orders: `(id, side, price, qty)`. Support: insert a limit order, `best_bid()`,
`best_ask()`, and depth at a price level. No crossing yet — assume orders never match.

Decide and document your book representation (two sorted structures? dict of price
levels holding FIFO queues?). The representation decision is the design content here.

<details><summary>Edge-case list (write yours first)</summary>

- empty book: what do `best_bid`/`best_ask` return? (Define the contract: None? raise?)
- single order each side
- two orders same price -> FIFO order within the level preserved
- better price arrives -> best bid/ask updates
- bids sort descending, asks ascending (opposite directions — classic sign-flip bug)
</details>

## Milestone 2 — Matching (the heart)

`match(book, incoming) -> (new_book, trades)`. Price-time priority: best price first,
oldest first within a price. Partial fills rest on the book. Trades execute at the
**resting** order's price.

This is the milestone to slow down on. Test it like `find_runs` — exhaustively,
with tiny hand-built books.

<details><summary>Edge-case list (write yours first)</summary>

- incoming qty == resting qty exactly (both vanish; nothing rests)
- incoming qty one MORE than resting (remainder rests on the other side)
- incoming qty one LESS (resting order shrinks, keeps its time priority)
- incoming sweeps multiple price levels -> multiple trades, correct prices each
- incoming crosses several orders at the SAME level -> fills in FIFO order
- incoming doesn't cross at all -> rests, zero trades
- price improvement: buy @ 11 hits ask @ 10 -> trade at 10, not 11
- empty opposite side -> rests untouched
</details>

<details><summary>Invariants (these become hypothesis property tests)</summary>

- **Conservation**: incoming qty == sum of trade qtys + qty now resting. Always.
- **Never crossed**: after match() returns, best_bid < best_ask (when both exist).
- **No spontaneous liquidity**: every trade's maker id was in the book beforehand.
- Property test: feed random order streams; assert all three after every event.
  Zero exact values needed — this is the test style that needs no expected grid.
</details>

## Milestone 3 — Order management

Cancel by id. Modify (cancel+replace: loses time priority).

<details><summary>Edge-case list (write yours first)</summary>

- cancel a resting order; cancel a PARTIALLY FILLED order (remaining qty only)
- cancel an id that doesn't exist / was already fully filled (define the contract!)
- cancel the only order at a level -> level disappears; best price updates
- replace loses queue position: old #1 at level, replaced -> now behind others
</details>

## Milestone 4 — Order types

Market orders, IOC (fill what you can, cancel the rest), FOK (fill entirely or not at all).

<details><summary>Edge-case list (write yours first)</summary>

- market order vs empty book (contract decision: reject? partial-cancel?)
- FOK boundary: available liquidity exactly equal / one short -> all-or-nothing flip
- IOC never rests, ever — even for one leftover share
</details>

## Milestone 5 — The big-project layer: event-driven replay

Now build the imperative shell: read a file of events (`ADD`, `CANCEL`, ...), feed
them through the pure core, write a trade tape and final book snapshot.

Testing lesson: **golden-file / end-to-end tests**. A scenario file in, an expected
tape out, full `==`. Deterministic because the core is pure — this is the payoff of
ground rule 1. Keep 3–4 scenario files under `scenarios/`. When a unit-level change
breaks a golden test, that's integration coverage doing its job.

## Milestone 6 (stretch) — Simulator

Random agents post/cancel orders; run 100k events; print stats (spread over time,
volume). Randomness comes from a seeded generator passed IN. One property run:
all Milestone-2 invariants hold across the entire simulation. Then benchmark and
optimize the book structure — with the test suite as your safety net while refactoring.
That experience (aggressive refactor, suite stays green) is the single best argument
for testing you'll ever feel firsthand.

## Interview drill (after finishing)

Redo Milestones 1–2 from scratch in 45 minutes, speaking out loud, tests as you go.
Twice. This is the closest home rehearsal of a trading-firm practical round that exists.

## After this: 12 / 13 / 14 candidates

- **12_chess_moves** — legal move generator, tested with *perft*: count all move
  sequences to depth N and compare against published exact numbers (perft(4) from
  the start position = 197,281). One number that verifies millions of paths — the
  most humbling "knowing what to test" exercise there is. Castling/en-passant/pins
  will fight you.
- **13_kv_store** — persistent key-value store: append-only log, in-memory index,
  compaction. New testing skill: crash recovery (kill the write at every byte offset,
  reopen, assert no acknowledged write is lost). Systems-flavored, bigger scope.
- **14_editor** — wire your 04_rope into a real editor buffer: cursor, undo/redo,
  multi-cursor. New skill: integration testing across components you built separately,
  plus property tests like undo(do(x)) == x.

Order book first, though. It compounds directly into your interviews.
