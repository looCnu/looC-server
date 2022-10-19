import model

def sign_in(member: model.Member):
    response = model.sign_in(member)
    if response:
        return response
    else:
        return {'status': 400}

def sign_up(member: model.Member):
    response = model.sign_up(member)
    if response:
        return response
    else:
        return {'status': 400}

def get_lectures():
    response = model.get_lectures()
    if response:
        return response
    else:
        return {'status': 400}
