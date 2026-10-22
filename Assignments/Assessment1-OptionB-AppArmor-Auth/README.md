# Assignment Assessment 1B: Secured Multi-Container Auth Application

This solution implements the second project choice from the BMS College assessment PDF.
It uses Flask, MongoDB, Docker networking, AppArmor, Docker SDK verification, and automated health monitoring.

## Requirements covered

- Flask registration and login endpoints with hashed passwords.
- MongoDB in a separate container with a named persistent volume.
- Custom bridge network connecting the web and database containers.
- `assessment-b-python` AppArmor profile restricting sensitive file access and selected binary execution.
- `apply_apparmor.py` loads the profile and verifies Docker `SecurityOpt`.
- `health_monitor.py` checks container health, restarts failures, and writes an alert/restart log.

## Run on Linux with AppArmor enabled

```bash
sudo cp assessment-b-python /etc/apparmor.d/assessment-b-python
sudo apparmor_parser -r /etc/apparmor.d/assessment-b-python
docker compose up -d --build
python apply_apparmor.py
curl http://localhost:5001/health
curl -X POST http://localhost:5001/register -H "Content-Type: application/json" -d '{"username":"alice","password":"correct-horse"}'
curl -X POST http://localhost:5001/login -H "Content-Type: application/json" -d '{"username":"alice","password":"correct-horse"}'
python health_monitor.py
```

Run the monitor as a background service in a separate terminal. It writes `health-monitor.log` and emits an alert whenever it restarts the web container.

## Test

```bash
python -m pytest -q
```

AppArmor and Docker security enforcement require a Linux host or WSL2 with Docker integration. The Compose stack can be inspected on Windows, but the AppArmor profile cannot be enforced there.
