from collections.abc import Collection, Iterable, Iterator, Mapping, MutableMapping, MutableSet
from typing import Any, Generic, NoReturn, Protocol, TypeVar, overload, type_check_only

from _typeshed import Incomplete
from typing_extensions import Self, TypeAlias

_K = TypeVar("_K")
_V = TypeVar("_V")
_Z = TypeVar("_Z")
_I = TypeVar("_I", covariant=True)

# Unfortunately, there's often check `if isinstance(var, (list, tuple))` in django
# codebase. So we need sometimes to declare exactly list or tuple.
_ListOrTuple: TypeAlias = list[_K] | tuple[_K, ...] | tuple[()]  # noqa: PYI047

@type_check_only
class _PropertyDescriptor(Generic[_K, _V]):
    """
    This helper property descriptor allows defining asynmetric getter/setters
    which mypy currently doesn't support with either:

        class HttpResponse:
            @property
            def content(...): ...
            @property.setter
            def content(...): ...

    or:

        class HttpResponse:
            def _get_content(...): ...
            def _set_content(...): ...
            content = property(_get_content, _set_content)
    """

    def __get__(self, instance: Any, owner: Any | None) -> _V: ...
    def __set__(self, instance: Any, value: _K) -> None: ...

@type_check_only
class _IndexableCollection(Protocol[_I], Collection[_I]):  # noqa: PYI046
    @overload
    def __getitem__(self, index: int) -> _I: ...
    @overload
    def __getitem__(self, index: slice) -> Self: ...

class OrderedSet(MutableSet[_K]):
    dict: dict[_K, None]
    def __init__(self, iterable: Iterable[_K] | None = ...) -> None: ...
    def __contains__(self, item: object) -> bool: ...
    def __iter__(self) -> Iterator[_K]: ...
    def __reversed__(self) -> Iterator[_K]: ...
    def __bool__(self) -> bool: ...
    def __len__(self) -> int: ...
    def add(self, item: _K) -> None: ...
    def remove(self, item: _K) -> None: ...
    def discard(self, item: _K) -> None: ...

class MultiValueDictKeyError(KeyError): ...

class MultiValueDict(dict[_K, _V]):
    @overload
    def __init__(self, key_to_list_mapping: Mapping[_K, list[_V] | None] = ...) -> None: ...
    @overload
    def __init__(self, key_to_list_mapping: Iterable[tuple[_K, list[_V]]] = ...) -> None: ...
    @overload
    def get(self, key: _K) -> _V | None: ...
    @overload
    def get(self, key: _K, default: _Z = ...) -> _V | _Z: ...
    def getlist(self, key: _K, default: _Z = ...) -> list[_V] | _Z: ...
    def setlist(self, key: _K, list_: list[_V]) -> None: ...
    @overload
    def setdefault(self: MultiValueDict[_K, _V | None], key: _K, default: None = None) -> _V | None: ...
    @overload
    def setdefault(self, key: _K, default: _V) -> _V: ...
    def setlistdefault(self, key: _K, default_list: list[_V] | None = ...) -> list[_V]: ...
    def appendlist(self, key: _K, value: _V) -> None: ...
    def items(self) -> Iterator[tuple[_K, _V | list[object]]]: ...  # type: ignore[override]
    def lists(self) -> Iterable[tuple[_K, list[_V]]]: ...
    def dict(self) -> dict[_K, _V | list[object]]: ...
    def copy(self) -> Self: ...
    def __getitem__(self, key: _K) -> _V | list[object]: ...  # type: ignore[override]
    def __setitem__(self, key: _K, value: _V) -> None: ...
    # These overrides are needed to convince mypy that this isn't an abstract class
    def __delitem__(self, item: _K) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[_K]: ...
    # Fake to make `values` work properly
    def values(self) -> Iterator[_V | list[object]]: ...  # type: ignore[override]
    def __copy__(self) -> Self: ...
    def __deepcopy__(self, memo: MutableMapping[int, Incomplete]) -> Self: ...

class ImmutableList(tuple[_V, ...]):
    warning: str
    def __new__(cls, *args: Any, warning: str = ..., **kwargs: Any) -> Self: ...
    def complain(self, *args: Any, **kwargs: Any) -> NoReturn: ...

@type_check_only
class _ItemCallable(Protocol[_V]):
    """Don't mess with arguments when assigning in class body in stub"""

    def __call__(self, value: _V, /) -> _V: ...

class DictWrapper(dict[str, _V]):
    func: _ItemCallable[_V]
    prefix: str
    @overload
    def __init__(self, data: Mapping[str, _V], func: _ItemCallable[_V], prefix: str) -> None: ...
    @overload
    def __init__(self, data: Iterable[tuple[str, _V]], func: _ItemCallable[_V], prefix: str) -> None: ...
    def __getitem__(self, key: str) -> _V: ...

class CaseInsensitiveMapping(Mapping[str, _V]):
    _store: dict[str, tuple[str, _V]]
    def __init__(self, data: Mapping[str, _V] | Iterable[tuple[str, _V]]) -> None: ...
    def __getitem__(self, key: str) -> _V: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[str]: ...
    def copy(self) -> Self: ...
