# 13 — Elevator Simulator — Specification

## System

A building has F floors (1..F) and E elevators. Time is simulated, measured in
seconds from 0. An elevator moves at T_floor seconds per floor and, when it stops
to load or unload, its doors stay open for T_door seconds.

## Input

- Config: F, E, T_floor, T_door.
- Workload: a list of requests, each `(time, from_floor, to_floor)` — a passenger
  appears at `from_floor` at `time`, wanting to reach `to_floor`.

## Required behavior

1. Passengers wait at their floor until an elevator stops there with open doors,
   then board, ride, and exit at their destination.
2. The simulation runs until every passenger in the workload has been delivered,
   then reports results. Every finite workload must terminate with all passengers
   delivered — no request may wait forever.
3. **Reproducibility:** identical config + workload must produce identical output,
   every run, byte for byte.

## Deliverables

1. `simulate(config, workload, strategy) -> (event_log, metrics)`
   - `event_log`: a chronological record of everything that happened (arrivals,
     boardings, movements, deliveries) with timestamps.
   - `metrics`: per-passenger wait time (boarding time − request time) and travel
     time (exit time − boarding time); aggregate average and maximum of each;
     total floors traveled by all elevators.
2. **At least two dispatch strategies**, selectable without modifying the
   simulator, plus a comparison report: both strategies on the same workloads,
   metrics side by side.
3. A workload generator producing named scenarios (at minimum: uniform random
   with a seed, and a morning rush — most requests originating at floor 1).
4. Tests. Their design is part of the work.

## Later phases (same spec, growing scope)

- P1: one elevator, one simple strategy, event log correct.
- P2: metrics.
- P3: strategy interface + a second strategy + the comparison report.
- P4: E elevators.
- P5: elevator capacity C (a full car cannot take more passengers); rush-hour
  scenario in the report.

## Notes

- This spec is deliberately underspecified in several places. Finding those
  places, deciding them, and writing the decisions down is part of the work.
- Process gate (your protocol): skeleton — stubs, one-sentence contracts, call
  graph, edge list — reviewed before any bodies are written.
