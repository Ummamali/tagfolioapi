# app/__init__.py

import os

from flask import Flask, jsonify

from flask_cors import CORS

def create_app():

	app = Flask(__name__)
	CORS(app)


	# Connections with database
	app.config['DB_USER'] = 'application'
	app.config['DB_PASSWORD'] = 'tf123'
	app.config['DB_URI'] = f'mongodb://{app.config["DB_USER"]}:{app.config["DB_PASSWORD"]}@127.0.0.1:9900/'
	app.config['DB_NAME'] = 'tagfolio'

	
	# The main / route to ping the whole server
	@app.route('/', methods=('GET',))
	def home():
		return jsonify({"status": 200, "msg": "Tagfolio Backend Services: Working!", "service": "Tagfolio Simple Backend"})

	# Import the routes to register them with the app
	from app.user.routes import user_bp

	# Register the blueprints
	app.register_blueprint(user_bp, url_prefix='/user')



	return app
