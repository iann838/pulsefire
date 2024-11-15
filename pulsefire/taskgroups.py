"""Module for pulsefire task groups.

This module contains adaptations of `asyncio.taskgroups` better fit to use cases of pulsefire.
"""

from contextvars import Context
from typing import Awaitable, override
import asyncio
import logging
import traceback


LOGGER = logging.getLogger("pulsefire.taskgroups")


class TaskGroup(asyncio.TaskGroup):
    """Asynchronous context manager for managing groups of tasks.
    See [python asyncio task groups documentation](https://docs.python.org/3/library/asyncio-task.html#task-groups).

    Adapted for pulsefire, key differences from `asyncio.TaskGroup`:

    - Accepts a semaphore to restrict the amount of concurrent running coroutines.
    - Due to semaphore support, the `create_task` method is now async.
    - Allows internal collection of results and exceptions, similar to `asyncio.Task`.
    - If exception collection is on (default), the task group will not abort on task exceptions.

    Example:
    ```python
    async with TaskGroup(asyncio.Semaphore(100)) as tg:
        await tg.create_task(coro_func(...))
    results = tg.results()
    ```
    """

    semaphore: asyncio.Semaphore | None = None
    """Semaphore for restricting concurrent running coroutines."""
    collect_results: bool = True
    """Flag for collecting task results."""
    collect_exceptions: bool = True
    """Flag for collecting task exceptions, disables abort."""

    def __init__(
        self,
        semaphore: asyncio.Semaphore | None = None,
        *,
        collect_results: bool = True,
        collect_exceptions: bool = True,
    ) -> None:
        super().__init__()
        self.semaphore = semaphore
        self.collect_results = collect_results
        self.collect_exceptions = collect_exceptions
        self._exceptions: list[BaseException] = []
        self._results = []

    async def __aenter__(self):
        self._exceptions = []
        self._results = []
        return await super().__aenter__()

    def results[T](self) -> list[T]:
        """Return the collected results returned from created tasks."""
        if not self.collect_results:
            raise RuntimeError(f"TaskGroup {self!r} has `collect_results` off")
        return self._results

    def exceptions(self) -> list[BaseException]:
        """Return the collected exceptions raised from created tasks."""
        if not self.collect_exceptions:
            raise RuntimeError(f"TaskGroup {self!r} has `collect_exceptions` off")
        return self._exceptions

    @override
    async def create_task[T](self, coro: Awaitable[T], *, name: str | None = None, context: Context | None = None) -> asyncio.Task[T]:
        """Create a new task in this group and return it.

        If this group has a semaphore, wrap this semaphore on the coroutine.
        """
        _coro = coro
        if self.semaphore:
            await self.semaphore.acquire()
            async def semaphored():
                try:
                    return await _coro
                finally:
                    self.semaphore.release()
            coro = semaphored()
        return super().create_task(coro, name=name, context=context)

    def _on_task_done(self, task) -> None:
        if task.cancelled():
            return super()._on_task_done(task)
        if exc := task.exception():
            if self.collect_exceptions:
                LOGGER.warning(
                    "TaskGroup: unhandled exception\n" +
                    "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
                )
                self._exceptions.append(exc)
                self._tasks.discard(task)
                if self._on_completed_fut is not None and not self._tasks:
                    if not self._on_completed_fut.done():
                        self._on_completed_fut.set_result(True)
                return
        elif self.collect_results:
            self._results.append(task.result())
        return super()._on_task_done(task)
