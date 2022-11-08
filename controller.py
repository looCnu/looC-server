from flask import Blueprint, request
from typing import Optional
import service
import model

bp = Blueprint('main', __name__, url_prefix='/looC')

@bp.route('/hello', methods=['GET'])
def hello():
    return 'Hello World!'

@bp.route('/sign-in', methods=['POST'])
def sign_in():
    member = model.Member(**request.get_json())
    response = service.sign_in(member)
    return response

@bp.route('/sign-up', methods=['POST'])
def sign_up():
    member = model.Member(**request.get_json())
    response = service.sign_up(member)
    return response

@bp.route('/lectures', methods=['GET'])
def get_lectures():
    response = service.get_lectures()
    return response

@bp.route('/find-lectures', methods=['GET'])
def find_lectures():
    args = request.args
    lecture_id = args.get('lecture_id')
    name = args.get('name')
    category = args.get('category')
    credit = args.get('credit')
    response = service.find_lectures(lecture_id, name, category, credit)
    return response

@bp.route('/evals', methods=['GET'])
def get_evals():
    args = request.args
    lecture_id = args.get('lecture_id')
    response = service.get_evals(lecture_id)
    return response

@bp.route('/feeds', methods=['GET'])
def get_feeds():
    args = request.args
    lecture_id = args.get('lecture_id')
    response = service.get_feeds(lecture_id)
    return response

@bp.route('/find-feeds', methods=['GET'])
def find_feeds():
    args = request.args
    lecture_id = args.get('lecture_id')
    title = args.get('title')
    response = service.find_feeds(lecture_id, title)
    return response

