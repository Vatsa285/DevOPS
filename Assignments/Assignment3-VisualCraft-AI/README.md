# Assignment 3: VisualCraft AI - Artistic Image Processing with DevOps

## Overview
An AI-powered artistic image processing service with 10 artistic filters, deployed using Docker and Kubernetes with a complete CI/CD pipeline.

## Architecture
```
Upload Image → Flask API → PIL Image Processing → Filtered Image
                  ↓
Jenkins CI/CD → Docker → Kubernetes (2 replicas)
```

## Available Filters

| Filter | Description |
|--------|-------------|
| `sketch` | Pencil sketch style |
| `emboss` | Emboss 3D effect |
| `contour` | Contour line extraction |
| `sharpen` | Image sharpening |
| `blur` | Artistic Gaussian blur |
| `edge_enhance` | Edge enhancement |
| `grayscale` | Artistic grayscale |
| `sepia` | Vintage sepia tone |
| `negative` | Color inversion |
| `posterize` | Reduced color poster |

## Files
- `app.py` - VisualCraft AI Flask application with image processing
- `test_app.py` - Unit tests
- `requirements.txt` - Python dependencies (Flask, Pillow)
- `Dockerfile` - Container definition
- `k8s-deployment.yaml` - Kubernetes Deployment + Service
- `Jenkinsfile` - CI/CD Pipeline with security scan

## Solution Steps

### Step 1: Run Locally
```bash
pip install -r requirements.txt
python app.py
```

### Step 2: Test Filters
```bash
# List available filters
curl http://localhost:5000/filters

# Demo filter (generates a sample image)
curl http://localhost:5000/process/demo?filter=sepia -o sepia_demo.png

# Process an uploaded image
curl -X POST http://localhost:5000/process \
  -F "image=@photo.jpg" \
  -F "filter=sketch" \
  -o sketch_output.png
```

### Step 3: Run Tests
```bash
python -m unittest test_app.py -v
```

### Step 4: Build Docker Image
```bash
docker build -t visualcraft-ai:1.0 .
docker run -d -p 5000:5000 --name visualcraft visualcraft-ai:1.0
```

### Step 5: Deploy on Kubernetes
```bash
minikube start
eval $(minikube docker-env)
docker build -t visualcraft-ai:1.0 .
kubectl apply -f k8s-deployment.yaml
minikube service visualcraft-ai-service --url
```

### Step 6: Jenkins CI/CD Pipeline
Pipeline stages:
1. **Clone** - Pull code from GitHub
2. **Build** - Build Docker image
3. **Test** - Run unit tests
4. **Security Scan** - Inspect Docker image
5. **Deploy** - Apply Kubernetes manifests
6. **Smoke Test** - Verify pods are running

## Key Learnings
- **Image processing** with Python Pillow (PIL) library
- **Resource limits** in Kubernetes for CPU/memory management
- **Security scanning** in CI/CD pipelines
- **Rollback strategy** on deployment failure
- **Multi-threaded Gunicorn** for handling concurrent image processing
