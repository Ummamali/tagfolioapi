from app.utils.hashing import hash_password
from bson import ObjectId

dummy_data = {
    "users": [
        {
            "_id": ObjectId("603f5b39872f4f94a26d027d"),
            "email": "tagfolioservices@gmail.com",
            "username": "User1",
            "password": hash_password("password@1"),
            "ownedOrganizations": [
                ObjectId("603f5b4e872f4f94a26d027f"),
                ObjectId("603f5b4e872f4f94a26d028f"),
            ],
            "joinedOrganizations": [],
        },
        {
            "_id": ObjectId("603f5b40872f4f94a26d027e"),
            "email": "ummaali2000@gmail.com",
            "username": "User2",
            "password": hash_password("password@2"),
            "ownedOrganizations": [],
            "joinedOrganizations": [
                ObjectId("603f5b4e872f4f94a26d027f"),
                ObjectId("603f5b4e872f4f94a26d028f"),
            ],
        },
    ],
    "organizations": [
        {
            "_id": ObjectId("603f5b4e872f4f94a26d027f"),
            "name": "Organization1",
            "owner": ObjectId("603f5b39872f4f94a26d027d"),
            "joinCode": "111222",
            "members": [ObjectId("603f5b40872f4f94a26d027e")],
        },
        {
            "_id": ObjectId("603f5b4e872f4f94a26d028f"),
            "name": "Organization2",
            "owner": ObjectId("603f5b39872f4f94a26d027d"),
            "joinCode": "111222",
            "members": [ObjectId("603f5b40872f4f94a26d027e")],
        },
    ],
    "ocean": [
        {
            # id is the same as owner's id
            "_id": ObjectId("603f5b40872f4f94a26d027e"),
            "known_faces": {
                "imranKhan": {"name": ["Imran Khan"]},
                "shahrukh": {"name": ["Shahrukh Khan"]},
                "kajol": {"name": ["Kajol Devgan"]},
            },
            "featuredBuckets": [
                {"name": "bucketone", "titleCover": "car.jpg"},
                {"name": "buckettwo", "titleCover": "cats.jpg"},
            ],
            "lastUpdated": 1715150682127,
            "buckets": [
                {
                    "name": "bucketone",
                    "disorderedBucket": [
                        {"title": "jane.jpg"},
                        {"title": "anna.jpg"}
                    ],
                    "items": [
                        {"path": "/", "title": "car.jpg",
                            "tags": {"objects": ["car", "sports_car", "desert", "blue_car"], "people": []}},
                        {"path": "/", "title": "flowers.jpg",
                            "tags": {"objects": ["flowers", "tree", "wall"], "people": []}},
                        {"path": "/", "title": "mountains.jpg",
                            "tags": {"objects": ["mountain", "desert"], "people": []}},
                    ],
                    "summary": ["car", "sports_car", "flowers", "mountain"],
                    "stars": 3
                },
                {"name": "buckettwo",
                 "disorderedBucket": [],
                 "items": [
                     {"path": "/", "title": "cats.jpg",
                      "tags": {"objects": ["cats", "cats (count): 2", "grass"], "people": []}},
                     {"path": "/", "title": "dogs.jpg",
                      "tags": {"objects": ["dogs", "dogs (count): 2", "running_dogs"], "people": []}},
                     {"path": "/", "title": "laptop.jpg",
                      "tags": {"objects": ["computer", "laptop", "macbook", "keyboard"], "people": []}}

                 ], "summary": ["cats", "dogs", "computer", "grass"],
                 "stars": 2

                 }
            ],
        }
    ],
}
