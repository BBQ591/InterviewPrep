# 32 — Access Control — Specification (M, interview sim)

Protocol: parts in order; no reading ahead. Python + pytest.

## Part 1 — direct grants

`grant(principal, resource, level)` — level is read, write, or owner;
owner implies write, write implies read.
`revoke(principal, resource)`
`check(user, resource, level) -> bool`

## Part 2 — groups

`add_member(group, principal)` / `remove_member(group, principal)` —
a principal is a user or another group; groups nest arbitrarily, and
nothing prevents membership loops. A grant to a group applies to every
user reachable through membership. `check` must answer correctly (and
finish) regardless of the membership structure.

## Part 3 — resource hierarchy and deny

Resources are paths (`/eng`, `/eng/repo-a/file.txt`); access granted on
a resource applies to everything beneath it.
`deny(principal, resource)` — an explicit block.
Precedence: an entry (grant or deny) on a nearer ancestor of the
resource beats an entry on a farther one; at the same resource, deny
beats grant.

Worked example: grant(eng-group, /eng, read); deny(bob, /eng/secrets);
bob is in eng-group → check(bob, /eng/README, read) is true,
check(bob, /eng/secrets/keys.txt, read) is false.

## Part 4 — explain

`explain(user, resource) -> ...` — the justification for what check
currently answers: which grant or deny decided it, and through which
membership chain. Design the return shape yourself.

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
