import unittest
from app import app

class TestVisualCraftAI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.testing = True

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["app"], "VisualCraft AI")

    def test_list_filters(self):
        response = self.client.get("/filters")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("filters", data)
        self.assertIn("sketch", data["filters"])
        self.assertIn("sepia", data["filters"])
        self.assertIn("grayscale", data["filters"])

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "visualcraft-ai")

    def test_demo_process(self):
        response = self.client.get("/process/demo?filter=grayscale")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "image/png")

    def test_process_no_image(self):
        response = self.client.post("/process")
        self.assertEqual(response.status_code, 400)

    def test_process_invalid_filter(self):
        from io import BytesIO
        from PIL import Image
        img = Image.new("RGB", (100, 100), color="red")
        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        response = self.client.post(
            "/process",
            data={"image": (buf, "test.png"), "filter": "invalid_filter"},
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
