from flask import Flask
from flask_cors import CORS
from .database import db

def create_app():

    app = Flask(__name__)

    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://inventory_user:inventory123@postgres:5432/inventory_db"

    db.init_app(app)

    # 👇 Ye line add karo
    from .models import Category, Product, Supplier, Order, User

    with app.app_context():
        db.create_all()

    from app.routes import api
    app.register_blueprint(api, url_prefix="/api")

    return app