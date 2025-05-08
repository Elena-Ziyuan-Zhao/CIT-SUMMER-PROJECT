import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.rating import Rating
from db import db
from models.secret import Secret

class TestRatingModel(unittest.TestCase):
    def setUp(self):
        # Set up a test database 
        self.rating = Rating(secret_id=1, rating=5)

    def test_rating_creation(self):
        """Test that a Rating object is created correctly."""
        self.assertEqual(self.rating.secret_id, 1)
        self.assertEqual(self.rating.rating, 5)

    def test_relationship_with_secret(self):
        secret = Secret(id=1) 
        self.rating.secret = secret
        self.assertEqual(self.rating.secret.id, 1)

    def test_primary_key(self):
        """Test that the primary key is set correctly."""
        self.rating.id = 10
        self.assertEqual(self.rating.id, 10)

    def test_foreign_key_secret_id(self):
        """Test that the foreign key secret_id is set correctly."""
        self.assertEqual(self.rating.secret_id, 1)

if __name__ == "__main__":
    unittest.main()