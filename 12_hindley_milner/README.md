# 12 — Hindley-Milner Type Inference

Build the type inference algorithm behind Haskell and ML: given an expression with
zero type annotations, either derive its most general (principal) type or prove it
has none. When this works, `\f -> \g -> \x -> f (g x)` comes back as
`(b -> c) -> (a -> b) -> a -> c` and you'll feel like a wizard.

Why this project, given your goals:

- **It's the "I understand Haskell now" project.** Every mysterious GHC error message
  and every `forall` becomes something you personally implemented.
- **Pure logic, top to bottom.** No IO, no randomness, no clock. Every function is
  `data -> data`, exactly-testable with `==`. The most test-friendly project on the menu.
- **A world-class oracle exists**: GHCi. Any type your engine infers can be checked
  against `:type` on the equivalent Haskell term. You never have to wonder if the
  expected value in a test is right.
- **Unification is a twofer** — it's also the engine of Prolog, so this unlocks
  mini-Prolog nearly for free.

## Ground rules (the standing ones, plus two project-specific)

1. Written test list before each milestone; open the spoiler only after.
2. Coverage never shrinks; every bug filed to the taxonomy in DESIGN_PRINCIPLES.md.
3. **Fresh type variables are your nondeterminism** (principle 6). Generate them from
   a counter you construct and pass in (or reset per inference) so runs are
   deterministic. If tests ever flake on variable names, the supply leaked.
4. **Assert types up to alpha-equivalence.** `a -> a` and `t3 -> t3` are the same
   type. Build `types_equal_up_to_renaming(t1, t2)` in Milestone 1 and use it in
   every assert — comparing raw variable names makes every test brittle to
   internals (that's asserting the representation, not the meaning).

Skip the parser: construct ASTs directly in tests (`App(Lam("x", Var("x")), Lit(1))`).
Parsing is a different project you've already done twice.

## The language (mini-ML)

Expressions: integer/bool literals, `Var`, `Lam(param, body)`, `App(fn, arg)`,
`If(cond, then, else)`, `Let(name, value, body)`. Types: `TInt`, `TBool`,
`TVar(name)`, `TFun(arg, result)`. Later: pairs, `LetRec`.

## Milestone 1 — Types, substitutions, and the equality helper

A substitution is a map from type variables to types; applying it rewrites a type.
Implement: `apply(subst, type)`, `compose(s2, s1)` (apply s1 first, then s2 — get
this order wrong and everything downstream is subtly broken), the alpha-equivalence
helper, and a pretty-printer that renames variables to `a, b, c...` for readable
failures.

<details><summary>Edge-case list (write yours first)</summary>

- apply on a type with no matching vars: unchanged
- apply is NOT recursive-until-fixpoint: `{a: b}` applied to `a` gives `b`, even if
  `b` is also in the map's domain — unless you compose properly. Decide the contract.
- compose order: `compose(s2, s1)` applied to `t` == `apply(s2, apply(s1, t))` —
  make this exact sentence a test; it is THE classic HM bug (category 3: direction)
- alpha-equivalence: `a -> b` vs `b -> a` are DIFFERENT; `a -> a` vs `b -> b` same;
  `a -> b` vs `c -> d` same
</details>

## Milestone 2 — Unification (the heart)

`unify(t1, t2) -> substitution` making both types equal, or a type error.

The contract is a one-line property — make it your first test:
**`s = unify(t1, t2)` implies `apply(s, t1) == apply(s, t2)`** (exact equality,
not alpha). Run it on every hand-written case, then on random type pairs.

<details><summary>Edge-case list (write yours first)</summary>

- unify(TInt, TInt) -> empty; unify(TInt, TBool) -> error
- unify(a, TInt) and the mirror unify(TInt, a) (category 2: test both orders!)
- unify(a, a) -> empty, NOT {a: a}
- unify(a, b) two different vars -> maps one to the other (either is fine — but
  your alpha-helper must accept both)
- **occurs check**: unify(a, a -> b) must ERROR, not loop. Feed it `\x -> x x`
  later and watch it fire. Skipping this = infinite types = the classic crash.
- function unification threads substitutions: unify arg types, APPLY the result
  to both result types, then unify those (forget the apply = category 5, stale state)
</details>

## Milestone 3 — Algorithm W, monomorphic core

Infer for: literals, `Var` (lookup or "unbound variable" error — decide that
contract), `Lam`, `App`, `If`. `Let(x, v, b)` for now types `v` and binds it
monomorphically. Every recursive call returns (subst, type); composing and applying
those correctly IS the algorithm.

<details><summary>Acceptance tests (these exact terms; check against GHCi)</summary>

- `\x -> x`            : a -> a
- `\x -> \y -> x`      : a -> b -> a           (K combinator)
- `\f -> \g -> \x -> f (g x)` : (b->c) -> (a->b) -> a -> c   (compose)
- `\f -> \x -> f x x`  : (a -> a -> b) -> a -> b
- `\x -> x x`          : occurs-check error
- `if` with mismatched branches: error; condition must be TBool
- `(\x -> x + 1) True` : error (if you add arithmetic; otherwise App mismatch)
- unbound variable: your decided error, tested
</details>

## Milestone 4 — Let-polymorphism (the famous part)

Type schemes (`forall a. a -> a`), `generalize` (quantify vars free in the type but
NOT free in the environment — that clause is the whole ballgame), `instantiate`
(fresh vars per use). This is what makes `let` different from lambda.

<details><summary>The boundary pair that defines this milestone</summary>

- `let id = \x -> x in (id 1, id True)` — TYPES. Each use of `id` instantiates fresh.
- `(\id -> (id 1, id True)) (\x -> x)` — FAILS. Lambda-bound variables are
  monomorphic; `id` can't be Int->Int and Bool->Bool at once.

Same shape as your FOK yes/no and maker-price pairs: two nearly identical programs,
opposite verdicts, and only the correct generalization rule passes both. Also test:
generalizing must NOT capture an env-bound variable — `\x -> let y = x in y` is
`a -> a`, not `a -> forall b. b` nonsense. Forgetting the "not free in env" clause
passes every simple test and fails exactly this one.
</details>

## Milestone 5 — LetRec, and errors worth reading

`LetRec` via a fresh variable for the function bound in its own body (the fix-point
trick): `let rec fact = \n -> if n then 1 else fact n` — infers without annotations.
Then spend one session making type errors *say something*: expected vs actual,
where. Testing error MESSAGES pins them as contracts (your category 6 made policy).

## Milestone 6 (stretch) — pick one

- Pairs + lists + polymorphic `map`/`fold` — watch `map : (a->b) -> [a] -> [b]` emerge.
- Constraint-generation style: walk the AST collecting equations, solve after.
  Same types out; compare engines against each other as mutual oracles.
- Reimplement the whole thing in Haskell. The types will hold your hand; feel the
  difference from Python.

## The oracle workflow

For every acceptance test, check the expected type in GHCi first:
`ghci> :type \f -> \g -> \x -> f (g x)`. Translate, assert up to alpha. When your
engine and GHC disagree, GHC is right — find out why, file the bug in the taxonomy.

## Bug forecast (from your own taxonomy)

- **Category 3 (direction):** substitution composition order. THE bug of this project.
- **Category 5 (second operation):** forgetting to apply the running substitution
  before the next unify — stale types, works on small terms, breaks on compose.
- **Category 1 (boundary):** occurs check; unify(a, a).
- **Category 6 (undecided contract):** unbound variables, error message shape.
- **Category 2 (mirror):** unify(x, y) vs unify(y, x) — test both orders always.
