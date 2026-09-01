# Exercise 1: Kubernetes Getting Started - Hello Pod

## Objective
Run your first app inside Kubernetes and access it using Minikube.

## Business Problem (Zepto Example)
As a DevOps Engineer at Zepto, deploy a lightweight web app (storefront and delivery status page) on Kubernetes using nginx container image.

## Pre-Requisites

### Install Minikube
```bash
# On Linux:
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# On macOS:
brew install minikube

# On Windows (PowerShell as Administrator):
choco install minikube
```

### Install kubectl
```bash
# On Linux:
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# On Windows:
choco install kubernetes-cli
```

## Solution Steps

### Step 1: Start Minikube
```bash
minikube start
```

### Step 2: Verify Cluster
```bash
kubectl cluster-info
minikube status
```

**Expected Output:**
```
Kubernetes control plane is running at https://192.168.49.2:8443
CoreDNS is running at https://192.168.49.2:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

### Step 3: Create an nginx Pod
```bash
kubectl run zepto-storefront --image=nginx --port=80
```

### Step 4: Verify Pod is Running
```bash
kubectl get pods
```

**Expected Output:**
```
NAME               READY   STATUS    RESTARTS   AGE
zepto-storefront   1/1     Running   0          30s
```

### Step 5: Expose the Pod as a Service
```bash
kubectl expose pod zepto-storefront --type=NodePort --port=80
```

### Step 6: Access the Application
```bash
minikube service zepto-storefront --url
```

### Step 7: Verify with curl
```bash
curl $(minikube service zepto-storefront --url)
```

**Expected Output:**
```html
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
```

### Step 8: Check Pod Details
```bash
kubectl describe pod zepto-storefront
```

### Step 9: View Logs
```bash
kubectl logs zepto-storefront
```

### Step 10: Clean Up
```bash
kubectl delete service zepto-storefront
kubectl delete pod zepto-storefront
minikube stop
```

## Key Learnings
- **Pods** are the smallest deployable units in Kubernetes
- **Services** expose pods to external traffic
- **NodePort** allows access to services from outside the cluster
- **Minikube** provides a local single-node Kubernetes cluster for development
