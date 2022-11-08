import model
from flask import make_response

def verify():
    return model.verify()

def sign_in(member: model.Member):
    response = model.sign_in(member)
    response.status = 200
    return response

def sign_up(member: model.Member):
    response = model.sign_up(member)
    response.status = 200
    return response

def get_lectures():
    if verify():
        response = model.get_lectures()
        response.status = 200
        return response
    else:
        return make_response('', 401)

def find_lectures(lecture_id, name, category, credit):
    if verify():
        response = model.find_lectures(lecture_id, name, category, credit)
        response.status = 200
        return response
    else:
        return make_response('', 401)

def get_feeds(lecture_id):
    if verify():
        response = model.get_feeds(lecture_id)
        response.status = 200
        return response
    else:
        return make_response('', 401)

