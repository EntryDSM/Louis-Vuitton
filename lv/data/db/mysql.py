from typing import Any, Dict, List

import aiomysql


class MySQLClient:
    __pool: aiomysql.Pool = None
    __db_config: dict

    @classmethod
    async def init(cls, db_config: dict):
        cls.__db_config = db_config

        await cls._get_pool()

    @classmethod
    async def _get_pool(cls) -> aiomysql.Pool:
        if cls.__pool and not cls.__pool._closed:  # pylint: disable=protected-access
            return cls.__pool

        cls.__pool = await aiomysql.create_pool(**cls.__db_config)

        return cls.__pool

    @classmethod
    async def destroy(cls) -> None:
        if cls.__pool is not None:
            cls.__pool.close()
            await cls.__pool.wait_closed()

        cls.__pool = None

    @classmethod
    async def execute(cls, query: str, *args) -> int:
        pool: aiomysql.Pool = await cls._get_pool()
        conn: aiomysql.Connection
        cur: aiomysql.DictCursor

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                influenced_row_cnt: int = await cur.execute(query, args)

        return influenced_row_cnt

    @classmethod
    async def fetchall(cls, query: str, *args) -> List[Dict[str, Any]]:
        pool: aiomysql.Pool = await cls._get_pool()
        conn: aiomysql.Connection
        cur: aiomysql.DictCursor

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args)
                result: List[Dict[str, Any]] = await cur.fetchall()

        return result

    @classmethod
    async def fetchone(cls, query: str, *args) -> Dict[str, Any]:
        pool: aiomysql.Pool = await cls._get_pool()
        conn: aiomysql.Connection
        cur: aiomysql.DictCursor

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args)
                result: Dict[str, Any] = await cur.fetchone()

        return result
