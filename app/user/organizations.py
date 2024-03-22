# This file contains all the routes for Use Case 4: Managing Organizations

from .routes import user_bp
from app.utils.middlewares import validate_schema, validate_schema_multiple
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from app.utils.database import find_document, add_document_to_collection
from http import HTTPStatus

organization_schema = {
	'POST': {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "minLength": 5
    }
  },
  "required": ["name"],
  "additionalProperties": False
}
}


# Frs Organization
@user_bp.route('/organization', methods=['POST'])
@jwt_required()
@validate_schema_multiple(organization_schema)
def organization():
	req_obj = request.json
	user_id = get_jwt_identity()
	exists = find_document('organizations', {"name": req_obj['name'], "owner": user_id}) is not None
	if exists:
		return jsonify(message='Cannot add same organization again'), HTTPStatus.CONFLICT
	
	result = add_document_to_collection('organizations', {"name": req_obj['name'], "owner": user_id})
	if result.inserted_id is None:
		return jsonify(message='Unable to create organization'), 400
	return jsonify({"ack": True, "organizationId": str(result.inserted_id)}), HTTPStatus.CREATED



# # FR 2: Create an Organization Join Code
# create_code_schema = {
#   "$schema": "http://json-schema.org/draft-07/schema#",
#   "type": "object",
#   "properties": {
#     "name": {
#       "type": "string",
#       "minLength": 5
#     }
#   },
#   "required": ["name"],
#   "additionalProperties": False
# }

# @user_bp.route('/organization/code', methods=['POST'])
# @jwt_required()
# @validate_schema(create_organization_schema)
# def organization_code():
# 	pass