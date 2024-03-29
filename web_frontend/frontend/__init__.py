import os

from flask import Flask, Blueprint, send_from_directory
from flask_restful import Api
from flask_cors import CORS


def create_app(test_config=None) -> Flask:
    """
    Create a flask web application. The configuration can be defined via the
    input test_config.
    @param test_config: Instance configuration
    @return: Flask web application
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    app.config.from_mapping(
        # gets overwritten in container... --> Dockerfiles
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "frontend.sqlite"),
        MODEL=os.path.join(
            app.instance_path, "../frontend/static/decision_tree_model.sav"
        ),
        BASE_URL="http://localhost:5000",
        TESTING=False,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        if os.path.exists(os.path.join(app.instance_path, "config.py")):
            app.config.from_pyfile("config.py")
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db

    db.init_app(app)

    @app.route("/hello")
    def hello_world():
        """
        Return Hello world entry.
        @return: Hello world entry
        """
        return "<p>Hello, World!</p>"

    @app.route("/favicon.ico")
    def favicon():
        """
        Load favicon icon.
        @return: Favicon icon.
        """
        return send_from_directory(
            os.path.join(app.root_path, "static"),
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    from . import auth

    app.register_blueprint(auth.bp)

    from . import accounts

    app.register_blueprint(accounts.bp)

    from . import prediction

    app.register_blueprint(prediction.bp)

    from .geolocator import GeoLocation
    from .predictor import HousePricePrediction

    # API - For internal and external use...
    api_bp = Blueprint("api", __name__)
    api = Api(api_bp)
    api.add_resource(HousePricePrediction, "/HousePricePrediction")
    api.add_resource(GeoLocation, "/GeoLocation")
    app.register_blueprint(api_bp)

    app.add_url_rule("/", endpoint="index")
    return app
