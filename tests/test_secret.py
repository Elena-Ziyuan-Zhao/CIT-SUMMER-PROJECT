import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, mock_open
from datetime import datetime
from models.secret import Secret

class TestSecretModel(unittest.TestCase):

    def setUp(self):
        self.secret = Secret(
            id=1,
            title="Test Secret",
            content="This is a test secret.",
            created_date=datetime(2023, 1, 1),
            user_id=1,
            expires_at=None,
            rating=5
        )

    def test_secret_initialization(self):
        self.assertEqual(self.secret.id, 1)
        self.assertEqual(self.secret.title, "Test Secret")
        self.assertEqual(self.secret.content, "This is a test secret.")
        self.assertEqual(self.secret.created_date, datetime(2023, 1, 1))
        self.assertEqual(self.secret.user_id, 1)
        self.assertIsNone(self.secret.expires_at)
        self.assertEqual(self.secret.rating, 5)

    @patch("builtins.open", new_callable=mock_open, read_data="name\nFakeName1\nFakeName2\nFakeName3")
    @patch("random.choice", return_value="FakeName2")
    def test_anonymous_poster(self, mock_random_choice, mock_file):
        anonymous_name = self.secret.anonymous_poster
        mock_file.assert_called_once_with("fakenames.csv", "r")
        mock_random_choice.assert_called_once()
        self.assertEqual(anonymous_name, "FakeName2")

    def test_default_created_date(self):
        secret = Secret(title="New Secret", content="Content", user_id=2)
        self.assertIsNotNone(secret.created_date)

    def test_default_rating(self):
        secret = Secret(title="New Secret", content="Content", user_id=2)
        self.assertEqual(secret.rating, 0)

if __name__ == "__main__":
    unittest.main()