from flask import Blueprint, jsonify, request
from app.utils.database import add_document_to_collection
from .routes import user_bp

@user_bp.route('/signup', methods=['POST'])
def signup():
  data = request.json
  result = add_document_to_collection('users', {'email': 'test', 'password': 'test'})
  return jsonify({'acknowledged': result.acknowledged})