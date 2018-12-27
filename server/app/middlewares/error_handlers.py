from flask import jsonify
from werkzeug.exceptions import HTTPException


def http_exception_handler(err: HTTPException):
    return jsonify({
        'description': err.description,
        'code': err.code
    })


def server_exception_handler(err: Exception):
    return jsonify({
        'description': str(err),
        'code': 500
    })
