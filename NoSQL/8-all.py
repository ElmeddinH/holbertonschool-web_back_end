#!/usr/bin/env python3
"""Module to list all documents in a MongoDB collection."""


def list_all(mongo_collection):
    """List all documents in a collection, return empty list if none."""
    return list(mongo_collection.find())
