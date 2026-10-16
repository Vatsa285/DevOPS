# Assignment 2: TreasureBook - DevOps Pipeline

## Overview
A Book Collection Management application with a complete DevOps CI/CD pipeline including Docker containerization, Kubernetes deployment, and Jenkins automation.

## Architecture
```
Code → Jenkins (Build/Test/Deploy) → Docker Image → Kubernetes (3 replicas)
```

## Files
- `app.py` - TreasureBook Flask REST API
- `test_app.py` - Unit tests
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container definition
- `k8s-deployment.yaml` - Kubernetes Deployment + Service
- `Jenkinsfile` - CI/CD Pipeline

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | App info and endpoints |
| GET | `/books` | List all books |
| GET | `/books/<id>` | Get specific book |
| POST | `/books` | Add a new book |
| DELETE | `/books/<id>` | Delete a book |
| GET | `/books/search?genre=<genre>` | Search by genre |
| GET | `/health` | Health check |

## Solution Steps

### Step 1: Run Locally
```bash
pip install -r requirements.txt
python app.py
# Visit http://localhost:5000
```

### Step 2: Run Tests
```bash
python -m unittest test_app.py -v
```

### Step 3: Build Docker Image
```bash
docker build -t treasurebook:1.0 .
docker run -d -p 5000:5000 --name treasurebook treasurebook:1.0
```

### Step 4: Deploy on Kubernetes
```bash
minikube start
eval $(minikube docker-env)
docker build -t treasurebook:1.0 .
kubectl apply -f k8s-deployment.yaml
minikube service treasurebook-service --url
```

### Step 5: Test API
```bash
# List books
curl http://localhost:5000/books

# Add a book
curl -X POST http://localhost:5000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Docker Deep Dive", "author": "Nigel Poulton", "genre": "Technology", "rating": 4.6}'

# Search books
curl http://localhost:5000/books/search?genre=Technology
```

### Step 6: Jenkins CI/CD
1. Create a Pipeline job in Jenkins
2. Point to the Jenkinsfile
3. Build triggers: Poll SCM or webhook
4. Pipeline stages: Clone → Build → Test → Deploy → Verify

## Key Learnings
- End-to-end DevOps pipeline from code to deployment
- Docker containerization with production-ready Gunicorn server
- Kubernetes deployment with health probes and replicas
- Jenkins automation for CI/CD
