from flask import Blueprint, jsonify, request
from app.database.tasks import add_document_to_collection

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/signup', methods=['POST'])
def login():
  data = request.json
  result = add_document_to_collection(data['username'], data['password'])
  return jsonify({'acknowledged': result.acknowledged})