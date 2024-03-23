from pymongo import MongoClient
from dummy_data import dummy_data

# This file contains all the dummy data for demonstration and testing purposes

db_url = "mongodb://application:tf123@127.0.0.1:9000/"
db_name = "tagfolio"


def seed_database():
    # Connect to MongoDB
    client = MongoClient(db_url)
    db = client[db_name]

    # Insert the dummy data into a collection
    for coll_name, documents in dummy_data.items():
        collection = db[coll_name]
        collection.insert_many(documents)
        print(f" * Collection {coll_name} has been seeded ")

    # Close the connection
    client.close()

    print("Database at port 9000 seeded!")


def clear_all_collections():
    # Connect to the MongoDB server
    client = MongoClient(db_url)

    # Access the specified database
    db = client[db_name]

    # Get a list of all collection names in the database
    collection_names = db.list_collection_names()

    # Clear each collection
    for collection_name in collection_names:
        collection = db[collection_name]
        collection.delete_many({})  # Delete all documents in the collection

    print(f"All collections of {db_name} cleared successfully.")


if __name__ == "__main__":
    q = input("Do you want to clear all collections before seeding (y/n): ")
    if q.lower()[0] == "y":
        clear_all_collections()
    seed_database()
