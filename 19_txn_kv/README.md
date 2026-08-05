# 19 — TxnKV&lt;K, V&gt; — Specification

Transactional key-value store with nested transactions — Tier-1 item 5 from
IMPLEMENTATION_PROBLEMS.md, materialized, in C++ so the templates count.
Same genre as 17: state + history + undo. 17 rolls back by replaying an
event log; this one rolls back by discarding state. Compare the two in a
written paragraph when both are done — that comparison is an interview
answer you'll reuse.

## Interface

```cpp
template <typename K, typename V>
class TxnKV {
  // get(const K&) -> std::optional<V>
  // put(K, V)
  // erase(const K&) -> bool
  // begin() / commit() / rollback()
  // depth() -> size_t        // open transaction count
};
```

Single-threaded, no I/O. Tests must instantiate BOTH
`TxnKV<std::string, int>` and `TxnKV<int, std::string>` — flushes out any
accidental K==string assumption.

## The representation decision (this is the problem)

Undo log per txn? Layered maps (a stack of
`unordered_map<K, std::optional<V>>`, nullopt = tombstone)? Full
copy-on-write snapshot on begin? Choose one, write down what get / commit /
rollback each cost under it, and why you picked it. The tests must not
care — they test the contract, and P5 proves it.

## Required behavior (contracts still to decide are marked ?)

1. Read-your-writes: a put inside a txn is visible to get inside that txn.
2. rollback discards exactly the innermost txn's effects.
3. commit at depth 1 applies to the base store. A nested commit merges into
   the PARENT txn — not the base. (The classic bug. Test: begin, put,
   begin, put, commit, rollback → both puts gone.)
4. erase inside a txn, then rollback → the key is back.
   erase-then-put-then-rollback → the original value. (Second operation,
   both orders.)
5. ? commit/rollback with no open txn: throw, no-op, or bool return — decide.
6. ? erase of a key that doesn't exist, inside a txn: returns false — but
   does it still shadow the key against outer layers? Decide, test.
7. get never mutates anything — mark it const and let the compiler enforce
   it.

## Killer tests

- Dumb oracle: an implementation that deep-copies the entire map on begin
  and swaps back on rollback. Obviously correct, gloriously inefficient.
  Seeded random op stream (put/erase/get/begin/commit/rollback at random
  depths) against both; every get result and the final base state must
  match.
- Fold oracle: the final committed state == replaying only the committed
  ops over a plain map (principle 13 again, from the other side).

## Phases

P1: flat store, no txns. P2: one-level begin/commit/rollback. P3: nested.
P4: the two oracles + fuzz. P5 (stretch): swap in the OTHER representation
behind the same tests — if any test has to change, the tests were testing
the implementation, not the contract.
