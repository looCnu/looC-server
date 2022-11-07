import sqlite3
import json
from typing import Optional, List
from pydantic import BaseModel
from flask import make_response, request
import jwt, hashlib

conn = sqlite3.connect('looC.db', check_same_thread=False)
c = conn.cursor()

class Member(BaseModel):
    student_id: str
    password: str
    name: Optional[str]
    college: Optional[str]
    preference: Optional[List[str]]

class Lecture(BaseModel):
    lecture_id: str
    name: str
    category: str
    time: str
    description: str
    credit: int

class eval(BaseModel):
    lecture_id: str
    eval_id: int
    rating: float
    contents: str

class Feed(BaseModel):
    lecture_id: str
    feed_id: int
    contents: str

class Comment(BaseModel):
    feed_id: int
    comment_id: int
    contents: str

def verify():
    encoded = request.cookies.get('accessToken')
    decoded = jwt.decode(encoded, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithms=["HS256"])
    result = c.execute(
        'select * from member where student_id="'+decoded['student_id']+'"'
    )
    return result

def sign_in(member: Member):
    response = make_response()
    data = { 'success': False }
    m = hashlib.sha256()
    m.update(member.password.encode('utf-8'))
    member.password = m.hexdigest()
    result = c.execute(
        'select student_id from member where student_id=\"'+member.student_id+'\" and password=\"'+member.password+'\"'
    ).fetchall()
    if result:
        student_id = result[0][0]
        encoded = jwt.encode({'student_id': student_id}, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithm='HS256')
        response.set_cookie('accessToken', encoded, max_age=60*60*2)
        data['success'] = True
    response.data = json.dumps(data)
    return response

def sign_up(member: Member):
    response = make_response()
    m = hashlib.sha256()
    m.update(member.password.encode('utf-8'))
    member.password = m.hexdigest()
    c.execute(
        'insert into member values (\"'+member.student_id+'\",\"'+member.password+'\",\"'+member.name+'\",\"'+member.college+'\")'
    )
    for category in member.preference:
        c.execute(
            'insert into preference values(\"'+member.student_id+'\",\"'+category+'\")'
        )
    conn.commit()
    return response

def get_lectures():
    response = make_response()
    result = c.execute(
        'select * from lecture'
    ).fetchall()
    if result:
        arr = []
        for temp in result:
            lecture = Lecture(
                lecture_id=temp[0],
                name=temp[1],
                category=temp[2],
                time=temp[3],
                description=temp[4],
                credit=temp[5]
            ).dict()
            arr.append(lecture)
        response.data = json.dumps(arr)
    return response

def find_lectures(lecture_id, name, category, credit):
    response = make_response()
    conditions = []
    lecture_id = 'lecture_id="'+lecture_id+'"' if lecture_id else ''
    if lecture_id: conditions.append(lecture_id)
    name = 'name="'+name+'"' if name else ''
    if name: conditions.append(name)
    category = 'category="'+category+'"' if category else ''
    if category: conditions.append(category)
    credit = 'credit="'+credit+'"' if credit else ''
    if credit: conditions.append(credit)
    condition_string = ' and '.join(conditions)
    result = c.execute(
        'select * from lecture where '+condition_string
    ).fetchall()
    if result:
        arr = []
        for temp in result:
            lecture = Lecture(
                lecture_id=temp[0],
                name=temp[1],
                category=temp[2],
                time=temp[3],
                description=temp[4],
                credit=temp[5]
            ).dict()
            arr.append(lecture)
        response.data = json.dumps(arr)
    return response
    
def get_feeds(lecture_id):
    response = make_response()
    result = c.execute(
        'select * from feed where lecture_id="'+lecture_id+'"'
    ).fetchall()
    if result:
        arr = []
        for temp in result:
            feed = Feed(
                lecture_id = temp[0],
                feed_id = temp[1],
                contents = temp[2]
            ).dict()
            arr.append(feed)
        response.data = json.dumps(arr)
    return response

