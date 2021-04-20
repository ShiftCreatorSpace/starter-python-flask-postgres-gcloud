from flask_restful import HTTPException


class BaseAPIError(HTTPException):
    def __init__(self, description='API Error'):
        HTTPException.__init__(self)
        self.description = self.description if hasattr(self, 'description') else description


class BadRequest(BaseAPIError):
    code = 400
    description = 'Bad request'


class NotAuthorized(BaseAPIError):
    code = 401
    description = 'Not authorized'


class Forbidden(BaseAPIError):
    code = 403
    description = 'Forbidden'


class NotFound(BaseAPIError):
    code = 404
    description = 'Not found'


class Conflict(BaseAPIError):
    code = 409
    description = 'Error'


class Gone(BaseAPIError):
    code = 410
    description = 'Gone'

class RateLimit(BaseAPIError):
    code = 429
    description = 'Too many requests'

class InternalError(BaseAPIError):
    code = 500
    description = "Internal Server Error"
