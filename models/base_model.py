#!/usr/bin/python3
"""BaseModel Module"""
import models
import uuid
from datetime import datetime


class BaseModel:
    """Defines all common attributes/methods for other classes"""

    def __init__(self, *args, **kwargs):
        """Initialize instance attributes"""
        from models import storage  # Delayed import to avoid circular import
        DATE_TIME = '%Y-%m-%dT%H:%M:%S.%f'
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key in ['created_at', 'updated_at']:
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)
            return
            """string_date = datetime.strptime(value, DATE_TIME)
                    self.__dict__[key] = string_date
                else:
                    self.__dict__[key] = value"""

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        models.storage.new(self)  # Add new instance to storage

    def __str__(self):
        """Return string representation of the instance"""
        return "[{}] ({}) {}".\
            format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """Update the public instance attribute updated_at"""
        """from models import storage 
        # Delayed import to avoid circular import
        """

        self.updated_at = datetime.now()
        storage.save()  """Save the change to storage"""

    def to_dict(self):
        """Return a dictionary containing all keys/values of __dict__"""
        instance_dict = {**self.__dict__}
        instance_dict["__class__"] = type(self).__name__
        instance_dict["created_at"] = instance_dict["created_at"].isoformat()
        instance_dict['updated_at'] = instance_dict["updated_at"].isoformat()
        return instance_dict
