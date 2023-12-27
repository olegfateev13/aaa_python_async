import abc
import asyncio
from typing import Coroutine, Set


class AbstractLongTaskCreator:
    @abc.abstractmethod
    def create_long_task(self) -> Coroutine:
        ...


class BackgroundCoroutinesWatcher:
    def __init__(self):
        self._running_tasks: Set[asyncio.Task] = set()

    def schedule_soon(self, coro: Coroutine):
        task = asyncio.create_task(coro)
        task.add_done_callback(self._remove_from_running_task)
        self._running_tasks.add(task)

    def _remove_from_running_task(self, task: asyncio.Task) -> None:
        self._running_tasks.remove(task)

    async def close(self):
        for task in self._running_tasks:
            task.cancel()
        self._running_tasks.clear()


class FastHandlerWithLongBackgroundTask:
    def __init__(self, long_task_creator: AbstractLongTaskCreator, bcw: BackgroundCoroutinesWatcher):
        self._long_task_creator = long_task_creator
        self._bcw = bcw

    async def handle_request(self) -> None:
        coro = self._long_task_creator.create_long_task()
        self._bcw.schedule_soon(coro)

    async def close(self) -> None:
        await self._bcw.close()
