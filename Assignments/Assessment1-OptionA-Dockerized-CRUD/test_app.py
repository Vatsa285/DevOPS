import os

os.environ["MONGO_URI"] = "mongodb://localhost:27017"

from app import app


def test_home():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert response.get_json()["app"] == "Assessment 1A CRUD API"
