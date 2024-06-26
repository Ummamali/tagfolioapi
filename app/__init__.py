# app/__init__.py

import os
from flask_jwt_extended import JWTManager
from datetime import timedelta

from flask import Flask, jsonify
from colorama import Fore, Style
from flask_cors import CORS
from flask_restful import Api

from app.utils.json_encoder import CustomJSONProvider

from app.utils.database import db_alive


def create_app():

    app = Flask(__name__)
    app.json = CustomJSONProvider(app)
    CORS(app)

    api = Api(app)

    jwt = JWTManager(app)

    # Connections with database
    # app.config["DB_USER"] = "application"
    # app.config["DB_PASSWORD"] = "tf123"
    app.config["DB_URI"] = f"mongodb://127.0.0.1:27017/"
    app.config["DB_NAME"] = "tagfolio"
    # For mailing and other stuff
    app.config["MAIL_EMAIL"] = os.environ.get("TAGFOLIO_EMAIL", None)
    app.config["MAIL_PASSWORD"] = os.environ.get("TAGFOLIO_PASSWORD", None)
    # Setting up json web tokens
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=6)

    # Monitoring the environment variable
    if any(
        item is None for item in (app.config["MAIL_EMAIL"], app.config["MAIL_PASSWORD"])
    ):
        print(
            Fore.RED
            + "WARNING! Environment variables not set properly!"
            + Style.RESET_ALL
        )

    # Monitoring the database
    if not db_alive(app.config["DB_URI"]):
        print(Fore.RED + "WARNING! Unable to ping the database!" + Style.RESET_ALL)

    # The main / route to ping the whole server
    @app.route("/", methods=("GET",))
    def home():
        return jsonify(
            {
                "status": 200,
                "msg": "Tagfolio Backend Services: Working!",
                "service": "Tagfolio Simple Backend",
            }
        )

    # Import the routes to register them with the app
    from app.user.routes import user_bp
    from app.media.routes import media_bp

    # Register the blueprints
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(media_bp, url_prefix="/media")

    # importing the resources
    from app.media.Resources.Bucket import BucketListResource

    # Registering the resources
    api.add_resource(BucketListResource, "/res/buckets")

    return app
