import re
import jsonschema


def run_schema(instance, schema):
    try:
        jsonschema.validate(instance=instance, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        return False

