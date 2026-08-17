# 42 — Rate Limiter — Specification (S, interview sim)

On every firm's list (tier-1 item 2 in IMPLEMENTATION_PROBLEMS.md); a
titled Jump question from 2025–2026 reports. Protocol: parts in order;
no reading ahead. Python + pytest. The clock is ALWAYS a parameter —
`now` is a float in seconds, passed into every call; never call
time.time() inside the logic.

## What a rate limiter is — no outside knowledge needed

A service gets hit with requests. To protect itself it enforces a rate:
each incoming request is either allowed or rejected, decided at the
moment it arrives. You are building the decision box:

    allow(now) -> bool      # True = let it through, False = reject

A DENIED request consumes nothing, in every part below — being told
"no" must not make the next answer worse.

## Part 1 — token bucket

The bucket metaphor, which is the actual algorithm: a bucket holds at
most `capacity` tokens. Every ALLOWED request spends exactly 1 token.
Tokens drip back in continuously at `rate` per second (so after `dt`
seconds, `dt * rate` tokens returned, capped at capacity). A request is
allowed iff at least 1 whole token is available at `now`.

`TokenBucket(capacity, rate)` ; `allow(now) -> bool`.

Worked trace — capacity=2, rate=0.5 tokens/sec, bucket starts full:

    allow(0.0)  -> True    # spend: 2 -> 1
    allow(0.0)  -> True    # spend: 1 -> 0
    allow(0.0)  -> False   # empty; denial consumes nothing
    allow(1.0)  -> False   # refilled 0.5 tokens; 0.5 < 1
    allow(2.0)  -> True    # refilled to 1.0; spend -> 0
    allow(99.0) -> True    # long idle refills to capacity 2, not beyond

That trace is your first test, verbatim.

Contracts you decide and test (deliberately open): does the bucket
start full or empty; do fractional tokens accumulate (0.5 above) or
only whole ones — the trace above is consistent with either; what
happens if `now` is earlier than a previous `now` (error? clamp?).

## Part 2 — sliding window log

A different, EXACT policy (token bucket smooths; this one counts): at
most `n` allowed requests in ANY trailing window of `window` seconds.
Keep a log of the timestamps of allowed requests; on each call, drop
entries older than the window, then compare the count to `n`.

`SlidingWindow(n, window)` ; `allow(now) -> bool`.

Worked trace — n=3, window=10:

    allow(1)     -> True    # log [1]
    allow(2)     -> True    # log [1, 2]
    allow(3)     -> True    # log [1, 2, 3]
    allow(4)     -> False   # 3 allowed in the last 10s; log unchanged
    allow(11.5)  -> True    # the t=1 entry aged out; log [2, 3, 11.5]

Memory must not grow past O(n) — prune as you go.

Contract you decide and test: the window edge. At `allow(11)`, is the
t=1 entry inside the trailing window or just outside? Half-open
`(now - window, now]` vs closed `[now - window, now]` give different
answers — pick one, write it down, test exactly this case.

## Part 3 — per-key

Real limiters are per-user/per-IP: `allow(key, now) -> bool`, each key
enforced independently (its own bucket or window — build on whichever
part you prefer). One object, many keys, one shared config:

    limiter = KeyedLimiter(capacity=2, rate=0.5)
    limiter.allow("alice", 0.0)  # True  — alice's bucket: 2 -> 1
    limiter.allow("alice", 0.0)  # True  — 1 -> 0
    limiter.allow("alice", 0.0)  # False — alice empty...
    limiter.allow("bob",   0.0)  # True  — ...bob's own bucket is full

Keys are never registered up front: a key seen for the first time
behaves as if it always had a full, untouched limiter — create real
state lazily.

The problem inside the problem: millions of keys that went quiet must
not leak memory forever. When is a key's stored state indistinguishable
from having no state at all? That's the moment it can be deleted — say
when that is for your chosen algorithm, decide how deletion happens
(lazily on touch? a sweep?), and test that idle keys actually die.

## Part 4 — composition

Per-key limit AND a global limit at once: a request passes only if BOTH
allow it, and it must consume from both or from neither — no partial
spend. The naive sequence (spend key token, then ask global, get
denied) leaves the key token gone on a rejected request; that's the
planted bug.

Test that catches it: global bucket has 1 token, alice's bucket is
empty. `allow("alice", now)` -> False — and then `allow("bob", now)`
must still find the global token there.

This is the independence-death move of this problem: per-key state no
longer suffices; name which assumption broke.

## Deliverables

Implementation + tests. Test design is part of the work — fake clock
advancing, allow/deny asserted per tick, fully deterministic; for
Part 2 a brute-force oracle (count timestamps in window from the full
history) makes a good property test. Deliberately underspecified in
places — finding the ambiguities and deciding those contracts is part
of the work.
