from typing import TYPE_CHECKING, Any, Awaitable, Callable, TypeVar

from returns.io import IOResult
from returns.result import Failure, Result, Success

if TYPE_CHECKING:
    from returns.future import Future, FutureResult  # noqa: F401


_ValueType = TypeVar('_ValueType', covariant=True)
_NewValueType = TypeVar('_NewValueType')
_ErrorType = TypeVar('_ErrorType', covariant=True)
_NewErrorType = TypeVar('_NewErrorType')


async def async_map(
    function: Callable[[_ValueType], _NewValueType],
    inner_value: Awaitable[Result[_ValueType, _ErrorType]],
) -> Result[_NewValueType, _ErrorType]:
    """Async maps a function over a value."""
    return (await inner_value).map(function)


async def async_bind(
    function: Callable[
        [_ValueType],
        'FutureResult[_NewValueType, _ErrorType]',
    ],
    inner_value: Awaitable[Result[_ValueType, _ErrorType]],
) -> Result[_NewValueType, _ErrorType]:
    """Async binds a container over a value."""
    container = await inner_value
    if isinstance(container, Result.success_type):
        return (await function(container.unwrap()))._inner_value
    return container  # type: ignore


async def async_bind_awaitable(
    function: Callable[[_ValueType], Awaitable[_NewValueType]],
    inner_value: Awaitable[Result[_ValueType, _ErrorType]],
) -> Result[_NewValueType, _ErrorType]:
    """Async binds a coroutine over a value."""
    container = await inner_value
    if isinstance(container, Result.success_type):
        return Result.from_success(await function(container.unwrap()))
    return container  # type: ignore


async def async_bind_async(
    function: Callable[
        [_ValueType],
        Awaitable['FutureResult[_NewValueType, _ErrorType]'],
    ],
    inner_value: Awaitable[Result[_ValueType, _ErrorType]],
) -> Result[_NewValueType, _ErrorType]:
    """Async binds a coroutine with container over a value."""
    container = await inner_value
    if isinstance(container, Result.success_type):
        return await (await function(container.unwrap()))._inner_value
    return container  # type: ignore


async def async_bind_result(
    function: Callable[[_ValueType], Result[_NewValueType, _ErrorType]],
    inner_value: Awaitable[Result[_ValueType, _ErrorType]],
) -> Result[_NewValueType, _ErrorType]:
    """Async binds a container returning ``Result`` over a value."""
    return (await inner_value).bind(function)


async def async_bind_ioresult(
    function: Callable[[_ValueType], IOResult[_NewValueType, _ErrorType]],
    inner_value: Awaitable[Result[_ValueType, _ErrorType]],
) -> Result[_NewValueType, _ErrorType]:
    """Async binds a container returning ``IOResult`` over a value."""
    container = await inner_value
    if isinstance(container, Result.success_type):
        return function(container.unwrap())._inner_value
    return container  # type: ignore


async def async_success(
    container: 'Future[_NewValueType]',
) -> Result[_NewValueType, Any]:
    """Async success unit factory."""
    return Success((await container)._inner_value)


async def async_failure(
    container: 'Future[_NewErrorType]',
) -> Result[Any, _NewErrorType]:
    """Async failure unit factory."""
    return Failure((await container)._inner_value)
