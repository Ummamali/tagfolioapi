from pymongo import MongoClient
from bson import ObjectId
from flask import current_app


    


def find_document(collection_name, query):
    # Connect to MongoDB (Make sure you have MongoDB running locally or provide connection details)
    client = MongoClient(current_app.config['DB_URI'])
    
    # Access the specified database
    db = client[current_app.config['DB_NAME']]  # Replace 'your_database_name' with the actual database name
    
    # Access the specified collection
    collection = db[collection_name]
    
    # Find the document based on the query
    result = collection.find_one(query)
    
    return result





def add_document_to_collection(collection_name, document):
    # Connect to MongoDB (Make sure you have MongoDB running locally or provide connection details)
    client = MongoClient(current_app.config['DB_URI'])
    
    # Access the specified database
    db = client[current_app.config['DB_NAME']]  # Replace 'your_database_name' with the actual database name
    
    # Access the specified collection
    collection = db[collection_name]
    
    # Insert the document into the collection
    result = collection.insert_one(document)
    
    return result