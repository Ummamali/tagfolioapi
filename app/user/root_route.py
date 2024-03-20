# app/routes/root_route.py
from flask import jsonify
from .routes import user_bp


@user_bp.route('/')
def root():
    return jsonify({"status": 200, "msg": "Tagfolio Backend Services: Working!", "module": "User Management"})
