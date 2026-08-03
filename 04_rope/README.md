# 04 — Rope (Immutable Text Buffer)

A **rope** is a balanced binary tree representing a string, giving O(log n) insert,
delete, and concat instead of O(n) on a flat string. Here the twist that makes it
an FP exercise: it is **immutable** — every operation returns a *new* rope and leaves
the original untouched. Because old versions stay valid (structural sharing), you get
**undo/redo for free**.

## Interface (`rope.py`)

```python
class Rope:
    @staticmethod
    def from_string(s: str) -> "Rope": ...

    def length(self) -> int: ...
    def char_at(self, i: int) -> str: ...          # 0-indexed
    def to_string(self) -> str: ...
    def concat(self, other: "Rope") -> "Rope": ...  # returns NEW rope
    def insert(self, i: int, s: str) -> "Rope": ...  # insert s BEFORE index i
    def delete(self, i: int, j: int) -> "Rope": ...  # remove chars in [i, j)
```

Every mutating-looking method (`concat`, `insert`, `delete`) must return a **new**
Rope and must **not** modify `self`. That immutability is the whole point.

## Suggested design

- A rope node is either a **leaf** (a string chunk) or an **internal** node with a
  left and right child plus a cached `weight` (the length of the left subtree — this
  is what makes `char_at` O(log n)).
- `concat(a, b)` = a new internal node with children `a` and `b`. O(1).
- `char_at(i)`: if `i < left.weight` go left, else go right with `i - left.weight`.
- `insert(i, s)` / `delete(i, j)`: `split` the rope at an index into (left, right),
  then `concat` the pieces back together. Implement `split` and you get both for free.
- Since nodes are never mutated, splits/concats **share** subtrees with the original
  — that's structural sharing, and it's why keeping every version is cheap.

Start simple (leaves can just be whole strings; don't worry about rebalancing at
first), get the tests green, then optimize.

## Bonus

Keep a list of past root ropes → `undo()` / `redo()` become trivial (just move a
pointer). Demonstrate that the old versions still read correctly.

## Run the tests

```bash
python test_rope.py       # or: pytest
```
