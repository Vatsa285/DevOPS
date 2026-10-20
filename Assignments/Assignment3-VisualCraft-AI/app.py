"""
VisualCraft AI - Artistic Image Processing Application
DevOps Assignment 3

An AI-powered artistic image processing service that applies
artistic filters and transformations to images.
"""
from flask import Flask, jsonify, request, send_file
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import io
import os
import socket
import uuid

app = Flask(__name__)

UPLOAD_DIR = "/tmp/visualcraft_uploads"
OUTPUT_DIR = "/tmp/visualcraft_outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Available artistic filters
FILTERS = {
    "sketch": "Convert image to pencil sketch style",
    "emboss": "Apply emboss effect",
    "contour": "Extract contour lines",
    "sharpen": "Sharpen the image",
    "blur": "Apply artistic blur",
    "edge_enhance": "Enhance edges for artistic effect",
    "grayscale": "Convert to artistic grayscale",
    "sepia": "Apply sepia tone filter",
    "negative": "Create negative/inverse image",
    "posterize": "Reduce colors for poster effect"
}


def apply_filter(image, filter_name):
    """Apply an artistic filter to the image"""
    if filter_name == "sketch":
        gray = ImageOps.grayscale(image)
        inverted = ImageOps.invert(gray)
        blurred = inverted.filter(ImageFilter.GaussianBlur(radius=21))
        return Image.blend(gray.convert("L"), blurred, alpha=0.5).convert("RGB")

    elif filter_name == "emboss":
        return image.filter(ImageFilter.EMBOSS)

    elif filter_name == "contour":
        return image.filter(ImageFilter.CONTOUR)

    elif filter_name == "sharpen":
        return image.filter(ImageFilter.SHARPEN)

    elif filter_name == "blur":
        return image.filter(ImageFilter.GaussianBlur(radius=5))

    elif filter_name == "edge_enhance":
        return image.filter(ImageFilter.EDGE_ENHANCE_MORE)

    elif filter_name == "grayscale":
        return ImageOps.grayscale(image).convert("RGB")

    elif filter_name == "sepia":
        gray = ImageOps.grayscale(image)
        sepia_r = gray.point(lambda x: min(int(x * 1.2), 255))
        sepia_g = gray.point(lambda x: min(int(x * 1.0), 255))
        sepia_b = gray.point(lambda x: min(int(x * 0.8), 255))
        return Image.merge("RGB", (sepia_r, sepia_g, sepia_b))

    elif filter_name == "negative":
        return ImageOps.invert(image.convert("RGB"))

    elif filter_name == "posterize":
        return ImageOps.posterize(image.convert("RGB"), bits=3)

    return image


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "app": "VisualCraft AI",
        "description": "AI-Powered Artistic Image Processing",
        "version": "1.0",
        "served_by": socket.gethostname(),
        "endpoints": {
            "GET /filters": "List available filters",
            "POST /process": "Apply filter to image",
            "GET /health": "Health check"
        }
    })


@app.route("/filters", methods=["GET"])
def list_filters():
    return jsonify({"filters": FILTERS})


@app.route("/process", methods=["POST"])
def process_image():
    """Process an uploaded image with the specified filter"""
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]
    filter_name = request.form.get("filter", "grayscale")

    if filter_name not in FILTERS:
        return jsonify({
            "error": f"Unknown filter '{filter_name}'",
            "available_filters": list(FILTERS.keys())
        }), 400

    try:
        image = Image.open(file.stream)
        processed = apply_filter(image, filter_name)

        # Save to buffer
        output_buffer = io.BytesIO()
        processed.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return send_file(
            output_buffer,
            mimetype="image/png",
            as_attachment=True,
            download_name=f"visualcraft_{filter_name}_{uuid.uuid4().hex[:8]}.png"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/process/demo", methods=["GET"])
def demo_process():
    """Generate a demo image with a filter applied"""
    filter_name = request.args.get("filter", "sepia")

    # Create a demo gradient image
    img = Image.new("RGB", (400, 300))
    for x in range(400):
        for y in range(300):
            r = int(255 * x / 400)
            g = int(255 * y / 300)
            b = int(255 * (x + y) / 700)
            img.putpixel((x, y), (r, g, b))

    processed = apply_filter(img, filter_name)

    output_buffer = io.BytesIO()
    processed.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    return send_file(output_buffer, mimetype="image/png")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "visualcraft-ai",
        "pod": socket.gethostname(),
        "filters_available": len(FILTERS)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
