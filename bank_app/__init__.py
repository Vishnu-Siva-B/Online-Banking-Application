from flask import Flask

# Importing all blueprints
from .views import views


def create_app():
    # Create an instance of the Flask application
    app = Flask(__name__)

    # Set the Flask app's secret key for session management
    app.config["SECRET_KEY"] = "Bankapp"

    # Register all blueprints, setting their URL prefix
    app.register_blueprint(views, url_prefix="/")

    return app
