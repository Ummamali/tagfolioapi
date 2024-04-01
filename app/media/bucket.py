from flask import Blueprint, jsonify, request, Response
from app.utils.middlewares import validate_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.database import DBConnection
from .routes import media_bp
from bson import ObjectId
from app.utils.json_encoder import jsonify_customs
from json import dumps
from http import HTTPStatus


@media_bp.route("/bucket/all", methods=["POST"])
@jwt_required()
def get_all_buckets():
    user_id = get_jwt_identity()
    with DBConnection() as db:
        col_ocean = db["ocean"]
        result = col_ocean.find_one({"_id": ObjectId(user_id)})
        return Response(
            dumps(result["buckets"], default=jsonify_customs),
            mimetype="application/json",
        )


create_bucket_schema = {
    "type": "object",
    "properties": {"name": {"type": "string", "minLength": 5}},
    "required": ["name"],
}


@media_bp.route("/bucket/create", methods=["POST"])
@jwt_required()
@validate_schema(create_bucket_schema)
def create_bucket():
    req_obj = request.json
    user_id = get_jwt_identity()
    name = req_obj["name"]
    with DBConnection() as db:
        col_ocean = db["ocean"]
        result = list(
            col_ocean.aggregate(
                [
                    {"$match": {"_id": ObjectId(user_id)}},
                    {"$unwind": "$buckets"},
                    {"$match": {"buckets.name": name}},
                    {"$project": {"_id": 0, "bucket": "$buckets"}},
                ]
            )
        )
        if len(result) > 0:
            return jsonify(msg="Cannot create same bucket again"), 400

        new_bucket = {"name": name, "items": []}

        # col_ocean.update_one()
        result = col_ocean.update_one(
            {"_id": ObjectId(user_id)},
            {"$push": {"buckets": new_bucket}},
        )

        return jsonify(new_bucket), HTTPStatus.CREATED
