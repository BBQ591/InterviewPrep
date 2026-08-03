# Worked Examples — every concept, concrete

Notation: `Int`, `Bool`, type variables `a, b, t0, t1...`, functions `a -> b`
(right-associative: `a -> b -> c` is `a -> (b -> c)`). Every "gives" below is an
assert waiting to happen.

IMPORTANT — notation vs code: the arrow forms are shorthand for humans. In code,
every type is a TREE of dataclass values, never a string:

    a           means   TVar("a")
    Int -> b    means   TFun(TInt(), TVar("b"))
    a -> b -> a means   TFun(TVar("a"), TFun(TVar("b"), TVar("a")))

Strings appear in exactly two places: the name inside a TVar, and the keys of a
substitution dict. The string form "a -> b" exists only as your pretty-printer's
OUTPUT. So `apply({"a": TInt()}, a -> b) gives Int -> b` fully spelled out is:
`apply({"a": TInt()}, TFun(TVar("a"), TVar("b"))) == TFun(TInt(), TVar("b"))`.

## 1. Types as data

| Type          | Representation                          |
|---------------|-----------------------------------------|
| `Int`         | `TInt()`                                |
| `a`           | `TVar("a")`                             |
| `a -> Int`    | `TFun(TVar("a"), TInt())`               |
| `(a -> b) -> a` | `TFun(TFun(TVar("a"), TVar("b")), TVar("a"))` |

## 2. Substitution and apply

A substitution is a dict `{var_name: Type}`.

```
apply({"a": TInt()},            a)           gives  Int
apply({"a": TInt()},            a -> b)      gives  Int -> b
apply({"a": TInt()},            Bool)        gives  Bool          (untouched)
apply({},                       a -> a)      gives  a -> a        (empty subst)
apply({"a": b, "b": TInt()},    a)           gives  b             (ONE step —
                                                    apply is not iterate-to-fixpoint;
                                                    compose is what chains steps)
```

## 3. compose — the order-sensitive one (category 3 bug lives here)

Contract (make this sentence a test):
`apply(compose(s2, s1), t) == apply(s2, apply(s1, t))`  — s1 happens FIRST.

With `s1 = {a: b}` and `s2 = {b: Int}`:

```
compose(s2, s1) = {a: Int, b: Int}     applied to a  gives  Int   ✓ (b then Int)
compose(s1, s2) = {a: b,   b: Int}     applied to a  gives  b     ✗ different!
```

If your compose gives `b` where the walkthroughs below need `Int`, the arguments
are flipped. This one example distinguishes the two orders — pin it.

## 4. unify — inputs and exact outputs

```
unify(Int, Int)              gives  {}
unify(Int, Bool)             gives  TypeError
unify(a, Int)                gives  {a: Int}
unify(Int, a)                gives  {a: Int}        (mirror — test BOTH orders)
unify(a, a)                  gives  {}              (not {a: a})
unify(a, b)                  gives  {a: b}          (or {b: a} — both legal)
unify(a -> Int, Bool -> b)   gives  {a: Bool, b: Int}
unify(a, a -> b)             gives  OccursError     (infinite type)
unify(a -> a, Int -> Bool)   gives  TypeError       — and HERE is why unification
                                    threads substitutions:
                                    step 1: unify(a, Int) = {a: Int}
                                    step 2: APPLY it to the result sides first:
                                            apply({a:Int}, a) = Int  vs  Bool
                                    step 3: unify(Int, Bool) -> error.  Skip the
                                    apply and you'd unify(a, Bool) = {a: Bool},
                                    silently accepting a contradiction.
```

The universal property (first test of Milestone 2, then run it on random pairs):
`s = unify(t1, t2)` implies `apply(s, t1) == apply(s, t2)` exactly.

## 5. Expressions as data

```
\x -> x                Lam("x", Var("x"))
\x -> \y -> x          Lam("x", Lam("y", Var("x")))
f x                    App(Var("f"), Var("x"))
let id = \x -> x in id id
                       Let("id", Lam("x", Var("x")),
                                 App(Var("id"), Var("id")))
if b then 1 else 2     If(Var("b"), Lit(1), Lit(2))
```

## 6. Inference walkthroughs (Algorithm W by hand)

**`\x -> x`** — bind x to fresh `t0`; body `Var("x")` looks up `t0`;
result `t0 -> t0`. Pretty-printed: **`a -> a`**.

**`\x -> \y -> x`** (K) — x:`t0`, y:`t1`, body gives `t0`;
result `t0 -> t1 -> t0` = **`a -> b -> a`**.

**`\f -> \x -> f x`** — f:`t0`, x:`t1`. App rule for `f x`: make fresh `t2`,
`unify(t0, t1 -> t2)` gives `{t0: t1 -> t2}`, App's type is `t2`.
Result after substitution: `(t1 -> t2) -> t1 -> t2` = **`(a -> b) -> a -> b`**.

**`\f -> \g -> \x -> f (g x)`** (compose) — f:`t0`, g:`t1`, x:`t2`.
`g x`: fresh `t3`, `unify(t1, t2 -> t3)` → `{t1: t2 -> t3}`, type `t3`.
`f (g x)`: fresh `t4`, `unify(t0, t3 -> t4)` → `{t0: t3 -> t4}`, type `t4`.
Result: `(t3 -> t4) -> (t2 -> t3) -> t2 -> t4` = **`(b -> c) -> (a -> b) -> a -> c`**.
(If you got `(a -> b) -> (b -> c) -> ...` your composition order is flipped — see §3.)

**`\x -> x x`** — x:`t0`. App: fresh `t1`, `unify(t0, t0 -> t1)` → **OccursError**.
This is the occurs check earning its keep.

## 7. generalize / instantiate (Milestone 4)

`generalize(env, type)` quantifies vars free in the type but NOT free in the env:

```
generalize({},          a -> a)   gives  forall a. a -> a
generalize({"x": a},    a -> a)   gives  a -> a          (quantifies NOTHING —
                                          a is x's type; quantifying it would
                                          disconnect y's type from x's)
generalize({"f": a->b}, a -> c)   gives  forall c. a -> c   (only c is free)
```

`instantiate(scheme)` stamps fresh vars per USE:

```
instantiate(forall a. a -> a)   gives  t5 -> t5    (first call)
instantiate(forall a. a -> a)   gives  t6 -> t6    (second call — DIFFERENT vars;
                                        this independence IS polymorphism)
```

## 8. The defining pair, traced

**`let id = \x -> x in id id`** — TYPES.
`\x -> x` infers `t0 -> t0`; env is empty so generalize gives `forall t0. t0 -> t0`.
In the body each `id` instantiates fresh: first `t1 -> t1`, second `t2 -> t2`.
App: fresh `t3`, `unify(t1 -> t1, (t2 -> t2) -> t3)` → `{t1: t2 -> t2, t3: t2 -> t2}`.
Result **`a -> a`**. Two uses, two types, no conflict — that's let-polymorphism.

**`(\id -> id id)`** — FAILS.
Lambda binds id monomorphically to ONE `t0`. `id id` needs
`unify(t0, t0 -> t1)` → **OccursError**. Same body, no generalization, no mercy.

**`\x -> let y = x in y`** — the env-capture guard.
x:`t0`; infer `x` → `t0`; generalize under env containing x:`t0` → quantifies
nothing (t0 is free in env) → y:`t0` mono; body → `t0`. Result **`a -> a`**.
If your generalize ignores the env, y becomes `forall t0. t0` and this infers
nonsense — this is the test that catches the missing "not free in env" clause.

## GHCi oracle crib

```
ghci> :type \f -> \g -> \x -> f (g x)
ghci> :type let id = \x -> x in id id
ghci> :type \x -> x x        -- watch the real error message
```
