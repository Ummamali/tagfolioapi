from .routes import user_bp
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.utils.database import DBConnection
from bson import ObjectId
from flask import jsonify


@user_bp.route('/data', methods=['GET'])
@jwt_required()
def get_user_data():
    user_id = get_jwt_identity()
    user_data = {}
    # now we will construct all the important data about the user

    with DBConnection() as db:
        ocean_col = db['ocean']
        ocean_data = ocean_col.find_one({'_id': ObjectId(user_id)}, {
            "_id": 0, "featuredBuckets": 1, "lastUpdated": 1})
        featured_buckets = ocean_data['featuredBuckets']
        user_data['featuredBuckets'] = featured_buckets
        user_data['lastUpdated'] = ocean_data['lastUpdated']

        # getting the

    return jsonify(user_data)
