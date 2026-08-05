# 19 — TxnKV — Worked Examples

A transaction is a DRAFT. begin() opens one; put/erase after it are written
in pencil. commit() accepts the draft; rollback() tears it up. Why it
exists: multi-step operations that must be all-or-nothing —
`begin(); take 50 from alice; give 50 to bob; commit()` — an error midway
means rollback, and the money was never half-moved.

## The mental picture: a stack of maps

```
base:       {x: 1}           committed truth, bottom
begin()     [{}, {x:1}]      push an empty draft
put(x, 2)   [{x:2}, {x:1}]   writes go to the TOP map only
get(x) → 2                   reads search top→bottom, first hit wins
rollback()  [{x:1}]          pop the draft, discard
get(x) → 1
```

erase writes a TOMBSTONE (⊘) into the top map: "deleted, as far as this
draft is concerned." A tombstone found during the top→down search means
"stop — answer is: not present."

Every numbered behavior in the README, as a trace you can run by hand:

## 1. Read-your-writes

```
put(x, 1)          base {x:1}
begin()
put(x, 99)
get(x) → 99        you see YOUR OWN draft, not the base
```
Wrong answer: 1. A store that hides your own uncommitted writes from you is
useless — you couldn't withdraw money you just deposited in the same txn.

## 2. rollback discards EXACTLY the innermost

```
put(x, 1)
begin()            txn A
put(x, 2)
begin()            txn B
put(x, 3)
get(x) → 3
rollback()         only B dies
get(x) → 2         A's draft is still alive   (wrong: 1 — rolled back too much)
rollback()
get(x) → 1
```

## 3. Nested commit merges into the PARENT, not the base — THE classic bug

```
begin()            A
put(x, 2)
begin()            B
put(y, 5)
commit()           B pours into A — y=5 is STILL provisional
get(y) → 5
rollback()         A dies, and takes y=5 with it
get(y) → nullopt   ← THE assertion
get(x) → nullopt
```
The buggy implementation commits B straight into the base store. Then A's
rollback can't reclaim y, and get(y) → 5 survives. This single trace is the
test that separates correct nesting from broken nesting.

## 4. erase is provisional too — both orders

```
put(x, 1)
begin()
erase(x) → true
get(x) → nullopt   deleted, in pencil
rollback()
get(x) → 1         the delete never happened
```
Second operation, other order:
```
put(x, 1)
begin()
erase(x) → true
put(x, 42)
get(x) → 42
rollback()
get(x) → 1         not 42, not missing — the ORIGINAL
```

## 5. ? commit/rollback with no open txn — you decide

```
// fresh store, begin() never called:
commit() → ???
```
Three defensible contracts — pick ONE, write it in the README, test it:
- throw std::logic_error   (loud — catches caller bugs at the scene)
- silent no-op             (quiet — and hides those same bugs)
- return bool              (caller decides — and can silently ignore it)
Same decision for rollback(). For reference, std::stack::pop() on empty is
UB — you can do better than the standard library did.

## 6. ? erase of a missing key — the sneaky one

```
// base: empty
begin()
erase(x) → false   nothing to erase... but did your impl RECORD anything?
put(x, 5)
get(x) → 5         ← MUST be 5
```
The bug this hunts: a per-layer design with a value-map PLUS a separate
deleted-set. erase(x) adds x to the deleted-set even while returning false;
put(x, 5) writes the value-map but forgets to clear the deleted-set; get
checks the deleted-set first → nullopt, though you just put it. The belief
"erase did nothing, so nothing to clean up" is exactly what makes the
cleanup easy to forget. A tombstone-in-the-map design
(map<K, optional<V>>, nullopt = tombstone) dodges this structurally: put
overwrites the tombstone in one write — one fact, one place (principle 3).
Whatever representation you pick: decide the behavior, and test this trace.

## 7. get is const — let the compiler stand guard

```cpp
std::optional<V> get(const K& key) const;    // ← this const
```
It promises get modifies nothing, and the compiler enforces the promise:
any accidental write inside a const method is a compile error.
The bug class it kills: a get() that "helpfully" caches its result into the
top layer (memoization). Now READS change what rollback discards, and your
oracle fuzz test fails mysteriously once in a thousand runs. const turns
that heisenbug into a red squiggle.

## How this connects to 17

remove_buyers rolls back by REPLAYING history (event log + fold). TxnKV
rolls back by DISCARDING drafts (layered state). Same goal — undo — two
representations. After building both, write the paragraph comparing them:
when is each one the right tool? (Hint: who has to see the history? how
expensive is replay? how deep does nesting go?)
