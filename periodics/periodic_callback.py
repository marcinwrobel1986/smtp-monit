import asyncio
import logging
from contextlib import suppress
from typing import Callable, Awaitable

logger = logging.getLogger('Periodic Callback')


class PeriodicCalllback:
    def __init__(self, interval: float, coro: Callable[..., Awaitable], *args, **kwargs):
        self.__coro = coro
        self.__args = args
        self.__kwargs = kwargs
        self.__interval = interval
        self.__started = False

        self.__running = False
        self.__loop = asyncio.get_event_loop()
        self.__task = None
        self.__handler = None

    def __repr__(self):
        return f"PeriodicCalllback({self.__interval}, {self.__coro})"

    def __str__(self):
        return f"PeriodicCalllback({self.__interval}, {self.__coro})"

    @property
    def interval(self):
        return self.__interval

    @property
    def started(self):
        return self.__started

    @property
    def running(self):
        return self.__running

    @property
    def coro(self):
        return self.__coro

    @property
    def args(self):
        return self.__args

    @property
    def kwargs(self):
        return self.__kwargs

    async def start(self, delay: float = None):
        if self.__started:
            return

        if delay is None:
            delay = self.__interval

        self.__started = True
        self.__running = False

        if delay is None:
            delay = self.__interval
        if delay == 0:
            self.__handler = self.__loop.call_soon(self.__run)
        else:
            self.__handler = self.__loop.call_later(delay, self.__run)

    async def stop(self, wait: float = 0):
        if not self.__started:
            return

        self.__started = False

        if self.__handler:
            self.__handler.cancel()
            self.__handler = None

        if self.__task is None:
            return

        if wait is False:
            wait = None

        with suppress(asyncio.TimeoutError, asyncio.CancelledError):
            await asyncio.wait_for(self.__task, wait)

        self.__task = None
        self.__running = False

    async def __runner(self):
        if not self.__started:
            return

        try:
            with suppress(asyncio.CancelledError):
                await self.__coro(*self.__args, **self.__kwargs)
        except:
            logger.exception('Got exception during awaiting periodically')
        finally:
            self.__running = False

    def __run(self):
        if not self.__started:
            return

        self.__handler = self.__loop.call_later(self.__interval, self.__run)

        if self.__running:
            logger.error('Throttling periodics call')
            return

        self.__running = True
        self.__task = asyncio.create_task(self.__runner())
