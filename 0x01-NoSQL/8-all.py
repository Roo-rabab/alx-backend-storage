#!/usr/bin/env python3
"""
Write a Python function that lists all documents in a collection
"""

def list_all(mongo_collection):
    '''Function that return list of all documents in a collection
    '''
    return [doc for doc in mongo_collection.find()]
