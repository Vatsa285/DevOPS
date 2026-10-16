"""
TreasureBook - A Book Collection Management Application
DevOps Assignment 2
"""
from flask import Flask, jsonify, request
import socket
import os

app = Flask(__name__)

# In-memory book collection (treasure book)
treasure_books = [
    {"id": 1, "title": "The DevOps Handbook", "author": "Gene Kim", "genre": "Technology", "rating": 4.8},
    {"id": 2, "title": "The Phoenix Project", "author": "Gene Kim", "genre": "Technology", "rating": 4.7},
    {"id": 3, "title": "Continuous Delivery", "author": "Jez Humble", "genre": "Technology", "rating": 4.6},
    {"id": 4, "title": "Site Reliability Engineering", "author": "Google", "genre": "Technology", "rating": 4.5},
    {"id": 5, "title": "Infrastructure as Code", "author": "Kief Morris", "genre": "Technology", "rating": 4.4},
]

next_id = 6


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "app": "TreasureBook",
        "description": "A Book Collection Management API",
        "version": "1.0",
        "served_by": socket.gethostname(),
        "endpoints": {
            "GET /books": "List all books",
            "GET /books/<id>": "Get a specific book",
            "POST /books": "Add a new book",
            "DELETE /books/<id>": "Delete a book",
            "GET /books/search?genre=<genre>": "Search by genre",
            "GET /health": "Health check"
        }
    })


@app.route("/books", methods=["GET"])
def get_books():
    return jsonify({"books": treasure_books, "total": len(treasure_books)})


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in treasure_books if b["id"] == book_id), None)
    if book:
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404


@app.route("/books", methods=["POST"])
def add_book():
    global next_id
    data = request.get_json()
    new_book = {
        "id": next_id,
        "title": data.get("title", "Unknown"),
        "author": data.get("author", "Unknown"),
        "genre": data.get("genre", "General"),
        "rating": data.get("rating", 0.0)
    }
    treasure_books.append(new_book)
    next_id += 1
    return jsonify({"message": "Book added", "book": new_book}), 201


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global treasure_books
    book = next((b for b in treasure_books if b["id"] == book_id), None)
    if book:
        treasure_books = [b for b in treasure_books if b["id"] != book_id]
        return jsonify({"message": "Book deleted", "book": book})
    return jsonify({"error": "Book not found"}), 404


@app.route("/books/search", methods=["GET"])
def search_books():
    genre = request.args.get("genre", "")
    results = [b for b in treasure_books if genre.lower() in b["genre"].lower()]
    return jsonify({"results": results, "query": genre, "total": len(results)})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "treasurebook",
        "pod": socket.gethostname(),
        "environment": os.getenv("ENV", "development")
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
