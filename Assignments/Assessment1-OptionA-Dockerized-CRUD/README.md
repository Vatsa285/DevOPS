# Assignment Assessment 1A: Dockerized CRUD Application

This solution implements the first project choice from the BMS College assessment PDF.
It uses Flask, MongoDB, Docker Compose, a custom bridge network, and Docker SDK scripts.

## Requirements covered

- Flask CRUD API for `/items`.
- MongoDB in a separate container with a named persistent volume.
- Custom bridge network connecting the Flask and MongoDB containers.
- `manage_network.py` creates/inspects the Docker network and checks container connectivity.
- `health_monitor.py` checks the Flask container health and restarts it when unhealthy, logging the event.

## Run

```bash
docker compose up -d --build
curl http://localhost:5000/health
curl -X POST http://localhost:5000/items -H "Content-Type: application/json" -d '{"name":"Docker","description":"Container platform"}'
curl http://localhost:5000/items
python manage_network.py
python health_monitor.py
```

Stop without deleting the database volume:

```bash
docker compose down
```

## Test

```bash
python -m pytest -q
```
