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
    time: str
    description: str
    credit: int
    image: str
    room: str
    professor: str
    category: str
    keword: List[str]
    score: float 

class Eval(BaseModel):
    lecture_id: str
    eval_id: int
    rating: float
    contents: str

class Feed(BaseModel):
    lecture_id: str
    feed_id: int
    title: str
    contents: str

class Comment(BaseModel):
    feed_id: int
    comment_id: int
    contents: str

def get_keyword(lecture_id):
    arr = []
    result = c.execute(
        'select name from keyword where lecture_id="'+lecture_id+'"'
    ).fetchall()
    if result:
        for temp in result:
            arr.append(temp[0])
    return arr

def get_score(lecture_id):
    arr = []
    result = c.execute(
        'select rating from eval where lecture_id="'+lecture_id+'"'
    ).fetchall()
    if result:
        for temp in result:
            arr.append(float(temp[0]))
    return sum(arr) / len(arr) if arr else 0

def verify():
    encoded = request.cookies.get('accessToken')
    if not encoded: return False
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
                time=temp[2],
                description=temp[3],
                credit=temp[4],
                image=temp[5],
                room=temp[6],
                professor=temp[7],
                category=temp[8],
                keword=get_keyword(temp[0]),
                score=get_score(temp[0])
            ).dict()
            arr.append(lecture)
        response.data = json.dumps(arr)
    return response

def find_lectures(lecture_id, name, category, credit):
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
                credit=temp[5],
                image=temp[6]
            )
            cond_lecture = lecture_id==lecture.lecture_id if lecture_id else True
            cond_name = name.lower() in lecture.name.lower() if name else True
            cond_category = category==lecture.category if category else True
            cond_credit = credit==lecture.credit if credit else True
            if cond_lecture and cond_name and cond_category and cond_credit: arr.append(lecture.dict())
        response.data = json.dumps(arr)
    return response

def get_evals(lecture_id):
    response = make_response()
    result = c.execute(
        'select * from eval where lecture_id="'+lecture_id+'"'
    ).fetchall()
    if result:
        arr = []
        for temp in result:
            _eval = Eval(
                lecture_id = temp[0],
                eval_id = temp[1],
                rating = temp[2],
                contents = temp[3]
            ).dict()
            arr.append(_eval)
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
                title = temp[2],
                contents = temp[3]
            ).dict()
            arr.append(feed)
        response.data = json.dumps(arr)
    return response

def find_feeds(lecture_id, title):
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
                title = temp[2],
                contents = temp[3]
            )
            cond_title = title in feed.title if title else True
            if cond_title: arr.append(feed.dict())
        response.data = json.dumps(arr)
    return response
