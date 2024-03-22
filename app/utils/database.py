from pymongo import MongoClient
from bson import ObjectId
from flask import current_app
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def find_document(collection_name, query):
    # Connect to MongoDB (Make sure you have MongoDB running locally or provide connection details)
    client = MongoClient(current_app.config["DB_URI"])

    # Access the specified database
    db = client[
        current_app.config["DB_NAME"]
    ]  # Replace 'your_database_name' with the actual database name

    # Access the specified collection
    collection = db[collection_name]

    # Find the document based on the query
    result = collection.find_one(query)

    return result


def add_document_to_collection(collection_name, document):
    # Connect to MongoDB (Make sure you have MongoDB running locally or provide connection details)
    client = MongoClient(current_app.config["DB_URI"])

    # Access the specified database
    db = client[current_app.config["DB_NAME"]]

    # Access the specified collection
    collection = db[collection_name]

    # Insert the document into the collection
    result = collection.insert_one(document)

    return result


def delete_document(collection_name, query):
    # Connect to MongoDB
    client = MongoClient(current_app.config["DB_URI"])

    # Select the database
    db = client[current_app.config["DB_NAME"]]

    # Select the collection
    collection = db[collection_name]

    # Delete the document
    result = collection.delete_one(query)

    return result.deleted_count


def update_document(collection_name, filter_query, update_query):
    # Connect to MongoDB
    client = MongoClient(current_app.config["DB_URI"])

    # Select the database
    db = client[current_app.config["DB_NAME"]]

    # Select the collection
    collection = db[collection_name]

    # Update the document, below function is exactly the same but not have $set
    result = collection.update_one(filter_query, {"$set": update_query})

    return result


def update_document_core(collection_name, filter_query, update_query):
    # Connect to MongoDB
    client = MongoClient(current_app.config["DB_URI"])

    # Select the database
    db = client[current_app.config["DB_NAME"]]

    # Select the collection
    collection = db[collection_name]

    # Updates the document, passes the update_query as it is
    result = collection.update_one(filter_query, update_query)

    return result


def db_alive(mongodb_uri, timeoutMS=2000):

    try:
        # Connect to the MongoDB server
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=timeoutMS)
        # Ping the server to check if it's available
        client.admin.command("ping")
        # If ping is successful, return True
        return True
    except ConnectionFailure:
        # If there's a connection failure, return False
        return False
