from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS  # Import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Load your config

    # Enable CORS for all routes, you can also specify the origins if needed
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})  # This allows all domains by default; you can configure it further if required

    # Initialize the database and migration
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Import your models here to ensure they are registered with SQLAlchemy
        from .models import Product  # Adjust the import based on your project structure
        db.create_all()  # Create database tables if they do not exist

        # Import and register your blueprint
        from .routes import bp
        app.register_blueprint(bp)

    return app
