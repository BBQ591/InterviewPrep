# 48 — Intern OA Bench — timed assessment sims (HRT + Jump)

Reconstructed from candidate reports and OA walkthroughs (Aug 2026
research; per-item confidence noted — prep-site reconstructions are
plausible but not gospel). The OAs themselves:

- **HRT**: proctored CodeSignal GCA — 4 questions, 70 minutes, scored
  /600, ~500+ to advance. Questions rotate from CodeSignal's general
  bank, so train the FORMAT: strict 70-minute sittings, no pauses.
- **Jump**: Codility — 3 problems; the 2024 intern cycle REQUIRED
  C++. Do Set C in C++, no exceptions.

Protocol: one full set per sitting, clock running, no reading ahead
into a set before its sitting starts. Score yourself honestly: partial
credit only for passing tests.

## Set A — HRT GCA sim (70 min, reported 2025–26 cycle, medium conf.)

1. **Obstacle line.** Ops on an infinite number line: `[1, x]` builds
   an obstacle at x; `[2, x, size]` asks whether a block centered at x
   reaching size−1 each way touches no obstacle. Output '1'/'0' per
   query. (Sorted structure + bisect.)
2. **First day to target.** Array `visits`, int `target`: first index
   where the running sum reaches target, else −1.
3. **Smallest string via one reversal.** Reverse any prefix OR any
   suffix (one operation, any length): return the lexicographically
   smallest result. O(n²) passes.
4. **Bubble pop.** Colored grid; clicking a cell removes its
   DIAGONALLY-connected same-color group, then per-column gravity
   drops everything. Clicking empty = no-op. Return the final grid.
   (Your Match3 (10), with diagonal-only adjacency — reuse the shape.)

## Set B — HRT GCA sim (70 min, single walkthrough source, medium conf.)

1. **Dice score.** Three d6: all equal → 1000×value; exactly two equal
   (value x) → 500×x; all distinct → 100×min.
2. **Consonant cipher.** Shift each consonant k steps through the
   consonant sequence (vowels fixed, wrap z→b / Z→B, preserve case).
   "CodeSignal", k=3 → "CodeTignam".
3. **Maze with portals.** (0,0) → (n−1,m−1), rightward movement plus
   portal jumps; −1 if blocked, −2 if you loop, else steps.
4. **Max embeddable square.** Row of building heights: largest square
   area that fits. (Binary search the side, or sliding-window min.)

## Set C — Jump Codility sim (3 problems, do it in C++, 2020 report)

1. **Weeks between dates.** Two dates in a year → number of weeks
   between them. Statement survives only at this level — deciding
   inclusive/exclusive/partial-week contracts IS the exercise; state
   them in a comment, then implement.
2. **Pizza discounts.** Buy pizza choosing the cheapest of 4 discount
   types. The four mechanics are lost — design four plausible coupon
   types (e.g. flat-off, percent-off, second-pizza-half, bundle),
   write the contract, implement cheapest-choice. Contract-writing
   under a vague spec is the actual skill graded.
3. **Largest square from tiles.** M 1×1 tiles and N 2×2 tiles: side of
   the largest fully-filled square. (Candidate one-liner matches the
   known closed-form problem; derive, don't memorize: try x =
   floor(sqrt(4N+M)) and repair parity.)

## Extras bench (untimed drills; lower-trust sources, still worth reps)

- **Rolling 5-second max** over timestamped price ticks, O(n) total
  (monotonic deque). *HRT-flavored, prep-site claim.*
- **Max instantaneous load** from (start, end, value) events (sweep /
  difference array). *Same source.*
- **Time-priority match volume**: buys/sells arrive over time, equal
  prices match oldest-first; total matched volume. Your order book,
  OA-sized. *Same source.*
- **Add binary strings** (LC 67) then **hashmap with extended ops** —
  the one reported HRT intern-specific OA pairing (2024 cycle,
  login-walled source, low detail).
- Jump screen fragments: Nth Fibonacci, linked-list class, swap
  without temp, "read-only files from Unix permission strings",
  fixed-window rolling mean in O(1).

## Deliverables

One folder per set (`setA/`, `setB/`, `setC/`) with solutions + the
tests you wrote DURING the sitting. Note your time and score at the
top of each. A set is done when re-run green, not when the clock ends.
