# shopping_cart.py
from flask import Flask, jsonify, request
import socket

app = Flask(__name__)

cart = []

@app.route("/cart", methods=["GET"])
def view_cart():
    return jsonify(cart)

@app.route("/cart", methods=["POST"])
@app.route("/cart/add", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    cart.append(data)
    return jsonify(cart), 201

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "shopping-cart", "pod": socket.gethostname()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
