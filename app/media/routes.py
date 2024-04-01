from flask import Blueprint

media_bp = Blueprint("media", __name__)

from . import bucket
