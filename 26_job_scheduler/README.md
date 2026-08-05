# 26 — Job Scheduler — Specification (S/M, interview sim)

Protocol: do the parts in order; don't read Part N+1 until Part N is
green. Python + pytest. The clock is always a parameter — never call
time.time() inside the logic.

## Part 1 — submit / run_next

`submit(job_id, priority, run_at)`
`run_next(now) -> job_id | None` — runs the highest-priority job whose
`run_at <= now`. Ties: earlier run_at first, then submission order.

## Part 2 — cancel / reschedule

`cancel(job_id) -> bool`
`reschedule(job_id, new_run_at) -> bool`

## Part 3 — recurring jobs

`submit_recurring(job_id, priority, first_run, every)` — running an
instance schedules the next one. `cancel(job_id)` on a recurring job
cancels the whole series.

## Part 4 — leases

`run_next(now)` no longer completes a job — it leases it until now + 30.
`ack(job_id, now)` completes it. A job whose lease expired without an
ack must run again. The same job must never be held under two leases at
once.

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
