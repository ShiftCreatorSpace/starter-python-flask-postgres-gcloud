import os
import uuid

from flask import request
from flask_restful import Resource, marshal_with, fields, reqparse
from .utils.entity_resolver_utils import resolve_entities
from .resource_fields.example_resource_fields import example_resource_fields

from common.models.base import db
from common.models.example_model_dao import ExampleModelDao

example_get_parser = reqparse.RequestParser()

example_get_parser.add_argument('id', type=str, location="view_args", required=True, help='Invalid `id`')

class Example(Resource):
    @resolve_entities(example_get_parser)
    @marshal_with(example_resource_fields)
    def get(self):
        return {
            "id": request.example.id
        }

    @marshal_with(example_resource_fields)
    def post(self):
        session = db.session
        example = ExampleModelDao()
        session.add(example)
        session.commit()

        return example, 201
