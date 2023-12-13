# app/routes/root_route.py
from flask import Blueprint, jsonify

root_bp = Blueprint('root', __name__)

@root_bp.route('/')
def root():
    return jsonify({"status": 200, "msg": "Tagfolio Backend Services: Working!"})
