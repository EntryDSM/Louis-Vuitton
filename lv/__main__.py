import asyncio
import uvloop

from lv.app import create_app


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    app = create_app()

    app.run(
        host=app.config.APP_HOST,
        port=app.config.APP_PORT,
        debug=app.config.DEBUG,
        auto_reload=False,
    )
