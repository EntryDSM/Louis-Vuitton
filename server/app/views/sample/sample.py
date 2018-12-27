from flask import request
from flask_restful import Resource


class Sample(Resource):
    def post(self):
        payload = request.json

        return payload, 201
