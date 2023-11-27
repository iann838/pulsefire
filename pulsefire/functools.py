"""Module for pulsefire function tools."""

from concurrent.futures import Executor
from typing import Any, Awaitable, Callable
import asyncio
import functools
import inspect


def async_to_sync(runner: Callable[[Awaitable[Any]], Any] = asyncio.run):
    """Convert a coroutine function to run synchronously. Use as decorator `@async_to_sync()`.

    Example:
    ```python
    @async_to_sync()
    async def sample_func(number: int):
        ...
    
    sample_func(0)
    ```

    Parameters:
        runner: A callable that runs the awaitable synchronously.

    Raises:
        TypeError: When `func` is not a coroutine function.
    """

    def decorator[**P, R](func: Callable[P, Awaitable[R]]) -> Callable[P, R]:
        if not inspect.iscoroutinefunction(func):
            raise TypeError(f"{func} is not a coroutine function")

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return runner(func(*args, **kwargs))

        return wrapper

    return decorator


def sync_to_async(executor: Executor | None = None):
    """Convert a function to run asynchronously. Use as decorator `@sync_to_async()`.

    Example:
    ```python
    @sync_to_async()
    def sample_func(number: int):
        ...

    async def main():
        await sample_func(0)
    ```

    Parameters:
        executor: Executor to be passed to `loop.run_in_executor`.
    """

    def decorator[**P, R](func: Callable[P, R]) -> Callable[P, Awaitable[R]]:

        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            new_func = functools.partial(func, *args, **kwargs)
            return await asyncio.get_event_loop().run_in_executor(executor, new_func)
        return wrapper

    return decorator
