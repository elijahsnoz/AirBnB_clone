#!/usr/bin/python3
"""BaseModel Module"""
import uuid
from datetime import datetime


class BaseModel:
    """Defines all common attributes/methods for other classes"""

    def __init__(self, *args, **kwargs):
        """Initialize instance attributes"""
        DATE_TIME = '%Y-%m-%dT%H:%M:%S.%f'
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ['created_at', 'updated_at']:
                        self.__dict__[key]=datetime.strptime(value, DATE_TIME)
                    elif key[0]=="id":
                        self.__dict__[key]=str(value)
                    else:
                        self.__dict__[key]=value
        else:
            self.id = str(uuid.uuid4())
            self.created_at=datetime.now()
            self.updated_at=datetime.now()

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

