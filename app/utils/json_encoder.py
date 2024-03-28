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
