
from flask import Blueprint

user_bp = Blueprint("user", __name__)


from . import login, signup, root_route, edit, organizations, delete_account, user_data