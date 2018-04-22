import asyncio

class Alist(list):
    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self)
        except StopIteration:
            raise StopAsyncIteration
        return value


class AsyncIter:
    def __init__(self, it):
        self._it = iter(it)
    async def __aiter__(self):
        return self
    async def __anext__(self):
        await asyncio.sleep(1)
        try:
            val = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return val