from Apply import TInt, TBool, TVar, TFun, all_types
from Unify import unify
import pytest


def test_unify():
    fun1 = TFun(TFun(TVar("x"), TBool()), TInt())
    fun2 = TFun(TFun(TInt(), TVar("y")), TInt())
    assert unify(fun1, fun2) == {"x": TInt(), "y": TBool()}


def test_unify_throw():
    fun1 = TInt()
    fun2 = TBool()
    with pytest.raises(NotImplementedError, match="This is not valid"):
        unify(fun1, fun2)
