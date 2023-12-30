from flask import Blueprint, jsonify, request
from app.database.tasks import check_credentials

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
  data = request.json
  is_valid = check_credentials(data['username'], data['password'])
  return jsonify({'isValid': is_valid})