import unittest
from app import app

class TestTreasureBook(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.testing = True

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["app"], "TreasureBook")

    def test_get_books(self):
        response = self.client.get("/books")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("books", data)
        self.assertGreater(len(data["books"]), 0)

    def test_get_single_book(self):
        response = self.client.get("/books/1")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["id"], 1)

    def test_get_nonexistent_book(self):
        response = self.client.get("/books/999")
        self.assertEqual(response.status_code, 404)

    def test_add_book(self):
        new_book = {
            "title": "Kubernetes Up & Running",
            "author": "Kelsey Hightower",
            "genre": "Technology",
            "rating": 4.5
        }
        response = self.client.post("/books", json=new_book)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["book"]["title"], "Kubernetes Up & Running")

    def test_search_books(self):
        response = self.client.get("/books/search?genre=Technology")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(len(data["results"]), 0)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "healthy")


if __name__ == "__main__":
    unittest.main()
