# Decomposition Problems — the independence genre

Born in 17 (buyer marketplace): requests for different item names never
interact, so the global replay decomposes into per-name replays. Naming
that — "these are independent" — collapsed the problem.

The skill has three moves, and interviews test all three:

1. **Claim it.** Find the key under which the state factors
   (item_name, symbol, account, file path, column).
2. **Prove it.** Two ops with different keys must commute: swapping their
   order can't change any final state. The proof is usually "they touch
   disjoint data." If you can't say the disjointness out loud, you don't
   have independence.
3. **Survive its death.** The follow-up adds a shared resource (a budget,
   an all-or-nothing order, a transfer) and the factoring shatters.
   Strong candidates say WHICH assumption broke and fall back gracefully.

Every problem below has a part where the independence is real and a part
where it breaks. Sizes as usual: (S) one evening, (M) a weekend.

1. **21_wallet_marketplace** (S) — sequel to 17. A per-buyer budget couples
   item names; per-name replay dies. Killer test: a case where per-name and
   global replay disagree.
2. **22_basket_exchange** (S/M) — sequel to 20. N books keyed by symbol is
   embarrassingly parallel (say the proof); all-or-nothing basket orders
   couple symbols and you invent two-phase commit live.
3. **23_ledger_undo** (S/M) — void one event, replay only what could have
   changed. Transfers weld accounts into union-find components; the affected
   set is a component query.
4. **24_keyed_executor** (M) — the commutativity proof made executable:
   same-key in order, cross-key interleaves freely; a property test over
   random legal interleavings asserts identical final state. Then a two-key
   op breaks the scheduler.
5. **Three-way merge** — no new folder; it's 16_mini_git P5. Auto-merge is
   independence keyed by path; "conflict" is the name we give the coupling.
   Hidden kill: renames mean path isn't stable identity.
6. **25_substitutable_inventory** (S) — independence lives at a GRANULARITY:
   SKU-level false, class-level true only if classes are disjoint,
   component-level always. Finding the level is the design act.

## You've already met this pattern

- 17: replay decomposes by item_name (until wallets).
- 20: one book per symbol — the exchange is embarrassingly parallel
  (until baskets).
- Match3: gravity is per-COLUMN independent; matching couples columns —
  which is why reduce_moves was hard to test until the phases were cut apart.
- 03_spreadsheet: cells are independent unless an edge connects them;
  recompute = replay the affected subgraph in topo order. Problem 3 is this
  in disguise.
- git merge: independence by path. git rebase: replay. This whole genre is
  secretly git.

Line to append to DESIGN_PRINCIPLES.md when one of these bites you:
**"Independence is a theorem, not a vibe: name the key, say the
disjointness, then hunt for the shared resource that kills it."**
