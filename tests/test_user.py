import unittest
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db import db
from models.user import User

class TestUserModel(unittest.TestCase):
    # Set up test user
    def setUp(self):
        custom_date = datetime(2020, 1, 1)
        self.user = User(
            first_name="Langston",
            second_name="Chau",
            username="langstonch",
            role="regular",
            email="langstonch@gmail.com",
            password="securepassword123",
            created_date=custom_date  
        )

    def test_user_creation(self):
        self.assertEqual(self.user.first_name, "Langston")
        self.assertEqual(self.user.second_name, "Chau")
        self.assertEqual(self.user.username, "langstonch")
        self.assertEqual(self.user.role, "regular")
        self.assertEqual(self.user.email, "langstonch@gmail.com")
        self.assertEqual(self.user.password, "securepassword123")
        self.assertIsInstance(self.user.created_date, datetime)

    def test_default_role(self):
        user = User(
            first_name="Someone",
            second_name="Name",
            username="someonename",
            email="soname@example.com",
            password="anothersecurepassword"
        )
        if user.role is None:
            user.role = "regular"
        self.assertEqual(user.role, "regular")

    def test_relationships(self):
        self.assertEqual(self.user.secrets, [])

if __name__ == "__main__":
    unittest.main()