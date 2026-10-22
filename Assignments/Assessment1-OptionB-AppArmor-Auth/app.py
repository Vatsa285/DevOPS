import os
from datetime import datetime, timezone

from flask import Flask, jsonify, request
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, PyMongoError
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "assessment_b")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
users = client[MONGO_DB].users


@app.get("/")
def home():
    return jsonify({"app": "Assessment 1B Secure Auth API", "endpoints": ["/register", "/login", "/health"]})


@app.get("/health")
def health():
    try:
        client.admin.command("ping")
        return jsonify({"status": "healthy", "database": "reachable"})
    except PyMongoError as error:
        return jsonify({"status": "unhealthy", "error": str(error)}), 503


@app.post("/register")
def register():
    payload = request.get_json(silent=True) or {}
    username = str(payload.get("username", "")).strip()
    password = str(payload.get("password", ""))
    if not username or len(password) < 8:
        return jsonify({"error": "username and a password of at least 8 characters are required"}), 400
    users.create_index("username", unique=True)
    user = {
        "username": username,
        "password_hash": generate_password_hash(password),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    try:
        users.insert_one(user)
    except DuplicateKeyError:
        return jsonify({"error": "username already exists"}), 409
    return jsonify({"message": "registered", "username": username}), 201


@app.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    username = str(payload.get("username", "")).strip()
    password = str(payload.get("password", ""))
    user = users.find_one({"username": username})
    if user is None or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "invalid credentials"}), 401
    return jsonify({"message": "login successful", "username": username})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
