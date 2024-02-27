#!/usr/bin/env python3
'''
Write a Python function that inserts a new document in a collection based on kwargs.
Module with a function that inserts a new document in a collection.
'''

import pymongo


def insert_school(mongo_collection, **kwargs):
    """functon that inserts a new document in a collection"""
    return mongo_collection.insert(kwargs)
