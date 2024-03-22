from functools import wraps
from flask import request, jsonify
from jsonschema import validate, ValidationError


def validate_schema(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not request.json:
                return jsonify({'error': 'Route requires JSON data, none provided!'}), 400
            try:
                validate(instance=request.json, schema=schema)
            except ValidationError as e:
                return jsonify({"message": "Invalid Schema!", 'error': e.message}), 400

            return func(*args, **kwargs)

        return wrapper
    return decorator
