from flask import Blueprint

meli = Blueprint("meli", __name__)

from .auth import auth
meli.register_blueprint(auth, url_prefix='/auth')

@meli.route('/')
def index():
    return "API is running. api/meli"
