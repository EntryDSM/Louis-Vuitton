from flask import request
from flask_restful import Resource
from flasgger import swag_from

from app.docs.sample.sample import SAMPLE_POST


class Sample(Resource):
    @swag_from(SAMPLE_POST)
    def post(self):
        payload = request.json

        return payload, 201
