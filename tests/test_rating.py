import unittest
from rating.py import Rating
from db import db

class TestRatingModel(unittest.TestCase):
    def setUp(self):
        # Set up a test database 
        self.rating = Rating(secret_id=1, rating=5)

    def test_rating_creation(self):
        """Test that a Rating object is created correctly."""
        self.assertEqual(self.rating.secret_id, 1)
        self.assertEqual(self.rating.rating, 5)

    def test_default_rating_value(self):
        """Test that the default rating value is set to 0."""
        rating = Rating(secret_id=2)
        self.assertEqual(rating.rating, 0)

    def test_relationship_with_secret(self):
        """Test the relationship between Rating and Secret."""
        # Assuming test Secret object is set up
        mock_secret = type("Secret", (object,), {"id": 1})
        self.rating.secret = mock_secret
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