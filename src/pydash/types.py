import typing as t


if t.TYPE_CHECKING:
    from decimal import Decimal

IterateeObjT = t.Union[int, str, t.List, t.Tuple, t.Dict]
NumberT = t.Union[float, int, "Decimal"]
NumberNoDecimalT = t.Union[float, int]


_T_co = t.TypeVar("_T_co", covariant=True)
_T_contra = t.TypeVar("_T_contra", contravariant=True)


class SupportsDunderLT(t.Protocol[_T_contra]):
    def __lt__(self, __other: _T_contra) -> bool:
        ...


class SupportsDunderGT(t.Protocol[_T_contra]):
    def __gt__(self, __other: _T_contra) -> bool:
        ...


class SupportsDunderLE(t.Protocol[_T_contra]):
    def __le__(self, __other: _T_contra) -> bool:
        ...


class SupportsDunderGE(t.Protocol[_T_contra]):
    def __ge__(self, __other: _T_contra) -> bool:
        ...


SupportsComparison: t.TypeAlias = t.Union[
    SupportsDunderLE, SupportsDunderGE, SupportsDunderGT, SupportsDunderLT
]


class SupportsInt(t.Protocol):
    def __int__(self) -> int:
        ...


class Addable(t.Protocol[_T_contra, _T_co]):
    def __add__(self, x: _T_contra, /) -> _T_co:
        ...


class Subable(t.Protocol[_T_contra, _T_co]):
    def __sub__(self, x: _T_contra, /) -> _T_co:
        ...


class Multiplyable(t.Protocol[_T_contra, _T_co]):
    def __mul__(self, x: _T_contra, /) -> _T_co:
        ...


class SupportsRound(t.Protocol[_T_co]):
    def __round__(self) -> _T_co:
        ...
