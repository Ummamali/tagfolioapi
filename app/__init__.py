# app/__init__.py

import os
from flask_mail import Mail, Message

from flask import Flask, jsonify

from flask_cors import CORS

def create_app():

	app = Flask(__name__)
	CORS(app)


	# Connections with database
	app.config['DB_USER'] = 'application'
	app.config['DB_PASSWORD'] = 'tf123'
	app.config['DB_URI'] = f'mongodb://{app.config["DB_USER"]}:{app.config["DB_PASSWORD"]}@127.0.0.1:9000/'
	app.config['DB_NAME'] = 'tagfolio'
	# For mailing and other stuff
	app.config['MAIL_EMAIL'] = os.environ.get('TAGFOLIO_EMAIL', None)
	app.config['MAIL_PASSWORD'] = os.environ.get('TAGFOLIO_PASSWORD', None)

	if any(item is None for item in (app.config['MAIL_EMAIL'], app.config['MAIL_PASSWORD'])):
		raise Exception("Environment variables not set properly!")

	# The main / route to ping the whole server
	@app.route('/', methods=('GET',))
	def home():
		return jsonify({"status": 200, "msg": "Tagfolio Backend Services: Working!", "service": "Tagfolio Simple Backend"})

	# Import the routes to register them with the app
	from app.user.routes import user_bp

	# Register the blueprints
	app.register_blueprint(user_bp, url_prefix='/user')



	return app
