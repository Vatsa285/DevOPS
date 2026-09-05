# Exercise 2: Deploy a Flask App on Minikube using kubectl and YAML

## Objective
Learn Kubernetes basics using Minikube to set up a single-node cluster and deploy a Python Flask application.

## Prerequisites
- Minikube installed
- kubectl installed
- Docker installed

## Files
- `app.py` - Flask application
- `Dockerfile` - Container definition
- `flask-deployment.yaml` - Kubernetes Deployment manifest
- `flask-service.yaml` - Kubernetes Service manifest

## Solution Steps

### Step 1: Start Minikube
```bash
minikube start
```

### Step 2: Build Docker Image with Minikube's Docker Daemon
```bash
eval $(minikube docker-env)
docker build -t flask-app .
```

### Step 3: Deploy the Application
```bash
kubectl apply -f flask-deployment.yaml
kubectl apply -f flask-service.yaml
```

### Step 4: Verify Deployment
```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

**Expected Output:**
```
NAME        READY   UP-TO-DATE   AVAILABLE   AGE
flask-app   1/1     1            1           30s
```

### Step 5: Access the Application
```bash
minikube service flask-app-service --url
```

### Step 6: Test the Application
```bash
curl $(minikube service flask-app-service --url)
```

**Expected Output:**
```
Hello from Flask on Kubernetes!
```

### Step 7: Clean Up
```bash
kubectl delete -f flask-service.yaml
kubectl delete -f flask-deployment.yaml
minikube stop
```

## Key Concepts
- **imagePullPolicy: Never** - Forces Kubernetes to use the locally built image
- **Deployment** - Manages the desired state of Pods
- **Service (NodePort)** - Exposes the deployment to external traffic
