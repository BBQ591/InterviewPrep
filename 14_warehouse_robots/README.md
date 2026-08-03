# 14 — Warehouse Robot Fulfillment — Specification

## System

A warehouse is a W×H grid. Each cell is open floor, a shelf (impassable), or a
packing station. R robots move on the grid in the four cardinal directions, one
cell per T_move seconds. Time is simulated, measured in seconds from 0.

An order `(time, shelf, station)` appears at `time`: an item on that shelf must
be delivered to that packing station. A robot must reach a cell adjacent to the
shelf, pick the item (T_pick seconds), drive to the station, and drop it
(T_drop seconds). A robot carries at most one item.

## Input

- Config: W, H, R, T_move, T_pick, T_drop.
- Layout: the grid — shelf cells, station cells, robot starting cells.
- Workload: a list of orders `(time, shelf, station)`.

## Required behavior

1. Two robots may never occupy the same cell at the same time, and two robots
   may never swap cells in a single step.
2. Every finite workload must terminate with all orders delivered — no order
   may wait forever, and no group of robots may block each other forever.
3. **Reproducibility:** identical config + layout + workload must produce
   identical output, every run, byte for byte.

## Deliverables

1. `simulate(config, layout, workload, strategy) -> (event_log, metrics)`
   - `event_log`: a chronological record of everything that happened (order
     arrivals, assignments, picks, drops, robot moves) with timestamps.
   - `metrics`: per-order completion time (drop time − order time); per-robot
     distance traveled and idle time; aggregate average and maximum of each.
2. **At least two assignment strategies** (which robot takes which order),
   selectable without modifying the simulator, plus a comparison report: both
   strategies on the same workloads, metrics side by side.
3. A generator producing named scenarios (at minimum: a seeded uniform random
   layout + workload, and a "hot aisle" — most orders hitting one shelf row).
4. Tests. Their design is part of the work.

## Later phases (same spec, growing scope)

- P1: one robot, no shelves (empty grid), one strategy, event log correct.
- P2: shelves + pathfinding, metrics.
- P3: strategy interface + a second strategy + the comparison report.
- P4: R robots — the collision rules now bind.
- P5: battery capacity B — each move costs 1 unit; charging docks restore
  charge over time; a robot must reach a dock before running empty. Hot-aisle
  scenario in the report.

## Notes

- This spec is deliberately underspecified in several places. Finding those
  places, deciding them, and writing the decisions down is part of the work.
- Process gate (your protocol): skeleton — stubs, one-sentence contracts, call
  graph, edge list — reviewed before any bodies are written.
