from flask import Flask
from flask_cors import CORS
from .database import db

def create_app():

    app = Flask(__name__)

    # Allow requests from frontend
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://inventory_user:inventory123@postgres:5432/inventory_db"

    db.init_app(app)

    from app.routes import api
    app.register_blueprint(api, url_prefix="/api")

    return app