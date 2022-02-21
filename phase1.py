# This code is for mini project 2 and it is written by Melih Keskin(melih) and Victor Smith(vwsmith)

from pymongo import MongoClient
import json
import string
import random
import datetime
import sys

def create_collection(collection_name, db):
    """
    Creates a collection with the input name
    """
    
    collist = db.list_collection_names() # List collection names
 
    if collection_name in collist: # If the collection already exists
        collection = db[collection_name] # Creates or opens the collection
        collection.delete_many({}) # Delete all entries in the previous collection
    else: # If the collection does not exist
        collection = db[collection_name]["row"]

    return collection


def main():
    
    port_num = input("Enter port number: ")
    # 27017
    client = MongoClient('127.0.0.1', int(port_num))
    db = client["291db"] # Creates or opens the database "291db"

    # change 2

    # Creates collections + deletes duplicates ** (fix)
    Posts = create_collection("Posts", db) 
    Tags = create_collection("Tags", db)
    Votes = create_collection("Votes", db)

    # Fills collections with data

    with open("Posts.json") as f:
        p_data = json.load(f)
    with open("Tags.json") as f:
        t_data = json.load(f)
    with open("Votes.json") as f:
        v_data = json.load(f)  # load data from JSON to dict
    

    db.Posts.insert_many(p_data["posts"]["row"])
    db.Tags.insert_many(t_data["tags"]["row"])
    db.Votes.insert_many(v_data["votes"]["row"])

main()