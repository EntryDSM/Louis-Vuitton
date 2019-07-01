import asyncio
from typing import Any, Dict, List
from functools import wraps

import aiohttp

from lv.exceptions.service import (
    ExternalServiceException,
    InterCallBadRequestException,
    InterCallNotFoundException,
)


def retry(retries=3, interval=3):
    def outer_function(original_function):
        @wraps(original_function)
        async def inner_function(*args, **kwargs):
            retry_count: int = 0

            while True:
                try:
                    res = await original_function(*args, **kwargs)
                except aiohttp.ClientResponseError as e:
                    if e.status == 400:
                        raise InterCallBadRequestException
                    if e.status == 404:
                        raise InterCallNotFoundException

                    retry_count += 1

                    if retry_count > retries:
                        raise ExternalServiceException

                    await asyncio.sleep(interval * retry_count)
                else:
                    return res
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
    @retry(retries=3)
    async def get(cls, url: str, **kwargs) -> Dict[str, Any]:
        session: aiohttp.ClientSession = await cls._get_session()

        async with session.get(
            url, params=kwargs, raise_for_status=True
        ) as resp:
            return await resp.json()

    @classmethod
    @retry(retries=3)
    async def get_list(cls, url: str, **kwargs) -> List[Dict[str, Any]]:
        session: aiohttp.ClientSession = await cls._get_session()

        async with session.get(
            url, params=kwargs, raise_for_status=True
        ) as resp:
            return await resp.json()

    @classmethod
    @retry(retries=3)
    async def patch(cls, url: str, json: Dict[str, Any]) -> None:
        session: aiohttp.ClientSession = await cls._get_session()

        await session.patch(url, json=json, raise_for_status=True)
