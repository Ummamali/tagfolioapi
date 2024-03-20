from flask import Blueprint, jsonify, request
from app.utils.database import add_document_to_collection, find_document
from http import HTTPStatus
from .routes import user_bp
from app.utils.misc import run_schema, send_email
from app.utils.hashing import hash_password
import random

req_obj_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "username": {
      "type": "string",
      "minLength": 3
    },
    "email": {
      "type": "string",
      "format": "email"
    },
    "password": {
      "type": "string",
      "minLength": 8,
      "pattern": "^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]+$"
    }
  },
  "required": ["username", "password", "email"]
}


@user_bp.route('/signup', methods=['POST'])
def signup():
  req_obj = request.json
  if run_schema(req_obj, req_obj_schema):
    verify = str(random.randint(100000, 999999))
    result = add_document_to_collection('unverified_users', {"verify": verify,'username': req_obj['username'],'email': req_obj['email'], 'password': hash_password(req_obj['password'])})
    send_email(req_obj['email'], 'Verify Your Registration', f'Verification Code: {verify}')
    return jsonify({'acknowledged': result.acknowledged})
  else:
    return jsonify({'msg': 'Invalid Schema!'}), HTTPStatus.BAD_REQUEST
  


# Now we verify the user 
  
req_obj_schema_verify = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "email": {
      "type": "string",
      "format": "email"
    },
    "verify": {
      "type": "string",
      "pattern": "^[0-9]{6}$"
    }
  },
  "required": ["email", "verify"]
}

@user_bp.route('/signup/verify', methods=['POST'])
def signup_verify():
  req_obj = request.json
  if run_schema(req_obj, req_obj_schema_verify):
    found = find_document('unverified_users', {**req_obj})
    if found is not None:
        del found['verify']
        add_document_to_collection('users', {**found})
    return jsonify({"acknowledged": True})
  else:
    return jsonify({'msg': 'Invalid Schema!'}), HTTPStatus.BAD_REQUEST