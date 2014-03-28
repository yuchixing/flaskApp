from flask.ext.admin.contrib.mongoengine import ModelView
from flask import request, jsonify
from functools import wraps

class AuthModelView(ModelView):
    def is_accessible(self):
        auth = request.authorization
        if not auth:
            return False
        elif not _check_auth(auth.username, auth.password):
            return False
        return True
                

def _check_auth(username, password):
    return username == 'admin' and password == 'fw2013'

def _authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="ADSD"'

    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth: 
            return _authenticate()

        elif not _check_auth(auth.username, auth.password):
            return _authenticate()
        return f(*args, **kwargs)

    return decorated

