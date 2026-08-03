from Apply import TInt, TBool, TVar, TFun, all_types


def check_invalid(t1, t2):
    if t1 == TInt() and t2 == TBool():
        return True
    if t1 == TInt() and isinstance(t2, TFun):
        return True
    if t1 == TBool() and isinstance(t2, TFun):
        return True
    return False


def is_in(var: str, tree: all_types) -> bool:
    if isinstance(tree, TBool) or isinstance(tree, TInt):
        return False
    if isinstance(tree, TVar):
        return tree.value == var
    recursive = is_in(var, tree.arg)
    recursive2 = is_in(var, tree.res)
    return recursive or recursive2


def check_var(t1, t2) -> dict[str, all_types] | None:
    if isinstance(t1, TVar):
        if is_in(t1.value, t2):
            raise NotImplementedError("Broken. recursive definition")
        return {t1.value: t2}
    return None


def unify(t1: all_types, t2: all_types) -> dict[str, all_types]:
    if check_invalid(t1, t2) or check_invalid(t2, t1):
        raise NotImplementedError("This is not valid")
    if t1 == t2:
        return {}
    if check_var(t1, t2) is not None:
        return check_var(t1, t2)
    if check_var(t2, t1) is not None:
        return check_var(t2, t1)
    assert isinstance(t1, TFun) and isinstance(t2, TFun)
    lhs = unify(t1.arg, t2.arg)
    rhs = unify(t1.res, t2.res)
    for var, type in lhs.items():
        if var in rhs and type != rhs[var]:
            raise NotImplementedError("This is not valid")
    return lhs | rhs
