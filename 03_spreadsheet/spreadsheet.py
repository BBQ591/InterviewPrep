"""Spreadsheet engine — see README.md.

Implement a Spreadsheet whose cells hold numbers or '='-prefixed formulas.
Formulas support cell refs (A1, B2), integers, + - * / with precedence, and parens.

Core ideas:
    - each cell is a pure function of the cells it references
    - recompute follows a dependency DAG
    - detect cycles instead of infinite-looping (raise ValueError)
"""


class Spreadsheet:
    def __init__(self):
        raise NotImplementedError

    def set_cell(self, name: str, contents) -> None:
        raise NotImplementedError

    def get_value(self, name: str):
        raise NotImplementedError
