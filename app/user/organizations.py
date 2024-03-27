# This file contains all the routes for Use Case 4: Managing Organizations

from .routes import user_bp
from app.utils.middlewares import validate_schema, validate_schema_multiple
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from app.utils.database import (
    find_document,
    add_document_to_collection,
    update_document,
    update_document_core,
    replace_ids_with_documents,
)
from http import HTTPStatus
import random

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
    org_ids = {
        "joined": user.get("joinedOrganizations"),
        "owned": user.get("ownedOrganizations"),
    }
    res_obj = {**org_ids}
    res_obj = replace_ids_with_documents(
        res_obj, "joined", "organizations", {"_id": 1, "name": 1, "members": 1}
    )
    res_obj = replace_ids_with_documents(
        res_obj, "owned", "organizations", {"_id": 1, "name": 1, "members": 1}
    )

    new_joined = []
    for item in res_obj["joined"]:
        hydrated_doc = replace_ids_with_documents(
            item, "members", "users", {"username": 1}
        )
        new_joined.append(hydrated_doc)
    print(new_joined)
    return jsonify(res_obj)


# Frs Organization
@user_bp.route("/organization", methods=["POST"])
@jwt_required()
@validate_schema_multiple(organization_schema)
def organization():
    req_obj = request.json
    user_id = get_jwt_identity()
    exists = (
        find_document("organizations", {"name": req_obj["name"], "owner": user_id})
        is not None
    )
    if exists:
        return (
            jsonify(message="Cannot add same organization again"),
            HTTPStatus.CONFLICT,
        )

    result = add_document_to_collection(
        "organizations", {"name": req_obj["name"], "owner": user_id, "members": []}
    )
    if result.inserted_id is None:
        return jsonify(message="Unable to create organization"), 400
    return (
        jsonify({"ack": True, "organizationId": str(result.inserted_id)}),
        HTTPStatus.CREATED,
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
    doc = find_document("organizations", {"owner": user_id, "name": req_obj["name"]})
    if doc is None:
        return jsonify(message="Cannot find Organization"), HTTPStatus.BAD_REQUEST
    if doc["owner"] != user_id:
        return jsonify(message="Unauthorized"), HTTPStatus.UNAUTHORIZED
    result = update_document("organizations", {"_id": doc["_id"]}, {"joinCode": code})
    if not result.acknowledged or result.modified_count != 1:
        return (
            jsonify(message="Unable to generate the joining code"),
            HTTPStatus.BAD_REQUEST,
        )
    return jsonify({"ack": True, "codeGenerated": code})


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
        "organizations", {"_id": organization["_id"]}, {"$push": {"members": user_id}}
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
