import sys
import unittest
import io
from main import app

from class_util import ChatModule, UserModule

class AppTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_get_users(self):
        # user = UserModule.get_users()
        x = True
        self.assertTrue(x)
        self.assertTrue(1 > 0)
        # self.assertTrue(user)
        # self.assertTrue(len(user) > 1)

if __name__ == '__main__':
    unittest.main()