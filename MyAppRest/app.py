"""Basil package initializer."""
from fakeredis import FakeRedis
from flask import Flask, g, Blueprint, jsonify
from flask_cors import CORS
from flask_restful import Api
from flask_redis import FlaskRedis
from sendgrid import SendGridAPIClient
from twilio.rest import Client
import stripe

from common.models.base import db
from common.models.utils.crypto import bcrypt
from .api.errors.general_errors import BaseAPIError
# from .api.errors.http import errors
from .api.meta import Meta
from .api.example import Example

from .settings import ProdConfig


def create_app(config_object=ProdConfig):
    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)

    db.init_app(app)

    CORS(app)
    bcrypt.init_app(app)

    create_api(app)

    return app

def create_api(app):
    api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
    api = Api(api_bp, catch_all_404s=True)

    api.add_resource(Meta, '/')
    api.add_resource(Example, '/example')

    app.register_blueprint(api_bp)
