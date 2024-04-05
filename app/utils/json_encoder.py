from datetime import datetime
from flask.json.provider import DefaultJSONProvider
from flask import Flask, jsonify
from bson import ObjectId
import json


def jsonify_customs(value):
    if isinstance(value, ObjectId):
        return str(value)
    raise TypeError(
        "Object of type %s with value of %s is not JSON serializable"
        % (type(value), repr(value))
    )


class CustomJSONProvider(DefaultJSONProvider):
    def __init__(self, app):
        super().__init__(app)

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(self, o)
