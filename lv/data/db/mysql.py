from aiomysql.sa import create_engine, Engine


class MySQLClient:
    __engine: Engine = None
    __db_config: dict = {}

    @classmethod
    async def init(cls, db_config: dict) -> None:
        cls.__engine = await create_engine(
            **db_config
        )

    @classmethod
    async def destroy(cls) -> None:
        if cls.__engine is not None:
            cls.__engine.close()
            await cls.__engine.wait_closed()

        cls.__engine = None

    @classmethod
    async def execute(cls):
        pass

    @classmethod
    async def execute_many(cls):
        pass

