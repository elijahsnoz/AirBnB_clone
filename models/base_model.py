#!/usr/bin/python3
"""BaseModel Module"""
import uuid
from datetime import datetime

class BaseModel:
    """Defines all common attributes/methods for other classes"""

    def __init__(self):
        """Initialize instance attributes"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        """Return string representation of the instance"""
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__
        )

    def save(self):
        """Update the public instance attribute updated_at"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Return a dictionary containing all keys/values of __dict__"""
        instance_dict = self.__dict__.copy()
        instance_dict['__class__'] = type(self).__name__
        instance_dict['created_at'] = self.created_at.isoformat()
        instance_dict['updated_at'] = self.updated_at.isoformat()
        return instance_dict

