# 33 — Package Manager — Specification (M, interview sim)

Protocol: parts in order; no reading ahead. Python + pytest.

## Part 1 — install

`register(name, version, deps)` — adds a package version to the
repository index. deps is a list of (name, constraint); constraints are
exact ("1.2") or ranges (">=1.0,<2.0"). Versions are dotted numbers,
compared numerically per component.
`install(name, constraint) -> bool` — installs the highest registered
version satisfying the constraint, plus everything it transitively
needs, choosing the highest satisfying version at every step. At most
one version of a package is installed at a time; if the request cannot
be satisfied without conflicting with what is already installed, the
whole install fails and changes nothing.
`installed() -> dict[name, version]`

## Part 2 — uninstall and autoremove

Packages installed by direct request are "explicit"; packages that
arrived only as dependencies are not.
`uninstall(name) -> bool` — refuses if anything still installed depends
on it.
`autoremove() -> list[name]` — removes every non-explicit package that
no remaining package needs.

## Part 3 — upgrade

`upgrade(name) -> bool` — moves the package to the highest registered
version that all installed dependents can accept, adjusting its own
dependencies as needed. Succeeds completely or changes nothing.

Worked example: registry has A 1.0 (deps: B >=1.0), A 2.0
(deps: B >=2.0), B 1.0, B 1.5, B 2.0. install(A, ">=1.0") installs
A 2.0 and B 2.0. If C 1.0 (deps: B <2.0) were installed first,
install(A, ">=1.0") must instead pick A 1.0 with B 1.5 — or fail if
that's impossible. Decide which, and write it down.

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
