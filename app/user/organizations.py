# This file contains all the routes for Use Case 4: Managing Organizations
import pprint
from .routes import user_bp
from app.utils.middlewares import validate_schema, validate_schema_multiple
from flask import request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from app.utils.database import (
    find_document,
    add_document_to_collection,
    update_document,
    update_document_core,
    replace_ids_with_documents,
    DBConnection,
)
from .org_pipelines import get_all_orgs_pipeline
from http import HTTPStatus
import random
from ..utils.json_encoder import jsonify_customs
import json

organization_schema = {
    "POST": {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {"name": {"type": "string", "minLength": 5}},
        "required": ["name"],
        "additionalProperties": False,
    }
}


# get organizations of a user
@user_bp.route("/organization/all", methods=["GET"])
@jwt_required()
def get_organizations():
    user_id = get_jwt_identity()
    user = find_document("users", {"_id": ObjectId(user_id)})
    if user is None:
        return jsonify(msg="No user"), HTTPStatus.BAD_REQUEST
    with DBConnection() as db:
        users_col = db["users"]

        res_obj = list(users_col.aggregate(get_all_orgs_pipeline(user_id)))

    return Response(
        json.dumps(res_obj[0], default=jsonify_customs), mimetype="application/json"
    )


# Frs Organization
@user_bp.route("/organization", methods=["POST"])
@jwt_required()
@validate_schema_multiple(organization_schema)
def organization():
    req_obj = request.json
    user_id = get_jwt_identity()
    exists = (
        find_document("organizations", {
                      "name": req_obj["name"], "owner": ObjectId(user_id)})
        is not None
    )
    if exists:
        return (
            jsonify(message="Cannot add same organization again"),
            HTTPStatus.CONFLICT,
        )
    new_org = {"name": req_obj["name"],
               "owner": ObjectId(user_id), "members": []}
    result = add_document_to_collection(
        "organizations", new_org
    )
    if result.inserted_id is None:
        return jsonify(message="Unable to create organization"), 400
    with DBConnection() as db:
        col_users = db['users']
        col_users.update_one({'_id': ObjectId(user_id)},
                             {"$push": {"ownedOrganizations": ObjectId(result.inserted_id)}})
    return (
        Response(json.dumps({"created": new_org},
                 default=jsonify_customs), mimetype='application/json')
    )


# FR 2: Generate an Organization Join Code
create_code_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {"name": {"type": "string", "minLength": 5}},
    "required": ["name"],
    "additionalProperties": False,
}


@user_bp.route("/organization/code", methods=["POST"])
@jwt_required()
@validate_schema(create_code_schema)
def organization_code():
    req_obj = request.json
    user_id = get_jwt_identity()
    code = str(random.randint(100000, 999999))
    doc = find_document(
        "organizations", {"owner": ObjectId(user_id), "name": req_obj["name"]})
    if doc is None:
        return jsonify(message="Cannot find Organization"), HTTPStatus.BAD_REQUEST
    if str(doc["owner"]) != user_id:
        return jsonify(message="Unauthorized"), HTTPStatus.UNAUTHORIZED
    result = update_document(
        "organizations", {"_id": doc["_id"]}, {"joinCode": code})
    if not result.acknowledged or result.modified_count != 1:
        return (
            jsonify(message="Unable to generate the joining code"),
            HTTPStatus.BAD_REQUEST,
        )
    return jsonify({"ack": True, "joinCode": code})


# Joining the organization

join_organization_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 5},
        "ownerEmail": {"type": "string", "format": "email"},
        "joinCode": {"type": "string", "pattern": "^[0-9]{6}$"},
    },
    "required": ["name", "ownerEmail", "joinCode"],
}


@user_bp.route("/organization/join", methods=["POST"])
@jwt_required()
@validate_schema(join_organization_schema)
def join_organization():
    req_obj = request.json
    user_id = get_jwt_identity()
    doc = find_document("users", {"email": req_obj["ownerEmail"]})
    if doc is None:
        return jsonify(message="Organization does not exists"), HTTPStatus.BAD_REQUEST
    organization = find_document(
        "organizations", {"owner": str(doc["_id"]), "name": req_obj["name"]}
    )
    if organization is None:
        return jsonify(message="Organization does not exists"), HTTPStatus.BAD_REQUEST
    if organization["joinCode"] != req_obj["joinCode"]:
        return jsonify(message="Unauthorized"), HTTPStatus.UNAUTHORIZED
    # Database State Change
    result = update_document_core(
        "organizations", {"_id": organization["_id"]}, {
            "$push": {"members": user_id}}
    )
    result_user = update_document_core(
        "users",
        {"_id": ObjectId(user_id)},
        {"$push": {"joinedOrganizations": str(organization["_id"])}},
    )
    if not result.acknowledged or not result_user.acknowledged:
        return jsonify(message="Unable to add member"), HTTPStatus.BAD_REQUEST
    return jsonify({"ack": True, "addedMember": user_id})


# Leave Organization
leave_organization_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {"orgId": {"type": "string"}},
    "required": ["orgId"],
}


@user_bp.route("/organization/leave", methods=["POST"])
@jwt_required()
@validate_schema(leave_organization_schema)
def leave_organization():
    req_obj = request.json
    user_id = get_jwt_identity()
    org = find_document("organizations", {"_id": ObjectId(req_obj["orgId"])})
    if org is None:
        return jsonify(message="Unable to find organization"), HTTPStatus.NOT_FOUND
    if org["owner"] == user_id:
        return (
            jsonify(message="Owner cannot leave organization"),
            HTTPStatus.BAD_REQUEST,
        )
    # DB state change
    result_org = update_document_core(
        "organizations",
        {"_id": ObjectId(req_obj["orgId"])},
        {"$pull": {"members": user_id}},
    )
    result_user = update_document_core(
        "users",
        {"_id": ObjectId(user_id)},
        {"$pull": {"joinedOrganizations": req_obj["orgId"]}},
    )
    if not result_org.acknowledged or not result_user.acknowledged:
        return jsonify(message="Unable to leave organization"), HTTPStatus.BAD_REQUEST
    return jsonify(message="Organization left successfully", ack=True)


delete_org_schema = {
    "type": "object",
    "properties": {
        "orgId": {"type": "string"}
    },
    "required": ["orgId"]
}


@user_bp.route("/organization/delete", methods=["DELETE"])
@jwt_required()
@validate_schema(delete_org_schema)
def delete_organization():
    user_id = get_jwt_identity()
    req_obj = request.json
    org_id = req_obj['orgId']
    with DBConnection() as db:
        users_col = db['users']
        exists = users_col.find_one({'_id': ObjectId(user_id), 'ownedOrganizations': {
            "$elemMatch": {"$eq": ObjectId(org_id)}}})
        if exists:
            users_col.update_one({'_id': ObjectId(user_id)}, {
                                 "$pull": {"ownedOrganizations": ObjectId(org_id)}})
            orgs_col = db['organizations']
            response = orgs_col.delete_one({'_id': ObjectId(org_id)})
            if response.deleted_count == 1:
                return jsonify(deleted=org_id)
    return jsonify(msg='Some error while deleting the organization'), HTTPStatus.BAD_REQUEST
