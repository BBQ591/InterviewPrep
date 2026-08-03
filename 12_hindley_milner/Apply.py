from dataclasses import dataclass


@dataclass(frozen=True)
class TInt:
    pass


@dataclass(frozen=True)
class TBool:
    pass


@dataclass(frozen=True)
class TVar:
    value: str


@dataclass(frozen=True)
class TFun:
    arg: TInt | TBool | TVar | TFun
    res: TInt | TBool | TVar | TFun


all_types = TFun | TVar | TBool | TInt


def apply(susbt: dict[str, all_types], type: all_types) -> all_types:
    match type:
        case TFun():
            return TFun(apply(susbt, type.arg), apply(susbt, type.res))
        case TVar():
            return apply(susbt, susbt[type.value])
        case TBool():
            return type
        case TInt():
            return type
        case _:
            raise Exception("Not implemented")
