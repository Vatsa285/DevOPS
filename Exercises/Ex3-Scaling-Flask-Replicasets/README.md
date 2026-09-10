# Exercise 3: Scaling Flask App on Single Node using ReplicaSets

## Real-Life Use Case: E-commerce Flash Sale
During flash sales (like Flipkart's Big Billion Days), traffic can spike from 100 to 10,000 requests per minute. ReplicaSets allow scaling to handle the load.

## Objective
- Understand ReplicaSets and Pods
- Scale Flask App deployment
- Observe pod distribution and load balancing

## Files
- `app.py` - Flash sale Flask application with `/`, `/buy`, and `/health` endpoints
- `Dockerfile` - Container definition using gunicorn
- `replicaset.yaml` - Kubernetes ReplicaSet manifest (3 replicas)
- `service.yaml` - Kubernetes Service manifest (NodePort)

## Solution Steps

### Step 1: Clean Up & Start Minikube
```bash
minikube stop
minikube delete
minikube start --nodes=1
```

### Step 2: Build Docker Image
```bash
eval $(minikube docker-env)
docker build -t flashsale:1.0 .
```

### Step 3: Deploy ReplicaSet and Service
```bash
kubectl apply -f replicaset.yaml
kubectl apply -f service.yaml
```

### Step 4: Verify Pods
```bash
kubectl get pods -o wide
```

**Expected Output:**
```
NAME                         READY   STATUS    RESTARTS   AGE   IP           NODE
flashsale-replicaset-abc12   1/1     Running   0          30s   10.244.0.5   minikube
flashsale-replicaset-def34   1/1     Running   0          30s   10.244.0.6   minikube
flashsale-replicaset-ghi56   1/1     Running   0          30s   10.244.0.7   minikube
```

### Step 5: Access the Application
```bash
minikube service flashsale-service --url
```

### Step 6: Test Load Distribution
```bash
# Run multiple requests and observe different pod names serving
for i in $(seq 1 10); do
  curl -s $(minikube service flashsale-service --url)/buy | python3 -m json.tool
  echo "---"
done
```

### Step 7: Scale Up/Down
```bash
# Scale up to 5 replicas
kubectl scale replicaset flashsale-replicaset --replicas=5
kubectl get pods

# Scale down to 2 replicas
kubectl scale replicaset flashsale-replicaset --replicas=2
kubectl get pods
```

### Step 8: Test Resilience (Delete a Pod)
```bash
# Delete a pod and watch ReplicaSet recreate it
kubectl delete pod <pod-name>
kubectl get pods -w
```

### Step 9: Clean Up
```bash
kubectl delete -f service.yaml
kubectl delete -f replicaset.yaml
minikube stop
```

## Key Learnings
- **ReplicaSets** ensure the desired number of pod replicas are always running
- **Load balancing** distributes traffic across pods automatically
- **Self-healing** - if a pod dies, the ReplicaSet creates a new one
- **Horizontal scaling** is as simple as changing the replica count
