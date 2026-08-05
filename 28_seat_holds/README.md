# 28 — Seat Holds — Specification (S/M, interview sim)

Protocol: parts in order; no reading ahead. Python + pytest. Every
public method takes `now` as a parameter; there is no background timer
anywhere in the system.

## System

A venue: rows of seats, each row with a price. A seat is free, held, or
booked. Some seats may already be booked when the system is constructed.

## Part 1 — hold / confirm

`hold(user, seat_ids, now) -> bool` — all-or-nothing: succeeds only if
every requested seat is free at `now`. A hold expires 300 seconds after
it is placed.
`confirm(user, now) -> list[seat]` — converts the user's unexpired holds
to booked seats.

## Part 2 — best available

`best_available(k, now) -> list[seat] | None` — k ADJACENT seats in the
cheapest row that has such a run available; ties → lowest row index,
then leftmost run.

## Part 3 — cancellation and the waitlist

Booking attempts that found no seats join a waitlist, in arrival order,
remembering their k and maximum price per seat.
`cancel_booking(user, now)` — frees that user's booked seats and serves
the waitlist in arrival order. Only bookings made through this system
can be cancelled; seats that were already booked at construction time
are never freed.

## Required behavior

- No seat is ever double-booked.
- A booked seat returns to free only via cancel_booking.

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
