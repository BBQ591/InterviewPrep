# Firm Interview Research — Aug 2026

Compiled from Glassdoor, Blind, LeetCode Discuss, 1point3acres, WSO,
Taro, Exponent, PracHub, firm blogs, and candidate GitHub repos.
Reddit was crawler-blocked everywhere; several Glassdoor/1p3a threads
are login-walled, so some items are snippet-level. Recurrence noted
inline. Folder numbers in [brackets] = where it's covered here.

## Jane Street — SWE

Format: 60-min phone screen, ONE problem grown by constraints added
every 10–15 min, any language, CoderPad. Onsite: 3–4 rounds × ~70 min,
often two interviewers, each round extends a single solution. No
math/brainteasers for SWE, no behavioral round. Scored on: per-op
complexity as constraints land, memory growth, edge cases, and
responsiveness to hints (explicitly scored).

- **Memoize → bounded FIFO cache → LRU O(1)** — their self-published
  canonical screen; highest recurrence. [36]
- **Connect Four → Connect-K → unbounded board → bottom push-up** —
  most-reported family 2024–2026, four variants. [37]
- **Code editor: brace matching → code folding (collapse/expand/render)**
  — 4+ independent listings 2023–2026, SWE + MLE screens. [38]
- **Tetris grown incrementally** — onsite; high recurrence. [06 done]
- **Sparse (ts, code, value) stream → dense matrix rows, watermark/
  max_lag disorder** — new-grad screen, single detailed report. [39]
- **Marketplace order matching + end-of-day reconciliation log
  (PAYMENT_FAILED / OK / OUT_OF_STOCK, billing adjustments)** — [17/21/30 genre]
- **Merkle tree with growing follow-ups** — onsite, medium recurrence.
- **Board game the interviewer describes (battleship, chess, invented)**
  — high recurrence as a genre; rules fidelity + decomposition. [06–10, 37, 45]
- **Stack machine interpreter with typed values; tokenized expression
  evaluation** — screen tier. [02/15 genre; 46#7]
- **Unit conversion graph (their official mock interview)** — [46#4]
- Onsite-tier misc: incremental PnL-table updates (hard, vague);
  circular buffer; interface-adapter; video player API; text-diff merge.

## HRT — SWE / Core / Algo Dev

Format: OA (CodeSignal ~4q/70min or Codility) → phone screens heavy on
C++/OS/networking fundamentals alongside coding → 2-hour onsite coding
block (parsing warm-up with edge cases; a data structure graded on
real-world efficiency; two algo problems) + rounds on optimization,
math, memory management. Experienced roles: timed take-home from a
spec; "take a spec, incorporate new facts iteratively" design round.

- **Board-game implementation (Reversi final-count-from-moves, 2048,
  Connect 4, calculator)** — most-repeated live genre, 3+ mentions. [45, 37, 07 done]
- **Trade-stream profit / replay events, answer state queries** — 2+
  reports; "spec → implement" house style. [40]
- **Stock exchange / order matching engine** (screen + OA) — strong
  recurrence. [11/20/22]
- **push()/randomPop() structure** [46#5]; **tree merge with ordered
  children** [46#8]; **pretty numbers base-4** [46#10]; poker hand
  simulator (single report).
- **C++ internals chains** (see drill list below) — the most
  consistently described HRT round of all.

## Jump Trading — SWE

Format: Codility/HackerRank OA (2–3 problems, 80–120 min, one usually
C++-flavored) → phone screen (coding + OS/arch/networking/UB probes,
"down to assembly") → 3-round coding onsite or superday. Recurring
spec-comprehension component: read a 3-page spec, find bugs in code
implementing it; comment/document unfamiliar code.

- **Order book from serialized message feed (A/X/T format, mid-price
  per message, book print every 10th, per-level traded volume,
  malformed input must not throw)** — real take-home, 3 independent
  appearances + a 2025 OA titled "Order Book Keeping in C++". [41]
- **malloc/free over a char array, two-part** — dated onsite report +
  2 aggregator entries. [43]
- **Small-buffer-optimized vector (stack < 10 elements, heap after)** [44]
- **Implement a hash map from scratch after C/pointer warmup** — [genre;
  see also IMPLEMENTATION_PROBLEMS.md]
- **Rate Limiter** (titled, 2026), **Symbol Tracker** — content unknown. [42]
- **Stack calculator** [46#7]; **merge two time series** [46#6]; **kth
  permutation** [46#9].
- Verbal: semaphore output prediction; implement a mutex; lazy
  singleton; loop order vs cache; virtual memory; move semantics.

## IMC — SWE

Format: HackerRank OA (2q, 90–120 min, C++/Java) → recorded video
round (design-out-loud, e.g. critique a hotel-booking design that uses
one huge list) → screens (sometimes mostly verbal: threading + data
structures) → final round.

- **Matching engine from skeleton code + ~20 pre-written unit tests:
  add order, cancel, price-time priority, partial fills, multi-level
  sweeps; follow-up O(1)-cancel via id lookup** — signature final
  round, reported 2021→2026 across offices. [11/20/22 — practice the
  make-the-tests-pass format]
- **Stack with inc(k, x) + sum(), all O(1)** — most-reported OA
  problem 2020–2026. [46#1]
- **Knight vs bishop BFS** — OA 2020–2022 unchanged. [46#2]
- **Bus-seat queue simulation** — OA 2024. [46#3]
- **Buried artifacts grid** — OA 2020–2021. [46#11]
- Onsite verbal cluster: false sharing (fix via cache-line padding),
  C++ memory model, move semantics, hash-table internals.
- Newer OAs trend trading-flavored ("calculate info from an order
  book" — knowing how one works helps).

## Voloridge — QD / SWE

Format: HR screen → online assessments (some third-party) → take-home
→ team interviews → 1–2 day onsite in Jupiter, FL. LeetCode
easy/medium tier, standard DS; code in your language of choice;
explicitly NOT brainteaser-driven. Stack: Python, C#, SQL (+ C++ on
the low-latency trading arm; FIX, microservices). Data-flavored:
SQL questions, pandas-style take-homes, "list vs hashmap under the
hood" — depth on YOUR resume more than puzzle depth.

- Existing Python sims [26–30] + 05 challenges cover the coding bar.
- Gap not worth a folder: a couple hours of SQL practice (joins,
  window functions) before their OA.

## C++ / systems verbal drill list (HRT, Jump, IMC)

Rehearse these as 2-minute spoken answers — they are asked verbatim:

1. std::vector internals: layout, push_back path, growth factor, why
   amortized O(1), what invalidates iterators. (→ 18/44 experience)
2. Move semantics: what the compiler generates, when moves happen,
   moved-from state; why SBO types can't steal pointers. (→ 44)
3. Virtual dispatch: vtable layout, object layout under multiple
   inheritance, cost of a virtual call; why virtual destructors.
4. Hash map internals: buckets, collision resolution choices, load
   factor, rehashing cost; unordered_map vs map trade-offs.
5. Two threads increment a shared counter 1M times each — why is the
   result < 2M; fixes (atomic, mutex) and their costs.
6. False sharing: what it is, why it wrecks a per-thread counter
   array, cache-line padding/alignment fix.
7. Loop order over a 2D array: row-major vs column-major traversal and
   the cache story; be able to estimate the difference.
8. Virtual memory: pages, TLB, page faults; what malloc does vs what
   mmap/sbrk do. (→ 43 experience)
9. Implement a mutex / how would a spinlock work; semaphore
   output-prediction puzzles.
10. Undefined behavior: three examples and why the compiler is allowed
    to do anything.

## Priority (as of Aug 2026, interviews pending)

Protect: 36 → 37 → 22 → 19 → 41.
Then: 40, 38, 26+28 timed, 42, 44.
Then: 39, 43, 45, 29, 21, warmups (46) interleaved as morning drills.
Deprioritized: 14, 15, 31–35 (34/35 as warmups only).
