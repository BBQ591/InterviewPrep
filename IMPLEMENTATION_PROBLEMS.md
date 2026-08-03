# Implementation Problems — the order-book/skip-list genre

Stateful structures with invariants, contracts, and rich boundaries. Standing rules:
written test list BEFORE code; coverage never shrinks; every bug filed into the
taxonomy in DESIGN_PRINCIPLES.md. Sizes: (S) one evening, (M) a weekend, (L) a week
of evenings.

## Tier 1 — do these next, in roughly this order

1. **LFU cache in O(1)** (M) — LRU's much harder sequel (user has LRU done).
   Every op O(1): key map + frequency-bucket lists (each bucket its own recency
   list) + a min-freq pointer. THREE structures that must agree — "facts stored
   twice" squared. Bug zones: second operation (get moves key between buckets;
   min-freq must follow), boundaries (capacity 1; tie at min freq -> LRU among
   them; freq bucket emptying), undecided contracts (put on existing key: does it
   bump freq?). Killer test: model-based — random ops vs a dumb O(n) oracle that
   recomputes evictions from full history; states must match after every op.
   Stretch sequel: **ARC** (adaptive replacement cache, the ZFS one) — four lists
   T1/T2/B1/B2 where two hold GHOSTS (evicted keys remembered without values) and
   a self-tuning balance parameter. Few people have ever built one; it shows.

2. **Rate limiter** (S/M) — token bucket, then sliding-window. The third
   nondeterminism source after randomness and ids: TIME. Inject the clock as a
   parameter (principle 6 — never call time.time() inside the logic).
   Bug zones: boundaries (request exactly at the limit; window edge), undecided
   contracts (burst at t=0? refill fractional tokens?). Killer test: fully
   deterministic — fake clock advances, assert allow/deny per tick. Everyone's
   interview list has this one.

3. **Position & P&L tracker with FIFO lots** (M) — feed of buys/sells; track
   realized/unrealized P&L per symbol with lot accounting. Lot-matching IS the
   matching loop from the order book wearing accounting clothes.
   Bug zones: boundaries (sell exactly one lot; sell across lots), second operation
   (flip long -> short in one fill), undecided contracts (short selling? zero-qty
   lots?). Killer test: conservation — sum of lot qtys == net position, always.
   The most trading-interview-relevant item on this list.

4. **Book builder from a market-data feed** (M) — reconstruct an L2 order book from
   add/modify/delete/trade messages, detect sequence gaps. Your order book, inverted:
   consume events instead of producing them. Real firms use this as a take-home.
   Bug zones: second operation (modify after delete; gap then late message),
   facts stored twice (book vs running best bid/ask cache). Killer test: golden
   files — message log in, book snapshots out (your Milestone 5 skill, reused).

5. **Transactional KV store** (L) — get/set/delete plus begin/commit/rollback,
   then nested transactions. The value-vs-identity conversation made executable:
   rollback = choosing between undo logs, copy-on-write, or layered dicts — a real
   representation decision with real tradeoffs.
   Bug zones: second operation everywhere (set same key twice in one txn; rollback
   after partial commit), undecided contracts (read-your-writes? commit inside
   nested?). Killer test: any committed state equals replaying the committed ops
   against a plain dict (fold-based oracle). Bridges into 13_kv_store persistence.

## Tier 2 — the bench

- **Ring buffer** (S) — wraparound off-by-ones; the full-vs-empty ambiguity is a
  classic undecided contract. Dense value per line of code.
- **Interval merge / interval map** (S/M) — boundary heaven: touching endpoints,
  containment, inclusive-vs-exclusive as an explicit contract decision.
- **Treap or AVL tree** (M) — rotations are mirror-bug purgatory (left/right =
  category 2). Property tests: BST invariant + balance/heap invariant + in-order
  equals sorted, vs a sorted-list oracle.
- **Union-Find** (S) — path compression + rank; property-test against naive
  connectivity. Small, satisfying.
- **Consistent hashing ring** (M) — wraparound boundaries; killer property: adding
  a node moves only ~1/N of keys (measure it, assert a bound).
- **Bloom filter** (S) — probabilistic contract: NO false negatives ever (hard
  assert), false-positive rate near theory (statistical assert with seeded input).
- **Event scheduler / timer wheel** (M) — priority queue + cancellation: your
  corpse/lazy-deletion pattern gets a second life.
- **Idempotent payment ledger** (M) — apply each transfer exactly once via
  idempotency keys; retries and duplicates are the whole point (category 5 as a
  product requirement).

## General menu — build-a-thing classics, by genre

### Emulators & machines
- **CHIP-8 emulator** (M) — the gateway emulator: ~35 opcodes, a display, a keypad;
  real games run on it. Public test ROMs = ready-made golden test suites.
  Stretch: Game Boy (L++).
- **Bytecode VM + compiler** (L) — stack machine, then compile a tiny language to it
  (Crafting Interpreters part II territory). Sequel to the lisp interpreter.
- **Forth interpreter** (S) — a whole language in an afternoon; the stack IS the
  semantics.

### Languages & logic (the Haskell-adjacent shelf)
- **Hindley-Milner type inference** (M/L) — unification + generalization for a mini-ML.
  The single best "I understand Haskell now" project that exists.
- **Mini-Prolog** (M) — unification + backtracking search; queries feel like magic.
- **Regex -> NFA -> DFA** (M) — sequel to 01_regex_engine: compile instead of
  interpret; property-test old engine vs new on random patterns (oracle reuse!).
- **Lambda calculus evaluator** (S) — Church encodings as the test suite.

### Systems (the CS439H shelf)
- **Unix shell** (M) — pipes, redirection, job control. fork/exec/dup2 for real.
- **Memory allocator** (M) — malloc/free with free lists + coalescing; test with
  randomized alloc/free sequences vs invariants (no overlap, all frees coalesce).
- **Write-yourself-a-git** (M/L) — init/hash-object/cat-file/commit/log, real .git
  format; verify against actual git as the oracle. Demystifies everything.
- **Redis clone** (M) — RESP protocol over sockets + your skip list for sorted sets.
  Two projects shake hands.
- **DNS resolver** (S/M) — raw UDP packets, byte-level parsing, recursion from root
  servers. Bit-boundary heaven.
- **Thread pool + work stealing** (M) — the concurrency bug taxonomy, live.

### Graphics & simulation
- **Ray tracer in a weekend** (M) — the classic; spheres, shadows, reflection.
  The output IS the test (plus: golden-image regression tests).
- **Software rasterizer** (M/L) — triangles, z-buffer, texture mapping; the other
  half of graphics.
- **Wolfenstein-style raycaster** (S/M) — 3D from a 2D grid in ~200 lines.
- **Game of Life -> Hashlife** (S then L) — trivial automaton, then the memoized
  quadtree version that runs generation 2^40. Absurd speedup, real algorithm.
- **Boids / falling-sand automata** (S) — emergence from three rules.
- **Verlet physics** (S/M) — cloth sim from position integration + constraints.

### Algorithms made tangible
- **Huffman + LZ77 compressor** (M) — build mini-zip; killer property test:
  decompress(compress(x)) == x on random bytes, forever.
- **Myers diff** (M) — the algorithm behind git diff; test against difflib as oracle.
- **Sudoku solver, Norvig-style** (S) — constraint propagation + search.
- **Poker hand evaluator + Monte Carlo equity** (S/M) — bitmask evaluation, seeded
  randomness (principle 6 again).
- **Micrograd-style autodiff + tiny neural net** (M) — backprop from scratch on
  scalar graphs; gradient-check against numerical derivatives as the oracle.
- **A* pathfinding on a grid** (S) — with a visualizer if feeling fancy; admissible
  heuristic as a tested contract.
- **Inverted index + BM25 search** (M) — a search engine over your own notes.

## From-scratch builds — decomposition is the boss fight

Chosen because the architecture is the hard part. Run each through the skeleton-first
protocol: stubs + contracts + edge list, reviewed BEFORE bodies.

- **Elevator simulator** (M) — E elevators, F floors, calls arrive as timed events;
  pluggable scheduling policy. Event queue + injected clock = fully deterministic
  sim, replayable and golden-testable. The decomp trap: mixing the simulation
  engine with the policy — cut them apart and policies become one-function plugins.
  A literal classic interview question, and the best rep-2 candidate on this list.
- **Digital logic sim -> CPU from NAND** (L, staged) — gates, wires, signal
  propagation; build NAND, then AND/OR/XOR, adder, flip-flop, register, ALU...
  until a program runs on hardware you "wired." nand2tetris energy; pairs with
  CS439H beautifully. Decomp IS the project — every chip is a stub with a contract,
  tested against its truth table. The purest contract-first practice that exists.
- **Assembler + toy CPU** (M) — two-pass assembler (labels, forward references)
  targeting a 16-instruction machine you also simulate. Natural sequel to the
  logic sim, or standalone. Golden tests: asm text in, memory trace out.
- **Scrabble engine** (M) — board with multipliers, rack, dictionary (trie),
  move validation + scoring; move GENERATION as the stretch. Scoring alone
  (cross-words, double-letter-under-new-tile-only rules) is an interview-sized
  decomp exercise with vicious boundary cases.
- **Card-game rules engine: Uno, then Dominion-lite** (M/L) — turn state machine,
  legal-move validation, then the boss: card EFFECTS that modify rules (skip,
  reverse, draw-2 stacking). Effects-as-data vs effects-as-code is a genuine
  architecture decision; get it wrong and card #20 forces a rewrite.
- **QR code generator** (M) — from "HELLO" to a scannable PNG: data encoding,
  Reed-Solomon error correction (real, learnable math), mask selection, quiet
  zones. Payoff is unbeatable: your phone reads your bytes. Oracle: any QR app.
- **SQL-subset engine over CSV** (L) — SELECT/WHERE/ORDER BY/LIMIT, then JOIN.
  Tokenizer -> parser -> planner -> executor: four layers, four contracts, and
  your third parser (this time the AST feeds an interpreter you also design).
  Oracle: sqlite3 on the same data.
- **Pool table physics** (M) — balls, cushions, friction, elastic collisions,
  fixed timestep. Decomp: integration / collision detection / resolution as
  separate testable stages. Property: momentum + energy conservation asserts.
- **WAV synthesizer** (S/M) — write raw WAV bytes; oscillators, envelopes, mixing;
  play a melody you computed. Bytes + math with an audible payoff; no libraries.
- **Sokoban + solver** (M) — the game is easy; the solver (BFS/A* with deadlock
  pruning) is the thinking. State-space design decides whether it's tractable.

## Already on the menu elsewhere

- Skip list (in flight) — tower first, property tests at model level, then fuse.
- 12_chess_moves / 13_kv_store / 14_editor — see 11_order_book/README.md.
- Match3 `to_remove` bug — still unfound. One evening. Close it out.
