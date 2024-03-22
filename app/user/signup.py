from flask import Blueprint, jsonify, request
from app.utils.database import (
    add_document_to_collection,
    find_document,
    delete_document,
)
from http import HTTPStatus
from .routes import user_bp
from app.utils.misc import run_schema, send_email
from app.utils.hashing import hash_password
from app.utils.middlewares import validate_schema
import random

req_obj_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "username": {"type": "string", "minLength": 3},
        "email": {"type": "string", "format": "email"},
        "password": {
            "type": "string",
            "minLength": 8,
            "pattern": "^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]+$",
        },
    },
    "required": ["username", "password", "email"],
}


@user_bp.route("/signup", methods=["POST"])
@validate_schema(req_obj_schema)
def signup():
    req_obj = request.json
    verify = str(random.randint(100000, 999999))
    doc_exists = find_document("users", {"email": req_obj["email"]}) is not None
    if doc_exists:
        return jsonify(message="Cannot register with this email"), HTTPStatus.CONFLICT
    success = send_email(
        req_obj["email"], "Verify Your Registration", f"Verification Code: {verify}"
    )
    if success:
        result = add_document_to_collection(
            "unverified_users",
            {
                "verify": verify,
                "username": req_obj["username"],
                "email": req_obj["email"],
                "password": hash_password(req_obj["password"]),
            },
        )
        return jsonify({"ack": result.acknowledged})
    else:
        return jsonify({"msg": "Unable to send email", "ack": False})


# Now we verify the user
req_obj_schema_verify = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "email": {"type": "string", "format": "email"},
        "verify": {"type": "string", "pattern": "^[0-9]{6}$"},
    },
    "required": ["email", "verify"],
}


@user_bp.route("/signup/verify", methods=["POST"])
@validate_schema(req_obj_schema_verify)
def signup_verify():
    req_obj = request.json
    doc = find_document("unverified_users", {**req_obj})
    if doc is not None and req_obj["verify"] == doc["verify"]:
        del doc["verify"]
        add_document_to_collection("users", {**doc})
        delete_document("unverified_users", {**req_obj})
        return jsonify({"acknowledged": True})
    else:
        return jsonify(ack=False, msg="Unauthorized!"), 400
