# 05 — FP Challenges (Haskell + Java)

16 problems where the imperative instinct is nested loops + mutable state, but the
elegant solution collapses into a functional primitive (fold / scan / map / group /
zip / catamorphism). Solve each **both ways** — Haskell to feel the pure version,
Java to translate it back.

## The rule that forces FP

- **Haskell:** it's pure by default — lean into `foldl'`, `scanl1`, `scanr1`, `map`,
  `filter`, `zipWith`, `groupBy`. No `IORef`, no mutation.
- **Java:** you *may* use loops, but try to write each as "an accumulator with an
  invariant" — no index off-by-ones, seed the accumulator once, don't mutate inputs.
  The goal is to make the fold/scan visible even in Java.

## Each folder has

- `SolutionN.hs`  — statement + stub + a tiny test `main`. Run: `runghc SolutionN.hs`
- `SolutionN.java` — statement + stub + a `main` with asserts. Run:
  `javac SolutionN.java && java SolutionN`

No hints in the files — struggle first. The table below names the hidden primitive
per problem, but resist reading the right-hand column until you've had a real go.

## Order (roughly easy → tricky)

| # | problem | hidden primitive |
|---|---------|------------------|
| 01 | Product Except Self | two scans (prefix × suffix), zipWith |
| 02 | Maximum Subarray | fold with a tuple accumulator (Kadane) |
| 03 | Trapping Rain Water | prefix-max & suffix-max scans, zip |
| 04 | Majority Element | fold (Boyer–Moore voting) |
| 05 | Valid Parentheses | fold with a stack (immutable list) accumulator |
| 06 | Daily Temperatures | fold building a monotonic stack |
| 07 | Subarray Sum = K | fold threading (prefix sum, count map, answer) |
| 08 | Group Anagrams | map-to-key then group |
| 09 | Merge Intervals | sort, then fold merging into the accumulator |
| 10 | Diameter of Binary Tree | tree fold (catamorphism) returning a tuple |
| 11 | Spiral Matrix | unfold: peel the top row, rotate the rest (`reverse . transpose`) |
| 12 | Sliding Window Maximum | two-list queue with cached maxima (banker's queue, amortized O(1)) |
| 13 | Hamming Numbers | laziness: self-referential infinite list, 3-way ordered merge |
| 14 | Highest Altitude | scanl: emit the running altitude at each step, then maximum |
| 15 | Buy and Sell Stock | running-min scan, zipWith (-), maximum |
| 16 | Partition Disjoint Intervals | prefix-max scan + suffix-min scan, zip, first agreeing index |

## Haskell setup

Just need GHC (`ghc`/`runghc`). Install via [ghcup](https://www.haskell.org/ghcup/):
`curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh`
Then `runghc Solution01.hs`. No cabal/stack project needed — these are single files.
