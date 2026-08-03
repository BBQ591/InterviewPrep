"""Regex engine — see README.md.

Implement `match(pattern, text) -> bool` (full-string match).
Supported: literals, '.', '*', '|', '(', ')'.  Bonus: '+', '?'.

Suggested functional design:
    parse(pattern) -> AST          # parser combinators; pure, no mutation
    compile(AST)   -> NFA          # Thompson construction
    simulate(NFA, text) -> bool    # BFS over a set of active states

Keep parsing and compilation pure (return new values, don't mutate inputs).
"""


def match(pattern: str, text: str) -> bool:
    pass
