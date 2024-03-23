from app.utils.hashing import hash_password
from bson import ObjectId

dummy_data = {
    "users": [
        {
            "_id": ObjectId("603f5b39872f4f94a26d027d"),
            "email": "tagfolioservices@gmail.com",
            "username": "User1",
            "password": hash_password("password@1"),
            "joinedOrganizations": ["603f5b4e872f4f94a26d027f"],
        },
        {
            "_id": ObjectId("603f5b40872f4f94a26d027e"),
            "email": "ummaali2000@gmail.com",
            "username": "User2",
            "password": hash_password("password@2"),
            "joinedOrganizations": ["603f5b4e872f4f94a26d027f"],
        },
    ],
    "organizations": [
        {
            "_id": ObjectId("603f5b4e872f4f94a26d027f"),
            "name": "Organization1",
            "owner": "603f5b39872f4f94a26d027d",
            "joinCode": "111222",
            "members": ["603f5b40872f4f94a26d027e"],
        }
    ],
}
