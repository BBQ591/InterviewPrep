"""Mini-Lisp interpreter — see README.md.

Implement `run(source) -> value`: evaluate a program of one or more expressions,
returning the value of the last.

Suggested pipeline:
    tokenize(source) -> [tokens]
    parse(tokens)    -> nested-list AST
    eval(expr, env)  -> value      # pure recursive function
    apply(fn, args)  -> value

Special forms: if, define, lambda.
Builtins: + - * /  < > =
"""


def run(source: str):
    raise NotImplementedError
