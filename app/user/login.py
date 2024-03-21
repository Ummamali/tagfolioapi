from flask import Blueprint, jsonify, request, make_response
from app.utils.database import find_document
from app.utils.misc import run_schema
from app.utils.hashing import verify_password
from flask_jwt_extended import JWTManager, create_access_token
from http import HTTPStatus
from .routes import user_bp


req_obj_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email",  # Ensures it's a valid email format
        },
        "password": {
            "type": "string",
            "minLength": 8,  # Ensures the password is at least 8 characters long
        },
    },
    "required": ["email", "password"],  # Both fields are required
    "additionalProperties": False,  # Disallows any additional properties not specified in the schema
}

@user_bp.route('/login', methods=['POST'])
def login():
  req_obj = request.json
  if(run_schema(req_obj, req_obj_schema)):
    doc = find_document('users', {'email': req_obj['email']})
    if(doc is not None and verify_password(req_obj['password'], doc['password'])):
      access_token = create_access_token(identity=str(doc['_id']))
      return jsonify(access_token=access_token)
    else:
      return jsonify({'msg': 'Unauthorized'}), HTTPStatus.UNAUTHORIZED
  else:
    return jsonify({'msg': 'Invalid Schema!'}), HTTPStatus.BAD_REQUEST