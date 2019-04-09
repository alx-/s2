import aiohttp
import asyncio
from typing import Dict, Any, TypeVar, Coroutine
T = TypeVar("T")

timeout = aiohttp.ClientTimeout(total=60)


async def get(url: str, params: Dict[str, str]):
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, **params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None


def run(func: Coroutine[Any, None, T], loop: asyncio.AbstractEventLoop = None) -> T:
    loop = loop or asyncio.get_event_loop()
    return loop.run_until_complete(func)
