from .routes import user_bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.misc import send_verification_email
from app.utils.middlewares import validate_schema
from app.utils.database import find_document, delete_document
from flask import jsonify, request
from http import HTTPStatus
from bson import ObjectId


@user_bp.route("/delete", methods=["POST"])
@jwt_required()
def delete_account():
    user_id = get_jwt_identity()
    res = send_verification_email("DELETE_ACCOUNT", user_id, "/user/delete")
    if not res:
        return jsonify(message="Unable to send email!"), HTTPStatus.BAD_REQUEST
    return jsonify(message="Email sent successfully")


delete_verify_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {"code": {"type": "string", "pattern": "^[0-9]{6}$"}},
    "required": ["code"],
}


@user_bp.route("/delete/verify", methods=["DELETE"])
@jwt_required()
@validate_schema(delete_verify_schema)
def delete_account_verify():
    user_id = get_jwt_identity()
    req_obj = request.json
    requester = find_document("users", {"_id": ObjectId(user_id)})
    if request is None:
        return jsonify(message="Unauthorized"), HTTPStatus.UNAUTHORIZED
    verify_doc = find_document(
        "verifications",
        {"email": requester["email"], "route": "/user/delete", "code": req_obj["code"]},
    )
    if verify_doc is None:
        return (
            jsonify(message="Unable to find verification option or invalid code"),
            HTTPStatus.BAD_REQUEST,
        )

    # Now user will be deleted and all the places where he is present will be reseted
    delete_document("users", {"_id": ObjectId(requester["_id"])})
    # Now removing him from all organizations
    for org in requester["joinedOrganizations"]:
        pass
    return jsonify(ack=True)
