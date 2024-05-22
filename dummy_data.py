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
    # Following is the data about the images stored in two dummy buckets
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
                {"name": "bucketone", "titleCover": "imageOne.jpg"},
                {"name": "buckettwo", "titleCover": "imageOne.jpg"},
            ],
            "lastUpdated": 1715150682127,
            "buckets": [
                {
                    "name": "bucketone",
                    "disorderedBucket": [{"title": "jane.jpg"}, {"title": "anna.jpg"}],
                    "items": [
                        {
                            "path": "/",
                            "title": "imageOne.jpg",
                            "boxes": [],
                            "tags": {
                                "objects": ["bike", "motor_bike", "orange bike"],
                                "people": [],
                            },
                        },
                        {
                            "path": "/",
                            "title": "imageTwo.jpg",
                            "boxes": [],
                            "tags": {
                                "objects": ["car", "desert", "blue car", "vehicle"],
                                "people": [],
                            },
                        },
                        {
                            "path": "/",
                            "title": "imageThree.jpg",
                            "boxes": [],
                            "tags": {
                                "objects": ["tree", "flowers", "red flowers"],
                                "people": [],
                            },
                        },
                        {
                            "path": "/",
                            "title": "imageFour.jpg",
                            "boxes": [],
                            "tags": {
                                "objects": [
                                    "mountain",
                                    "desert",
                                    "blue skies",
                                    "landscape",
                                ],
                                "people": [],
                            },
                        },
                        {
                            "path": "/",
                            "title": "imageFive.jpg",
                            "boxes": [],
                            "tags": {
                                "objects": [
                                    "tree",
                                    "flowers",
                                    "bench",
                                    "chinese",
                                    "architecture",
                                ],
                                "people": [],
                            },
                        },
                        {
                            "path": "/",
                            "title": "imageSix.jpg",
                            "boxes": [],
                            "tags": {
                                "objects": ["pakistan", "prime minister"],
                                "people": ["Imran Khan"],
                            },
                        },
                    ],
                    "summary": ["car", "sports_car", "flowers", "mountain", "trees"],
                    "stars": 3,
                },
                {
                    "name": "buckettwo",
                    "disorderedBucket": [],
                    "items": [
                        {
                            "path": "/",
                            "title": "imageOne.jpg",
                            "boxes": [],
                            "tags": {
                                "objects": ["cats", "cats (count): 2", "grass"],
                                "people": [],
                            },
                        },
                        {
                            "path": "/",
                            "title": "imageTwo.jpg",
                            "boxes": [],
                            "tags": {
                                "objects": ["dogs", "dogs (count): 2", "running_dogs"],
                                "people": [],
                            },
                        },
                        {
                            "path": "/",
                            "title": "imageThree.jpg",
                            "boxes": [],
                            "tags": {
                                "objects": [
                                    "computer",
                                    "laptop",
                                    "macbook",
                                    "keyboard",
                                ],
                                "people": [],
                            },
                        },
                        {
                            "path": "/",
                            "title": "imageFour.jpg",
                            "boxes": [],
                            "tags": {
                                "objects": [
                                    "cars",
                                    "two cars",
                                    "grass",
                                    "blue sky",
                                ],
                                "people": [],
                            },
                        },
                        {
                            "path": "/",
                            "title": "imageFive.jpg",
                            "boxes": [],
                            "tags": {
                                "objects": [
                                    "car",
                                    "sports car",
                                    "road",
                                    "yellow car",
                                ],
                                "people": [],
                            },
                        },
                        {
                            "path": "/",
                            "title": "imageSix.jpg",
                            "boxes": [],
                            "tags": {
                                "objects": ["suits", "actors"],
                                "people": ["Shahrukh Khan", "Amir Khan"],
                            },
                        },
                        {
                            "path": "/",
                            "title": "imageSeven.jpg",
                            "boxes": [],
                            "tags": {
                                "objects": ["suits", "actor"],
                                "people": ["Shahrukh Khan"],
                            },
                        },
                    ],
                    "summary": ["cats", "dogs", "computer", "grass", "cars"],
                    "stars": 2,
                },
            ],
        }
    ],
}
