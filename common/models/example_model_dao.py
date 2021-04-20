import uuid
from .base import db
from sqlalchemy import Column, DateTime, Text, ForeignKey
from .utils.guid import GUID

class ExampleModelDao(db.Model):
    __tablename__ = 'example_model'

    id = Column(GUID, default=uuid.uuid4, nullable=False, primary_key=True)

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.get(_id)

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)
