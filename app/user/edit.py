# This file containes all the routes for Module 1 Use Case 03: Editing account information

from .routes import user_bp
from flask import jsonify, request
from app.utils.misc import run_schema, send_verification_email, is_valid_password
from app.utils.database import update_document
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from app.utils.database import find_document, update_document, delete_document
from app.utils.hashing import hash_password

# Editing Username
edit_username_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "newUsername": {
      "type": "string",
      "minLength": 3
    }
  },
  "required": ["newUsername"],
  "additionalProperties": False
}


@user_bp.route("/edit/username", methods=('POST',))
@jwt_required()
def edit_username():
	req_obj = request.json
	if run_schema(req_obj, edit_username_schema):
		user_id = get_jwt_identity()
		result = update_document('users', {"_id": ObjectId(user_id)}, {"username": req_obj['newUsername']})
		return jsonify(ack=result.modified_count == 1 or (result.matched_count==1 and result.modified_count==0))
	else:
		return jsonify({'msg': 'Invalid Schema!'}), HTTPStatus.BAD_REQUEST
	


@user_bp.route("/edit/password", methods=('POST',))
@jwt_required()
def edit_password():
	user_id = get_jwt_identity()
	if send_verification_email("RESET_PASSWORD", user_id, "/edit/password"):
		return jsonify(ack=True)
	return jsonify(ack=False)

# Verification of the reset password

change_password_verify_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "code": {
      "type": "string",
      "pattern": "^[0-9]{6}$"
    },
    "newPassword": {
      "type": "string",
      "minLength": 8,
    }
  },
  "required": ["code", "newPassword"]
}

@user_bp.route("/edit/password/verify", methods=('POST',))
@jwt_required()
def edit_password_verify():
	req_obj = request.json
	if run_schema(req_obj, change_password_verify_schema) and is_valid_password(req_obj['newPassword']):
		user_id = get_jwt_identity()
		user_doc = find_document('users', {"_id": ObjectId(user_id)})
		verify_query = {"_id": user_doc['_id'], "email": user_doc["email"], "route": "/edit/password"}
		verify_doc = find_document("verifications", verify_query)
		if verify_doc and verify_doc['code'] == req_obj['code']:
			result = update_document('users', {"_id": user_doc['_id']}, {"password": hash_password(req_obj['newPassword'])})
			delete_document('verifications', verify_query)
			return jsonify(ack=result.modified_count == 1 or (result.matched_count==1 and result.modified_count==0))
		else:
			return jsonify(msg='Unauthorized'), HTTPStatus.UNAUTHORIZED
	else:
		return jsonify({'msg': 'Invalid Schema or a bad Password!'}), HTTPStatus.BAD_REQUEST
	
