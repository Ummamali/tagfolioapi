from pymongo import MongoClient
from bson import ObjectId

def check_credentials(username, password):
    # Connect to MongoDB (replace with your connection string)
    client = MongoClient("mongodb://localhost:27017/")
    
    # Specify the database and collection
    db = client["tagfolio"]
    collection = db["users"]

    # Query for the user with the provided username
    user_document = collection.find_one({"username": username})

    # Close the MongoDB connection
    client.close()

    # Check if the user was found
    if user_document:
        # Check if the provided password matches the stored password
        if user_document["password"] == password:
            return True  # Passwords match
        else:
            return False  # Passwords do not match
    else:
        return False  # User not found





def add_document_to_collection(username, password):
    # Replace with your MongoDB connection string
    mongo_uri = "mongodb://localhost:27017/"

    # Connect to MongoDB
    client = MongoClient(mongo_uri)

    # Specify the database and collection
    db = client["tagfolio"]
    collection = db["users"]

    # Create a document with the provided username and password
    document = {
        "username": username,
        "password": password,
    }

    # Insert the document into the collection
    result = collection.insert_one(document)


    # Close the MongoDB connection
    client.close()
    return result