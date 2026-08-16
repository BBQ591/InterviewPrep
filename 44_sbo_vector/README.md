# 44 — Small-Buffer Vector — Specification (S/M)

Reported Jump intern question, verbatim: "a vector that stores its
elements on the stack when N < 10, but uses the heap for any exceeding
elements when N >= 10." Sequel to 18_mini_vector — build on that code.
C++. Also your ammunition for the HRT/IMC verbal chain ("how does
std::vector grow? what does push_back do? move semantics?") — after
this you answer from experience.

## Part 1 — SBO

Inline storage for the first 10 elements (aligned raw bytes, not
default-constructed T's); spill to the heap at 11. `push_back`, `pop_back`,
`operator[]`, `size`, `capacity`. Decide: does shrinking below 10 move
back inline? Defend the answer std::string gives.

## Part 2 — the special members

Copy ctor, move ctor, copy assign, move assign, dtor — correct across
all four state pairs (small↔small, small↔big, big↔small, big↔big).
Moving a SMALL vector cannot steal a pointer — elements must be moved
one by one, and the moved-from state must still be valid. Say why this
makes SBO move slower than plain vector move; that trade-off IS the
interview conversation.

## Part 3 — non-trivial T

Instantiate with std::string and with a type having no default ctor.
Placement new, explicit destructor calls, no memcpy of objects.
Exception safety of push_back during spill: decide your guarantee and
test it with a throwing type.

## Killer test

An instrumented element type counting constructions/destructions —
balance to exactly zero after every scenario, all four copy/move state
pairs covered.

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
