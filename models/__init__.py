#!/usr/bin/env python3
# __init__.py
""" This module auto initialises a FileStorage instance """

from models.engine.file_storage import FileStorage
storage = FileStorage()
storage.reload()
