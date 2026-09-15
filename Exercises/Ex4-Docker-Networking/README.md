# Exercise 4: Docker Networking with Multiple Containers

## Objective
Understand Docker networking concepts and configure a multi-container application with Flask, MySQL, and Redis.

## Scenario
Develop a web application with:
- A Python Flask web server (container 1)
- A MySQL database (container 2)
- A Redis cache (container 3)

## Files
- `app.py` - Flask REST API application
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container definition for Flask app
- `docker-compose.yaml` - Multi-container orchestration

## Solution Steps

### Task 1: Create a Bridge Network
```bash
docker network create --driver bridge my-bridge-net
```

### Task 2: Verify the Network
```bash
docker network ls
```

**Expected Output:**
```
NETWORK ID     NAME           DRIVER    SCOPE
87c23b491f59   my-bridge-net   bridge    local
```

### Task 3: Inspect the Network
```bash
docker network inspect my-bridge-net
```

### Task 4: Launch Containers Individually (Manual Method)

#### Build Flask app image:
```bash
docker build -t flask-networking-app .
```

#### Launch MySQL container:
```bash
docker run -d --name mysql-database \
  --network my-bridge-net \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=myapp \
  -e MYSQL_USER=appuser \
  -e MYSQL_PASSWORD=apppassword \
  mysql:8.0
```

#### Launch Redis container:
```bash
docker run -d --name redis-cache \
  --network my-bridge-net \
  redis:7-alpine
```

#### Launch Flask container:
```bash
docker run -d --name flask-web-server \
  --network my-bridge-net \
  -p 5001:5001 \
  flask-networking-app
```

### Task 5: Using Docker Compose (Recommended)
```bash
docker-compose up -d
```

### Task 6: Verify Connectivity
```bash
# Check all containers are running
docker ps

# Test Flask app
curl http://localhost:5001/about

# Verify network connectivity between containers
docker exec flask-web-server ping mysql-database
docker exec flask-web-server ping redis-cache
```

### Task 7: Inspect Container Networks
```bash
docker network inspect my-bridge-net
```

### Task 8: Clean Up
```bash
docker-compose down -v
# OR manually:
docker stop flask-web-server mysql-database redis-cache
docker rm flask-web-server mysql-database redis-cache
docker network rm my-bridge-net
```

## Key Learnings
- **Bridge Network** - Default Docker network driver for container-to-container communication
- **DNS Resolution** - Containers on the same network can reach each other by container name
- **Network Isolation** - Containers on different networks cannot communicate directly
- **Docker Compose** - Simplifies multi-container orchestration
