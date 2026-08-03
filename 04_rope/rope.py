"""Immutable Rope — see README.md.

A balanced tree over string chunks. Every operation returns a NEW Rope and never
mutates self (immutability + structural sharing => free undo).

Node = leaf(string)  OR  internal(left, right, weight=len(left)).
Implement `split(index) -> (left_rope, right_rope)` and insert/delete fall out of
split + concat.
"""


class Rope:
    @staticmethod
    def from_string(s: str) -> "Rope":
        raise NotImplementedError

    def length(self) -> int:
        raise NotImplementedError

    def char_at(self, i: int) -> str:
        raise NotImplementedError

    def to_string(self) -> str:
        raise NotImplementedError

    def concat(self, other: "Rope") -> "Rope":
        raise NotImplementedError

    def insert(self, i: int, s: str) -> "Rope":
        raise NotImplementedError

    def delete(self, i: int, j: int) -> "Rope":
        raise NotImplementedError
