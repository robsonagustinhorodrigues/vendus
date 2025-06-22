from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

from .meli_auth import meli_auth
api.register_blueprint(meli_auth, url_prefix='/meli_auth')

from .meli import meli
api.register_blueprint(meli, url_prefix='/meli')

@api.route('/')
def index():
    return "API is running. api/"

