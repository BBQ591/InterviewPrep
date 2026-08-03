from regex import match


def test_literal():
    assert match("abc", "abc") is True
    assert match("abc", "ab") is False
    assert match("abc", "abcd") is False
    assert match("abc", "xbc") is False


def test_empty():
    assert match("", "") is True
    assert match("", "a") is False
    assert match("a", "") is False


def test_dot():
    assert match("a.c", "abc") is True
    assert match("a.c", "axc") is True
    assert match("a.c", "ac") is False
    assert match("...", "abc") is True
    assert match("...", "ab") is False


def test_star():
    assert match("ab*c", "ac") is True
    assert match("ab*c", "abc") is True
    assert match("ab*c", "abbbbc") is True
    assert match("ab*c", "abxc") is False


def test_dot_star():
    assert match(".*", "") is True
    assert match(".*", "anything at all") is True
    assert match("a.*z", "abcxyz") is True
    assert match("a.*z", "az") is True
    assert match("a.*z", "ab") is False


def test_alternation():
    assert match("a|b", "a") is True
    assert match("a|b", "b") is True
    assert match("a|b", "c") is False
    assert match("cat|dog", "dog") is True
    assert match("cat|dog", "cot") is False


def test_group():
    assert match("(ab)*", "") is True
    assert match("(ab)*", "abab") is True
    assert match("(ab)*", "aba") is False
    assert match("(a|b)c", "ac") is True
    assert match("(a|b)c", "bc") is True
    assert match("(a|b)c", "cc") is False


def test_combined():
    assert match("(a|b)*c", "c") is True
    assert match("(a|b)*c", "ababc") is True
    assert match("(a|b)*c", "aac") is True
    assert match("(a|b)*c", "abx") is False
    assert match("g(oo|a)*gle", "google") is True
    assert match("g(oo|a)*gle", "gaagle") is True


# ---- bonus (uncomment once you add + and ?) ----
# def test_plus_question():
#     assert match("ab+c", "abc") is True
#     assert match("ab+c", "ac") is False
#     assert match("ab?c", "abc") is True
#     assert match("ab?c", "ac") is True
#     assert match("ab?c", "abbc") is False


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
