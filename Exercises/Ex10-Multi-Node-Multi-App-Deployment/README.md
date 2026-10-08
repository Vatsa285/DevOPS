# Exercise 10: Multi-Node Kubernetes Cluster with Multiple Applications

## Storyboard
Building an e-commerce platform with two microservices:
1. **Product Catalog (AppA)** - Lists available products (2 replicas)
2. **Shopping Cart (AppB)** - Manages user shopping carts (3 replicas)

Replicas are distributed across multiple nodes for high availability and fault tolerance.

## Files
- `product_catalog.py` - Product Catalog Flask app
- `shopping_cart.py` - Shopping Cart Flask app
- `Dockerfile.product-catalog` - Dockerfile for Product Catalog
- `Dockerfile.shopping-cart` - Dockerfile for Shopping Cart
- `product-catalog-deployment.yaml` - K8s Deployment + Service (2 replicas)
- `shopping-cart-deployment.yaml` - K8s Deployment + Service (3 replicas)

## Solution Steps

### Step 0: Clean Up Existing Minikube
```bash
minikube stop
minikube delete
```

### Step 1a: Start Minikube with Multiple Nodes
```bash
minikube start --nodes 3 -p devops-multinode --force
```

### Step 1b: Enable Registry Add-on
```bash
minikube -p devops-multinode addons enable registry
```

### Step 2: Verify Nodes
```bash
kubectl get nodes
```

**Expected Output:**
```
NAME                   STATUS   ROLES           AGE   VERSION
devops-multinode       Ready    control-plane   60s   v1.31.0
devops-multinode-m02   Ready    <none>          40s   v1.31.0
devops-multinode-m03   Ready    <none>          20s   v1.31.0
```

### Step 3: Build and Load Images
```bash
# Build Product Catalog
docker build -t product-catalog:latest -f Dockerfile.product-catalog .
minikube -p devops-multinode image load product-catalog:latest

# Build Shopping Cart
docker build -t shopping-cart:latest -f Dockerfile.shopping-cart .
minikube -p devops-multinode image load shopping-cart:latest
```

### Step 4: Deploy Applications
```bash
kubectl apply -f product-catalog-deployment.yaml
kubectl apply -f shopping-cart-deployment.yaml
```

### Step 5: Verify Pod Distribution
```bash
kubectl get pods -o wide
```

**Expected Output:**
```
NAME                              READY   STATUS    NODE
product-catalog-xxx-abc           1/1     Running   devops-multinode
product-catalog-xxx-def           1/1     Running   devops-multinode-m02
shopping-cart-xxx-ghi             1/1     Running   devops-multinode
shopping-cart-xxx-jkl             1/1     Running   devops-multinode-m02
shopping-cart-xxx-mno             1/1     Running   devops-multinode-m03
```

### Step 6: Access Services
```bash
minikube -p devops-multinode service product-catalog-service --url
minikube -p devops-multinode service shopping-cart-service --url
```

### Step 7: Test Endpoints
```bash
# Test Product Catalog
curl http://<service-url>/products

# Test Shopping Cart
curl -X POST http://<service-url>/cart/add \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user1", "item": "Laptop"}'

curl http://<service-url>/cart
```

### Step 8: Test Fault Tolerance
```bash
# Delete a node and watch pods redistribute
kubectl drain devops-multinode-m02 --ignore-daemonsets --force
kubectl get pods -o wide
```

### Step 9: Clean Up
```bash
kubectl delete -f product-catalog-deployment.yaml
kubectl delete -f shopping-cart-deployment.yaml
minikube -p devops-multinode stop
minikube -p devops-multinode delete
```

## Key Learnings
- **Multi-node clusters** distribute pods across nodes for redundancy
- **Minikube registry add-on** enables image sharing between nodes
- **Pod anti-affinity** can ensure replicas are on different nodes
- **Fault tolerance** - pods are rescheduled when a node goes down
- Separate microservices can be independently scaled
