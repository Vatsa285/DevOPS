import os
from datetime import datetime, timezone

from flask import Flask, jsonify, request
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "assessment_a")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
collection = client[MONGO_DB].items


def serialize(item):
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "description": item.get("description", ""),
        "created_at": item.get("created_at", ""),
    }


@app.get("/")
def home():
    return jsonify({"app": "Assessment 1A CRUD API", "endpoints": ["/items", "/health"]})


@app.get("/health")
def health():
    try:
        client.admin.command("ping")
        return jsonify({"status": "healthy", "database": "reachable"})
    except PyMongoError as error:
        return jsonify({"status": "unhealthy", "error": str(error)}), 503


@app.get("/items")
def list_items():
    return jsonify([serialize(item) for item in collection.find().sort("created_at", 1)])


@app.post("/items")
def create_item():
    payload = request.get_json(silent=True) or {}
    name = str(payload.get("name", "")).strip()
    if not name:
        return jsonify({"error": "name is required"}), 400
    item = {
        "name": name,
        "description": str(payload.get("description", "")),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    result = collection.insert_one(item)
    item["_id"] = result.inserted_id
    return jsonify(serialize(item)), 201


@app.get("/items/<item_id>")
def get_item(item_id):
    from bson import ObjectId

    try:
        item = collection.find_one({"_id": ObjectId(item_id)})
    except Exception:
        item = None
    if item is None:
        return jsonify({"error": "item not found"}), 404
    return jsonify(serialize(item))


@app.put("/items/<item_id>")
def update_item(item_id):
    from bson import ObjectId

    payload = request.get_json(silent=True) or {}
    updates = {key: payload[key] for key in ("name", "description") if key in payload}
    if not updates:
        return jsonify({"error": "name or description is required"}), 400
    try:
        result = collection.update_one({"_id": ObjectId(item_id)}, {"$set": updates})
    except Exception:
        result = None
    if result is None or result.matched_count == 0:
        return jsonify({"error": "item not found"}), 404
    return jsonify(serialize(collection.find_one({"_id": ObjectId(item_id)})))


@app.delete("/items/<item_id>")
def delete_item(item_id):
    from bson import ObjectId

    try:
        result = collection.delete_one({"_id": ObjectId(item_id)})
    except Exception:
        result = None
    if result is None or result.deleted_count == 0:
        return jsonify({"error": "item not found"}), 404
    return jsonify({"message": "item deleted"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
