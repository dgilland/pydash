import typing as t


if t.TYPE_CHECKING:
    from decimal import Decimal


IterateeObjT = t.Union[int, str, t.List, t.Tuple, t.Dict]
NumberT = t.Union[float, int, "Decimal"]


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
