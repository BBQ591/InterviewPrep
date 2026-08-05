# 24 — Keyed Executor — Specification (M)

The commutativity proof from this genre, made executable. Python. Simulated
concurrency — no threads; the interleaving choice is the injected
randomness (principle 6: the seed is a parameter).

## System

Ops arrive as a sequence of `(key, op)` where op mutates a per-key state
(keep it simple: counters with add/mul, or strings with append — something
where ORDER shows). Constraint: ops with the same key apply in arrival
order; ops with different keys may interleave arbitrarily.

Build the scheduler: per-key queues; at each step a seeded RNG picks any
queue whose head is runnable and runs it.

## The deliverable is the test

Run the SAME op set under many different seeds (many legal interleavings);
assert the final state is byte-identical every time. That property IS the
commutativity theorem, checked by machine.

Negative control (required): write a deliberately broken scheduler that
violates same-key ordering, and watch the property fail. A test you've
never seen fail proves nothing (principle 2).

## The kill — multi-key ops

Add `swap(key_a, key_b)`. Per-key queues now misorder or stall unless you
redesign: an op holds ALL its keys and is runnable only when it is the head
of EVERY one of its queues.

Then the question you must answer in writing: can two multi-key ops
deadlock — op1(a,b) waiting on op2(b,a)? Work out why arrival order saves
you (or construct the case where it doesn't). This is the argument, not
the code, and it's the part an interviewer would push on.

## Phases

P1: single-key scheduler + the interleaving property test.
P2: the negative control.
P3: multi-key ops; property still holds across seeds.
P4: the deadlock argument, written down, with the test that backs it.

## Why this problem exists

Kafka partitions by key so same-key events stay ordered while partitions
scale independently; cross-partition transactions are exactly the multi-key
op, and exactly as painful. The marketplace per-name replay, the
book-per-symbol exchange, and this scheduler are the same theorem wearing
three costumes.
