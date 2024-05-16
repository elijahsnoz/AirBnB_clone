#!/usr/bin/python3
from models.base_model import BaseModel


class City(BaseModel):
    """Represent a city

    Attributes:
        state_id (str): state id.
        name (str): City name

    """
    state_id = ""
    name = ""
