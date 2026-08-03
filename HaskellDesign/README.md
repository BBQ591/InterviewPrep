# Haskell Design Drills

Not syntax drills — those live in `Q/`. These retune the *modeling* instinct:
state as values, change as functions, errors as data, logs as return values.
The point is to carry the instinct back into C++, where it becomes
`const&` in / value out.

## Files (do them in order)

1. `01_pure_updates.hs` — records, pure state transitions, event logs.
   Contains the exact helper we discussed for `Elevator::get_next`.
2. `02_adts_errors.hs` — an expression ADT: eval, render, simplify.
   `Either` instead of exceptions; spec decisions you must make yourself.
3. `03_elevator_kata.hs` — the capstone: your elevator P1 as a pure
   function `tick :: World -> (World, [Event])`. No mutation exists.
   Checks are *properties* (everyone delivered, boards before delivery,
   unit moves), so the detailed semantics are yours to decide — just like
   the C++ version.

## How to run

```bash
runghc 01_pure_updates.hs     # prints PASS / FAIL / TODO per check
# or interactively:
ghci 01_pure_updates.hs       # then :main, or poke functions directly
```

Every function starts as `todo`. Replace bodies until everything is PASS.

## The dictionary (Haskell habit → C++ spelling)

| Haskell | C++ |
|---|---|
| `filter p xs` | `std::erase_if(v, notP)` / `std::copy_if` |
| `map f xs` | `std::transform` |
| `foldl' step z xs` | `std::accumulate` / loop with an accumulator |
| `partition p xs` | `std::stable_partition` |
| `r { field = v }` | copy the struct, set the field, return it |
| `Maybe a` | `std::optional<A>` |
| `Either String a` | error-or-value return (`std::expected` in C++23) |
| pure function | `const&` parameters, result by return value, `const` method |

## The one rule (same as Preperation/)

Functional core, imperative shell: `main` may print; nothing else may
do anything but compute.
