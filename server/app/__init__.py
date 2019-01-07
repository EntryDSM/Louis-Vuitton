from flask import Flask
from werkzeug.exceptions import HTTPException


def register_extensions(flask_app: Flask):
    from app import extensions

    extensions.cors.init_app(flask_app)
    extensions.jwt.init_app(flask_app)
    extensions.validator.init_app(flask_app)

    extensions.swagger.init_app(flask_app)
    extensions.swagger.template = flask_app.config['SWAGGER_TEMPLATE']
    extensions.db.init_app(flask_app)


def register_views(flask_app: Flask):
    from app.views import route

    handle_exception_func = flask_app.handle_exception
    handle_user_exception_func = flask_app.handle_user_exception

    route(flask_app)

    flask_app.handle_exception = handle_exception_func
    flask_app.handle_user_exception = handle_user_exception_func


def register_middlewares(flask_app: Flask):
    from app.middlewares import error_handlers, request_hooks

    flask_app.register_error_handler(HTTPException, error_handlers.http_exception_handler)
    flask_app.register_error_handler(Exception, error_handlers.server_exception_handler)

    flask_app.after_request(request_hooks.after_request)


def create_app(*config_cls) -> Flask:
    flask_app = Flask(__name__)

    for config in config_cls:
        flask_app.config.from_object(config)

    register_extensions(flask_app)
    register_views(flask_app)
    register_middlewares(flask_app)

    return flask_app
