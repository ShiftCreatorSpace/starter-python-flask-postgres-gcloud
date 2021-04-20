from flask import request
from functools import wraps

from common.models.example_model_dao import ExampleModelDao
from MyAppRest.api.errors.general_errors import NotFound

def resolve_entities(argparser):
    def inner_func(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            _resolve(argparser)
            return f(*args, **kwargs)

        return wrap

    return inner_func


def _resolve(argparser):
    request.args = argparser.parse_args()

    example_id = request.args.get('id')

    if example_id is not None and not hasattr(request, 'example'):
        request.example = ExampleModelDao.get_by_id(example_id)
        if request.example is None:
            raise NotFound

