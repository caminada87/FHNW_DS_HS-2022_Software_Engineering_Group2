import os

from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS

import requests
import requests_toolbelt.adapters.appengine



#Application factory function (This returns the flask web application!)
def create_app(test_config=None):
    requests_toolbelt.adapters.appengine.monkeypatch()
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    
    app.config.from_mapping(
        #should be overwritten on deployment (random value)
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'frontend.sqlite'),
        MODEL=os.path.join(app.instance_path, '../frontend/static/decision_tree_model.sav')
    )

    if test_config is None:
        #load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load the test config if passed in
        app.config.from_mapping(test_config)
    
    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World'
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import prediction
    app.register_blueprint(prediction.bp)

    from .geolocator import GeoLocation
    from .predictor import HousePricePrediction
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)
    api.add_resource(HousePricePrediction, '/HousePricePrediction')
    api.add_resource(GeoLocation, '/GeoLocation')
    
    app.register_blueprint(api_bp)

    app.add_url_rule('/', endpoint='index')

    return app
