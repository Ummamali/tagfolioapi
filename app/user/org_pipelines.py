# this file contains all the pipelines for curating the searches for frontend
from bson import ObjectId


def get_all_orgs_pipeline(user_id):
    pipeline = [
        # Match documents based on user ID
        {"$match": {"_id": ObjectId(user_id)}},
        # Lookup for joined organizations
        {
            "$lookup": {
                "from": "organizations",
                "localField": "joinedOrganizations",
                "foreignField": "_id",
                "as": "joinedOrganizations",
            }
        },
        # Lookup for owned organizations
        {
            "$lookup": {
                "from": "organizations",
                "localField": "ownedOrganizations",
                "foreignField": "_id",
                "as": "ownedOrganizations",
            }
        },
        # Project to include only required fields
        {
            "$project": {
                "_id": 0,
                "joinedOrganizations": {
                    "$map": {
                        "input": "$joinedOrganizations",
                        "as": "joinedOrg",
                        "in": {
                            "name": "$$joinedOrg.name",
                            "owner": "$$joinedOrg.owner",
                            "members": "$$joinedOrg.members",
                            "_id": {"$toString": "$$joinedOrg._id"},
                        },
                    }
                },
                "ownedOrganizations": {
                    "$map": {
                        "input": "$ownedOrganizations",
                        "as": "ownedOrg",
                        "in": {
                            "name": "$$ownedOrg.name",
                            "owner": "$$ownedOrg.owner",
                            "members": "$$ownedOrg.members",
                            "_id": {"$toString": "$$ownedOrg._id"},
                        },
                    }
                },
            }
        },
    ]
    return pipeline
