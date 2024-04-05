# This file contains all the handler for buckets
from flask_restful import Resource, reqparse
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.utils.database import DBConnection
from app.utils.middlewares import validate_schema, paginate
from bson import ObjectId
from flask import jsonify
from http import HTTPStatus


class BucketListResource(Resource):
    create_bucket_schema = {
        "type": "object",
        "properties": {"name": {"type": "string", "minLength": 5}},
        "required": ["name"],
    }

    @jwt_required()
    @paginate()
    def get(self, page, per_page):
        user_id = get_jwt_identity()
        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', 10)
        skip = (page - 1) * per_page
        with DBConnection() as db:
            col_ocean = db["ocean"]
            # Aggregation pipeline to paginate through resources array
            pipeline = [
                # Match documents based on criteria
                {'$match': {"_id": ObjectId(user_id)}},
                # Paginate resources array
                {'$project': {'buckets': {
                    '$slice': ['$buckets', skip, per_page]}}}
            ]
            result = list(col_ocean.aggregate(pipeline))
            print(result)
            return jsonify(result)

    @jwt_required()
    @validate_schema(create_bucket_schema)
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
            if len(result) > 0:
                return jsonify(msg="Cannot create same bucket again"), 400

            new_bucket = {"name": name, "items": []}

            # col_ocean.update_one()
            result = col_ocean.update_one(
                {"_id": ObjectId(user_id)},
                {"$push": {"buckets": new_bucket}},
            )

            return jsonify(new_bucket), HTTPStatus.CREATED
