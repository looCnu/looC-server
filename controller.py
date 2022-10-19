from flask import Blueprint, request
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
