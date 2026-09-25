# Exercise 6: Real-Time Operations Monitoring with Grafana

## Objective
As a DevOps engineer at ZAPPTTO, create a real-time monitoring system for a delivery service using Python, Prometheus, Grafana, and Jenkins.

## Architecture
```
Python Metrics App (port 8000) → Prometheus (port 9090) → Grafana (port 3000)
```

## Files
- `delivery_metrics.py` - Python script simulating delivery metrics
- `prometheus.yml` - Prometheus scraping configuration
- `alerts_rules.yml` - Alert rules for monitoring thresholds
- `Jenkinsfile` - Jenkins pipeline for automated setup

## Solution Steps

### Step 1: Install Dependencies
```bash
pip3 install prometheus-client
```

### Step 2: Start the Metrics Server
```bash
python3 delivery_metrics.py
```
Access metrics at: http://localhost:8000/metrics

### Step 3: Start Prometheus with Docker
```bash
docker run -d --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  -v $(pwd)/alerts_rules.yml:/etc/prometheus/alerts_rules.yml \
  prom/prometheus
```
Access Prometheus at: http://localhost:9090

### Step 4: Start Grafana with Docker
```bash
docker run -d --name grafana \
  -p 3000:3000 \
  grafana/grafana
```
Access Grafana at: http://localhost:3000 (default credentials: admin/admin)

### Step 5: Configure Grafana
1. Login to Grafana (admin/admin)
2. Add Prometheus as a data source:
   - URL: `http://host.docker.internal:9090`
3. Create a new dashboard with panels for:
   - Total Deliveries (Gauge)
   - Pending Deliveries (Graph)
   - On-the-way Deliveries (Graph)
   - Average Delivery Time (Graph)

### Step 6: Verify Metrics
```bash
curl http://localhost:8000/metrics
curl http://localhost:9090/api/v1/targets
```

### Step 7: Clean Up
```bash
docker stop prometheus grafana
docker rm prometheus grafana
```

## Metrics Explained
| Metric | Type | Description |
|--------|------|-------------|
| `total_deliveries` | Gauge | Total number of deliveries |
| `pending_deliveries` | Gauge | Number of pending deliveries |
| `on_the_way_deliveries` | Gauge | Deliveries currently in transit |
| `average_delivery_time` | Summary | Average delivery time in seconds |

## Key Learnings
- **Prometheus** scrapes metrics from HTTP endpoints at regular intervals
- **Grafana** visualizes time-series data from Prometheus
- **Alert rules** trigger notifications when thresholds are exceeded
- **prometheus_client** Python library exposes metrics on `/metrics` endpoint
