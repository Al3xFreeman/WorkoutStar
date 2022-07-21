from datetime import datetime, timedelta
import unittest
from app import db, create_app
from app.models import *
from config import Config

#testing class that inherits from Config so we can override or
#   add new fields to have a fresh database where to perform the tests
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()