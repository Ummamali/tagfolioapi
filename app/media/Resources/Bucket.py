# This file contains all the handler for buckets
from flask_restful import Resource, reqparse
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.utils.database import DBConnection
from app.utils.middlewares import validate_schema_resource
from bson import ObjectId
from flask import jsonify
from http import HTTPStatus


class BucketListResource(Resource):
    create_bucket_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {"name": {"type": "string"}},
        "required": ["name"],
    }

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        with DBConnection() as db:
            col_ocean = db["ocean"]
            # Aggregation pipeline to paginate through resources array
            result = col_ocean.find_one(
                {"_id": ObjectId(user_id)}, {"_id": 0, "buckets": 1}
            )
            return jsonify(result["buckets"])

    @jwt_required()
    @validate_schema_resource(create_bucket_schema)
    def post(self):
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
            print(result)
            if len(result) > 0:
                return {"msg": "Cannot create the same bucket again"}, 400

            new_bucket = {
                "name": name,
                "items": [],
                "disorderedBucket": [],
                "summary": [],
                "stars": 0,
            }

            print("creating bucket....")
            result = col_ocean.update_one(
                {"_id": ObjectId(user_id)},
                {"$push": {"buckets": new_bucket}},
            )

            return new_bucket, HTTPStatus.CREATED
