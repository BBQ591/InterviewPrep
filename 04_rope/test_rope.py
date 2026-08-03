from rope import Rope


def test_roundtrip():
    assert Rope.from_string("hello").to_string() == "hello"
    assert Rope.from_string("").to_string() == ""


def test_length():
    assert Rope.from_string("hello").length() == 5
    assert Rope.from_string("").length() == 0


def test_char_at():
    r = Rope.from_string("abcde")
    assert r.char_at(0) == "a"
    assert r.char_at(2) == "c"
    assert r.char_at(4) == "e"


def test_concat():
    a = Rope.from_string("abc")
    b = Rope.from_string("def")
    assert a.concat(b).to_string() == "abcdef"
    assert a.concat(b).length() == 6


def test_concat_char_at():
    # char_at must work across the concat boundary (weights done right)
    r = Rope.from_string("abc").concat(Rope.from_string("def"))
    assert r.char_at(0) == "a"
    assert r.char_at(3) == "d"
    assert r.char_at(5) == "f"


def test_insert():
    r = Rope.from_string("abcd")
    assert r.insert(2, "XY").to_string() == "abXYcd"
    assert r.insert(0, "Z").to_string() == "Zabcd"
    assert r.insert(4, "Q").to_string() == "abcdQ"


def test_delete():
    r = Rope.from_string("abcdef")
    assert r.delete(1, 4).to_string() == "aef"   # remove b, c, d
    assert r.delete(0, 2).to_string() == "cdef"
    assert r.delete(4, 6).to_string() == "abcd"


def test_immutability():
    r = Rope.from_string("abc")
    r2 = r.insert(1, "X")
    # original must be untouched
    assert r.to_string() == "abc"
    assert r2.to_string() == "aXbc"

    r3 = r2.delete(0, 1)
    assert r2.to_string() == "aXbc"   # r2 still intact
    assert r3.to_string() == "Xbc"


def test_chained_edits_keep_history():
    v0 = Rope.from_string("cat")
    v1 = v0.insert(3, "s")        # "cats"
    v2 = v1.delete(0, 1)          # "ats"
    v3 = v2.insert(0, "b")        # "bats"
    # every past version still reads correctly (structural sharing)
    assert v0.to_string() == "cat"
    assert v1.to_string() == "cats"
    assert v2.to_string() == "ats"
    assert v3.to_string() == "bats"


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
