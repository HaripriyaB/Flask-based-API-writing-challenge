"""Routes for the course resource.
"""

from run import app
from flask import request
from http import HTTPStatus
import data
import json
from datetime import datetime
import re

@app.route("/")
def show_data():
    return data.load_data()


@app.route("/course/<int:id>", methods=['GET'])
def get_course(id):
    """Get a course by id.

    :param int id: The record id.
    :return: A single course (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------   
    1. Bonus points for not using a linear scan on your data structure.
    """
    # YOUR CODE HERE
    allcourses = data.load_data()

    try: 
        ans={}
        ans["data"] = allcourses[id]
        return ans
    except:
        return "Course {} does not exist".format(id)
    

@app.route("/course", methods=['GET'])
def get_courses():
    """Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    ------------------------------------------------------------------------- 
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.
    """
    # YOUR CODE HERE
    if request.args.get("title-words")!=None:
        words = list(request.args.get("title-words"))
        resp={}
        with open("json/course.json") as f:
            temp = json.load(f)
            li=[]
            for i in temp:
                for j in words:
                    if j in i["title"]:
                        li.append(i)
            resp["data"]=li
        return resp

    if request.args.get("page-number")!=None:
        resp={}
        pagenumber= int(request.args.get("page-number"))
        pagesize = int(request.args.get("page-size"))
        with open("json/course.json") as f:
            temp = json.load(f)
            resp["data"]=(temp[(pagenumber-1)*pagesize:((pagenumber-1)*pagesize)+pagesize])
        return resp
    else:
        ans={}
        with open("json/course.json") as f:
            temp = json.load(f)
            ans["data"]=temp
        return ans


@app.route("/course", methods=['POST'])
def create_course():
    """Create a course.
    :return: The course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the POST body fields
    """
    # YOUR CODE HERE
    content = request.get_json()
    if request.is_json and content["title"] and content["price"] and len(content["title"])>=6 and len(content["title"])<=100 and len(content["description"])<=255:
        courses = data.load_data()
        content["id"]=list(courses.keys())[-1]+1
        content["date_created"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        content["date_updated"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with open("json/course.json") as f:
            temp = json.load(f)
            temp.append(content)
        with open("json/course.json","w") as f:
            json.dump(temp,f,indent=4)
        
        return content
    else:
        return "Error: Content of the data is not proper"



@app.route("/course/<int:id>", methods=['PUT'])
def update_course(id):
    """Update a a course.
    :param int id: The record id.
    :return: The updated course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the PUT body fields, including checking
       against the id in the URL

    """
    content = request.get_json()
    courses = data.load_data()
    if request.is_json and content["title"] and content["price"] and type(content["on_discount"])==bool and len(content["title"])>=6 and len(content["title"])<=100 and len(content["description"])<=255:
        content["date_created"] = courses[id]["date_created"]
        content["date_updated"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        content["id"]=id
        with open("json/course.json") as f:
            temp = json.load(f)
            x=0
            for i in temp:
                if i["id"]==id:
                    temp[x]=content
                    break
                x=x+1
        with open("json/course.json","w") as f:
            json.dump(temp,f,indent=4)
        return content
    else:
        return "The id does not match the payload"

        





@app.route("/course/<int:id>", methods=['DELETE'])
def delete_course(id):
    """Delete a course
    :return: A confirmation message (see the challenge notes for examples)
    """
    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    None
    """
    # YOUR CODE HERE
    allcourses = data.load_data()

    try: 
        ans = allcourses[id]
        with open("json/course.json") as f:
            temp = json.load(f)
            x=0
            for i in temp:
                if i["id"]==id:
                    temp.pop(x)
                    break
                x=x+1
        with open("json/course.json","w") as f:
            json.dump(temp,f,indent=4)
        
        return "The specified course was deleted"
    except:
        return "Course {} does not exist".format(id)


