# 27 — Leaderboard over an Event Store — Specification (S/M, interview sim)

Protocol: parts in order; no reading ahead. Python + pytest.

## Given

```python
class EventStore:
    def append(self, event) -> int: ...   # returns event_id; arrival order
    def get_all(self) -> list[Event]: ... # insertion order; append-only
```

Event: (event_id, player, points, ts). The Leaderboard is constructed
around an EventStore instance and may use only these two methods.

## Part 1 — totals and top-k

`record_score(player, points, ts)` — records via the store.
`top(k) -> [(player, total)]` — highest totals first.

## Part 2 — voiding

`void_event(event_id)` — a score is disqualified; all queries must
behave as if it never happened.
`void_player(player)` — same, for every event by that player.

## Part 3 — windowed queries

`top(k, since, until)` — only events with ts inside the window count.

## Part 4 — a second reader

A second Leaderboard instance is constructed over the SAME store
mid-life. It must give identical answers to the first. Events then keep
arriving through instance A while instance B serves reads; B's answers
must remain correct.

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
