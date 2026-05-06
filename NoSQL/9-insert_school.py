#!/usr/bin/env python3
"""Module to insert a document in a MongoDB collection."""


def insert_school(mongo_collection, **kwargs):
    """Insert a new document in a collection and return the new _id."""
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
