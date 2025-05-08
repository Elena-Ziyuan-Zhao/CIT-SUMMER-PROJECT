import unittest
from models.user import User
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
class TestUserModel(unittest.TestCase):
#set up test user
    def setUp(self):
        self.user = User(
            first_name="Langston",
            second_name="Chau",
            username="langstonch",
            user_type="regular",
            email="langstonch@gmail.com",
            password="securepassword123"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.first_name, "Langston")
        self.assertEqual(self.user.second_name, "Chau")
        self.assertEqual(self.user.username, "langstonch")
        self.assertEqual(self.user.user_type, "regular")
        self.assertEqual(self.user.email, "langstonch@gmail.com")
        self.assertEqual(self.user.password, "securepassword123")
        self.assertIsInstance(self.user.created_date, datetime)

    def test_default_user_type(self):
        user = User(
            first_name="Someone",
            second_name="Name",
            username="someonename",
            email="soname@example.com",
            password="anothersecurepassword"
        )
        self.assertEqual(user.user_type, "regular")

    def test_relationships(self):
        self.assertEqual(self.user.secrets, [])
       

if __name__ == "__main__":
    unittest.main()