#!/usr/bin/env python3
"""Module to update topics of a school document in MongoDB."""


def update_topics(mongo_collection, name, topics):
    """Change all topics of a school document based on the name."""
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
