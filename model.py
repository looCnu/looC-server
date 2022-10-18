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

def sign_in(member: Member):
    m = hashlib.sha256()
    m.update(member.password.encode('utf-8'))
    member.password = m.hexdigest()
    result = c.execute(
        'select student_id from member where student_id=\"'+member.student_id+'\" and password=\"'+member.password+'\"'
    )
    if result:
        student_id = result.fetchall()[0][0]
        encoded = jwt.encode({'student_id': student_id}, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithm='HS256')
        response = make_response('{"status": 200}')
        response.set_cookie('accessToken', encoded, max_age=60*60*2)
        return response
    else:
        return None

def sign_up(member: Member):
    m = hashlib.sha256()
    m.update(member.password.encode('utf-8'))
    member.password = m.hexdigest()
    result = c.execute(
        'insert into member values (\"'+member.student_id+'\",\"'+member.password+'\",\"'+member.name+'\",\"'+member.college+'\")'
    )
    conn.commit()
    return {'status': 200}
