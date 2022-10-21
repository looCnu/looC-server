import sqlite3
from typing import Optional
from pydantic import BaseModel
from flask import make_response
import jwt, hashlib

conn = sqlite3.connect('looC.db', check_same_thread=False)
c = conn.cursor()

class Member(BaseModel):
    student_id: str
    password: str
    name: Optional[str]
    college: Optional[str]

class Lecture(BaseModel):
    lecture_id: str
    name: str
    category: str
    time: str
    description: str
    credit: int

class Feed(BaseModel):
    lecture_id: str
    feed_id: str
    contents: str

class Comment(BaseModel):
    feed_id: str
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
    m = hashlib.sha256()
    m.update(member.password.encode('utf-8'))
    member.password = m.hexdigest()
    result = c.execute(
        'select student_id from member where student_id=\"'+member.student_id+'\" and password=\"'+member.password+'\"'
    )
    if result:
        student_id = result.fetchall()[0][0]
        encoded = jwt.encode({'student_id': student_id}, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithm='HS256')
        response.set_cookie('accessToken', encoded, max_age=60*60*2)
    return response

def sign_up(member: Member):
    response = make_response()
    m = hashlib.sha256()
    m.update(member.password.encode('utf-8'))
    member.password = m.hexdigest()
    result = c.execute(
        'insert into member values (\"'+member.student_id+'\",\"'+member.password+'\",\"'+member.name+'\",\"'+member.college+'\")'
    )
    conn.commit()
    return response

def get_lectures():
    response = make_response()
    result = c.execute(
        'select * from lecture'
    )
    if result:
        arr = []
        for temp in result:
            arr.push(Lecture(**temp).dict())
        response.data = arr
    return response

def find_lectures(lecture_id, name, category, credit):
    response = make_response()
    conditions = []
    lecture_id = if lecture_id 'lecture_id="'+lecture_id+'"' else ''
    if lecture_id: conditions.push(lecture_id)
    category = if category 'category="'+category+'"' else ''
    if category: conditions.push(category)
    credit = if credit 'credit="'+credit+'"' else ''
    if credit: conditions.push(credit)
    condition_string = ' and '.join(conditions)
    result = c.execute(
        'select * from lecture where '+condition_string
    )
    if result:
        arr = []
        for temp in result:
            arr.push(Lecture(**temp).dict())
        response.data = arr
    return response
    
