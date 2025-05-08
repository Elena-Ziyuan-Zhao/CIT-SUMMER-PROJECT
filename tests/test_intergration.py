import unittest

import requests 

class TestIntegration(unittest.TestCase):
    BASE_URL = "http://localhost:8888"  

    def test_endpoint(self):
        # Example: Test a GET request to an endpoint
        response = requests.get(f"{self.BASE_URL}/api/example")
        self.assertEqual(response.status_code, 200)
        self.assertIn("expected_key", response.json())

    def test_post_request(self):
        # Example: Test a POST request to an endpoint
        payload = {"key": "value"}
        response = requests.post(f"{self.BASE_URL}/api/example", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("success", response.json())

if __name__ == "__main__":
    unittest.main()