import abc
import asyncio


class AbstractModel:
    @abc.abstractmethod
    async def compute(self):
        ...


class Handler:
    def __init__(self, model: AbstractModel):
        self._model = model

    async def handle_request(self) -> None:
        loop = asyncio.get_event_loop()
        task = loop.run_in_executor(None, self._model.compute)
        await task
