"""Routines associated with the application data.
"""
import json
courses={}

def load_data():
    """Load the data from the json file.
    """
    with open('json/course.json') as f:
        obj=json.load(f)
        for i in obj:
            courses[int(i["id"])]=i
    return courses


