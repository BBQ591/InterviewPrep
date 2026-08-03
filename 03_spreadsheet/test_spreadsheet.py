from spreadsheet import Spreadsheet


def test_literal():
    s = Spreadsheet()
    s.set_cell("A1", 5)
    assert s.get_value("A1") == 5


def test_unset_is_zero():
    s = Spreadsheet()
    assert s.get_value("Z9") == 0


def test_simple_reference():
    s = Spreadsheet()
    s.set_cell("A1", 5)
    s.set_cell("B1", "=A1 + 3")
    assert s.get_value("B1") == 8


def test_chain():
    s = Spreadsheet()
    s.set_cell("A1", 1)
    s.set_cell("B1", "=A1 + 1")
    s.set_cell("C1", "=B1 + 1")
    assert s.get_value("C1") == 3


def test_precedence():
    s = Spreadsheet()
    s.set_cell("A1", 2)
    s.set_cell("B1", 3)
    s.set_cell("C1", "=A1 * B1 + 1")
    assert s.get_value("C1") == 7


def test_parentheses():
    s = Spreadsheet()
    s.set_cell("A1", 2)
    s.set_cell("A2", 4)
    s.set_cell("B1", "=(A1 + A2) / 2")
    assert s.get_value("B1") == 3


def test_recompute_on_change():
    s = Spreadsheet()
    s.set_cell("A1", 5)
    s.set_cell("B1", "=A1 + 1")
    assert s.get_value("B1") == 6
    s.set_cell("A1", 10)
    assert s.get_value("B1") == 11


def test_multiple_refs():
    s = Spreadsheet()
    s.set_cell("A1", 10)
    s.set_cell("A2", 20)
    s.set_cell("A3", 30)
    s.set_cell("SUM", "=A1 + A2 + A3")
    assert s.get_value("SUM") == 60


def test_cycle_detection():
    s = Spreadsheet()
    s.set_cell("A1", "=B1")
    s.set_cell("B1", "=A1")
    try:
        s.get_value("A1")
        assert False, "expected a cycle to be detected"
    except ValueError:
        pass  # good — raised instead of infinite-looping


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
