from asyncio import Task
from typing import Callable, Coroutine, Any
import asyncio


async def await_my_func(f: Callable[..., Coroutine] | Task | Coroutine) -> Any:
    if isinstance(f, Callable):
        return await f()
    elif isinstance(f, Task):
        return await f
    elif isinstance(f, Coroutine):
        return await asyncio.create_task(f)
    else:
        raise ValueError('invalid argument')
