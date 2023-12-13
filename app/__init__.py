# app/__init__.py

import os

from flask import Flask

from flask_cors import CORS

def create_app():

	app = Flask(__name__)
	CORS(app)

	# You can put other configurations here, such as database connections, etc.
	app.config['STAGING_AREA'] = os.path.join(os.path.dirname(app.root_path), 'staging')
	app.config['BRAIN_PATH'] = os.path.join(app.root_path, 'brain')

	# creating the staging area
	os.makedirs(app.config["STAGING_AREA"], exist_ok=True)
	

	# Import the routes to register them with the app
	from app.routes.upload import upload_route_bp
	from app.routes.root_route import root_bp

	# Register the blueprints
	app.register_blueprint(upload_route_bp)
	app.register_blueprint(root_bp)

	return app