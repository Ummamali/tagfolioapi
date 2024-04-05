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

# This validator runs schema against the request


def validate_schema_multiple(schema_map):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get the schema corresponding to the current request method
            schema = schema_map.get(request.method)
            if not schema:
                # If no schema is provided for the current method, call the original function without validation
                return func(*args, **kwargs)

            # Check if request.json contains JSON data
            if not request.json:
                return jsonify({'error': 'Route requires JSON data, none provided!'}), 400

            try:
                # Validate the JSON data against the provided schema
                validate(instance=request.json, schema=schema)
            except ValidationError as e:
                # Return an error response if validation fails
                return jsonify({"message": f"Invalid Schema for {request.method}!", 'error': e.message}), 400

            # Call the original route handler function if validation passes
            return func(*args, **kwargs)

        return wrapper
    return decorator


def paginate(default_per_page=10, page_param='page', per_page_param='per_page'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract page and per_page query parameters from the request
            page = int(request.args.get(page_param, 1))
            per_page = int(request.args.get(per_page_param, default_per_page))

            # Call the original handler function with pagination parameters
            return func(page=page, per_page=per_page, *args, **kwargs)

        return wrapper
    return decorator
