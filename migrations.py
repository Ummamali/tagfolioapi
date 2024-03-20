from pymongo import MongoClient
from app.utils.hashing import hash_password
# This file contains all the dummy data for demonstration and testing purposes

# Dummy data for users collection
dummy_users = [
    {"email": "john", "password": hash_password("john12345")},
    {"email": "alice", "password": hash_password("alice12345")},
]

def seed_database():
    # Connect to MongoDB
    client = MongoClient('mongodb://application:tf123@localhost:9000/')
    db = client['tagfolio']
    
    # Insert the dummy data into a collection
    collection = db['users']
    collection.insert_many(dummy_users)

    # Close the connection
    client.close()

if __name__ == "__main__":
    seed_database()
    print("Dummy Data has been added to your database (9000)")
