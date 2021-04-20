import os

from flask_restful import Resource


class Meta(Resource):
    def get(self):
        return os.environ.get('DEPLOY_VERSION', 'dev'), 201
