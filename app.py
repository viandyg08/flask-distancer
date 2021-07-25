from flask import Flask
import logging.config
import yaml
from distancer.routes import distancer


def create_app():
    app = Flask(__name__)

    # Use logging.conf to define logging
    logging.config.dictConfig(yaml.load(open('logging.conf'), Loader=yaml.FullLoader))

    app.register_blueprint(distancer)
    return app
