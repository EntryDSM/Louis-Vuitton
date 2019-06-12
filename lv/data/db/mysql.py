from aiomysql.sa import create_engine, Engine, SAConnection
from aiomysql.sa.result import ResultProxy


class MySQLClient:
    __engine: Engine = None
    __db_config: dict

    @classmethod
    async def init(cls, db_config: dict) -> None:
        cls.__db_config = db_config

        await cls._get_engine()

    @classmethod
    async def destroy(cls) -> None:
        if cls.__engine is not None:
            cls.__engine.close()
            await cls.__engine.wait_closed()

        cls.__engine = None

    @classmethod
    async def _get_engine(cls) -> Engine:
        if cls.__engine and cls.__engine._pool._closed: # pylint: disable=protected-access
            return cls.__engine

        cls.__engine = await create_engine(**cls.__db_config)

        return cls.__engine

    @classmethod
    async def execute(cls, query, **params) -> ResultProxy:
        engine: Engine = await cls._get_engine()
        conn: SAConnection
        res: ResultProxy

        async with engine.acquire() as conn:
            res = conn.execute(query(), **params)

        return res
