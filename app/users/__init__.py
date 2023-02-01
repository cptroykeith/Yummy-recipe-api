from flask import Blueprint

users = Blueprint('users', __name__)

from users import views