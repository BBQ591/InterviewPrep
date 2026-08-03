# Design Principles — paid for in bugs

The rule of this file: after every bug, append one line — which principle would have
prevented it? If none on the list would have, that's a NEW principle: write it down.
A principle you can't attach to a bug you personally hit isn't yours yet.

## Testing

1. **Expected values come from the domain rule, not from tracing your code.**
   The mental model that writes the bug also writes the assert that blesses it.
   *(bid/ask swap in 11; maker-price bug in 11 — twice)*
2. **A test's worth = how many wrong programs it rejects.**
   `!= old_state` rejects almost nothing. One order per side hides every ordering bug;
   square grids hide transpose bugs. Inputs need enough diversity that order matters.
   *(Match3 test_end_end; order book part 1)*
3. **Redundant state needs a cross-check after EVERY mutating operation.**
   Two copies of one truth will drift; the check must run wherever either copy changes.
   *(depth dicts stale after execute(); copy() cloning depth_sell into depth_buy)*
4. **Single-shot tests can't catch state-transition bugs. Write sequence tests.**
   Some bugs only exist between two operations, not inside one.
   *(is_new_order flag stale after the order rested)*
5. **If a test is hard to write, the design is wrong — fix the shape, not the test.**
   When every way to test a function feels bad, the function bundles too much.
   *(Match3 reduce_moves: detection + gravity + random refill in one body)*

## Design

6. **Functional core, imperative shell. Nondeterminism enters as data.**
   Random values, time, ids — produced at the edge, passed in as arguments.
   *(Match3 generate_el buried inside filter_fill_row)*
7. **Derive, don't store. Structure already knows most facts.**
   "Resting" = it's in the book. "Incoming" = it's the parameter. A stored flag must be
   maintained on every path forever; a derived fact can't go stale.
   *(is_new_order — predicted stale, went stale)*
8. **Parameters for facts the caller learns at runtime; separate functions for choices
   made while writing the code.** If every call site would pass a literal, it's two
   functions. If the discriminator arrives in the data, it's a parameter.
   *(resting= flag vs side= parameter)*
9. **Collapse branches that differ by a value, not a behavior.**
   A branch that is secretly min/max/sign/lookup should become that expression.
   A branch that doesn't exist can't be the untested one.
   *(three-way qty if/elif hiding a 5-field tuple in the equal case)*
10. **Make invalid states unrepresentable / unreachable through the public API.**
    If callers can build a crossed book, someone will. `_rest` is private for a reason.
11. **Named types at boundaries; positional tuples are swap bugs waiting.**
    `Trade(taker_id=, maker_id=, price=, qty=)` — the 5-tuple would have been a loud
    TypeError instead of a silent shape change.
12. **Duplication is cheaper than the wrong abstraction.**
    Keep mirror branches until tests are green, then unify only if they change together.
    *(BUY/SELL mirror in match)*
13. **One timeline → mutate; multiple timelines → values.**
    What-if, history, concurrent readers = you need values (or an event log + fold).
    *(deepcopy-per-match vs event sourcing)*
14. **Fix reported bugs before building features on top of them.**
    Known defects compound: every new layer built on a corrupt copy() tests garbage.
    *(copy() bug survived two reviews while matching got built on it)*
15. **Assert the post-state, not just the return value.**
    Wrong-heap pushes, buried orders, stale depths — all invisible if you only check
    what the function returned. *(three rest-path bugs shipped behind green trade asserts)*

## Bug taxonomy — where bugs cluster (the interview six)

File every new bug under one of these; a bug that fits none is category seven.
Interview ritual: after each function, a spoken 20-second scan down this list.

1. **Boundaries** — first/last/empty/exactly-equal/±1. *(end-of-row match; equal-qty
   5-tuple; FOK short-by-one)*
2. **Mirrors** — the copy you edited second. Diff the twins; test the second one first.
   *(wrong-heap push; `pice`; extra self; copy() depth clone — four bugs)*
3. **Signs & directions** — every negation and reversed sort gets one deliberate second.
   *(bid/ask swap; missing minus on the rest path)*
4. **Facts stored twice** — "where else does this fact live?" *(depth vs heaps, three times)*
5. **The second operation** — works once; what about again, or in the other order?
   *(stale is_new flag; corpse quotes; double-cancel)*
6. **Undecided contracts** — the "hm, what should this do?" flicker is a bug report
   from the future. Decide, test the decision. *(empty-book best_bid; unknown-id cancel)*
