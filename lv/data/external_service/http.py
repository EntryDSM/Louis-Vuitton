import asyncio
from typing import Any, Dict, List
from functools import wraps

import aiohttp

from lv.exceptions.data import (
    ExternalServiceDownException,
    InterCallBadRequestException,
    InterCallNotFoundException,
)

DEFAULT_RETRIES = 3
DEFAULT_RETRY_INTERVAL_SECOND = 3


def retry(retries=DEFAULT_RETRIES, interval=DEFAULT_RETRY_INTERVAL_SECOND):
    def outer_function(original_function):
        @wraps(original_function)
        async def inner_function(*args, **kwargs):
            for retry_count in range(retries):
                try:
                    res = await original_function(*args, **kwargs)
                except aiohttp.ClientResponseError as e:
                    if e.status == 400:
                        raise InterCallBadRequestException
                    if e.status == 404:
                        raise InterCallNotFoundException

                    await asyncio.sleep(interval * (retry_count + 1))
                else:
                    return res

            raise ExternalServiceDownException
        return inner_function
    return outer_function


class HTTPClient:
    __session: aiohttp.ClientSession = None

    @classmethod
    async def init(cls):
        await cls._get_session()

    @classmethod
    async def _get_session(cls) -> aiohttp.ClientSession:
        if cls.__session:
            return cls.__session

        timeout = aiohttp.ClientTimeout(total=10)
        conn = aiohttp.TCPConnector(limit=100)
        cls.__session = aiohttp.ClientSession(connector=conn, timeout=timeout)

        return cls.__session

    @classmethod
    async def destroy(cls) -> None:
        if cls.__session is not None:
            await cls.__session.close()

        cls.__session = None

    @classmethod
    @retry()
    async def get(cls, url: str, **kwargs) -> Dict[str, Any]:
        session: aiohttp.ClientSession = await cls._get_session()

        async with session.get(
            url, params=kwargs, raise_for_status=True
        ) as resp:
            return await resp.json()

    @classmethod
    @retry()
    async def get_list(cls, url: str, **kwargs) -> List[Dict[str, Any]]:
        session: aiohttp.ClientSession = await cls._get_session()

        async with session.get(
            url, params=kwargs, raise_for_status=True
        ) as resp:
            return await resp.json()

    @classmethod
    @retry()
    async def patch(cls, url: str, json: Dict[str, Any]) -> None:
        session: aiohttp.ClientSession = await cls._get_session()

        await session.patch(url, json=json, raise_for_status=True)
