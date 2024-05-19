#!/usr/bin/python3
"""Initialize storage"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
