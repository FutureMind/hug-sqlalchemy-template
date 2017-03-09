import os

from .app import create_app
import hug


app = create_app(os.getenv('APP_CONFIG') or 'default')
