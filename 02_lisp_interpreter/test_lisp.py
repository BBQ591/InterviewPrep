from lisp import run


def test_integer():
    assert run("42") == 42
    assert run("0") == 0


def test_arithmetic():
    assert run("(+ 1 2)") == 3
    assert run("(- 10 3)") == 7
    assert run("(* 2 3)") == 6
    assert run("(/ 6 2)") == 3


def test_variadic():
    assert run("(+ 1 2 3 4)") == 10
    assert run("(* 2 3 4)") == 24


def test_nesting():
    assert run("(+ 1 (* 2 3))") == 7
    assert run("(* (+ 1 1) (+ 2 3))") == 10


def test_comparison():
    assert run("(< 1 2)") is True
    assert run("(> 1 2)") is False
    assert run("(= 2 2)") is True
    assert run("(= 2 3)") is False


def test_if():
    assert run("(if (< 1 2) 10 20)") == 10
    assert run("(if (> 1 2) 10 20)") == 20


def test_define():
    assert run("(define x 5) x") == 5
    assert run("(define x 5) (+ x 1)") == 6
    assert run("(define a 3) (define b 4) (* a b)") == 12


def test_lambda():
    assert run("((lambda (x) (* x x)) 5)") == 25
    assert run("(define sq (lambda (x) (* x x))) (sq 6)") == 36
    assert run("(define add (lambda (a b) (+ a b))) (add 3 4)") == 7


def test_closure():
    # f closes over x defined in the outer scope
    assert run("(define x 10) (define f (lambda (y) (+ x y))) (f 5)") == 15
    # a function that returns a function (curried adder)
    prog = ("(define make-adder (lambda (n) (lambda (x) (+ x n)))) "
            "(define add5 (make-adder 5)) (add5 100)")
    assert run(prog) == 105


# ---- bonus (uncomment if you add function-define sugar) ----
# def test_define_sugar():
#     assert run("(define (sq x) (* x x)) (sq 9)") == 81


if __name__ == "__main__":
    import sys
    tests = {k: v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)}
    passed = 0
    for name, fn in tests.items():
        try:
            fn()
            print(f"  PASS  {name}")
            passed += 1
        except NotImplementedError:
            print(f"  TODO  {name}")
        except AssertionError as e:
            print(f"  FAIL  {name}: {e}")
        except Exception as e:
            print(f"  ERR   {name}: {type(e).__name__}: {e}")
    print(f"\n{passed}/{len(tests)} passed")
    sys.exit(0 if passed == len(tests) else 1)
