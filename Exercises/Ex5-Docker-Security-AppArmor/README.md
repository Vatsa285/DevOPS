# Exercise 5: Docker Security with AppArmor

## Objective
Secure Docker containers using AppArmor profiles to restrict access to sensitive directories and prevent unauthorized actions.

## Scenario
Deploy a Python Flask app in Docker and secure it with AppArmor to:
- Restrict access to sensitive system files (`/etc/shadow`, `/etc/passwd`)
- Prevent execution of unauthorized binaries (`curl`, `wget`, `bash`)
- Deny write access to system directories

## Prerequisites
```bash
# Install AppArmor utilities (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install apparmor-utils
```

## Files
- `app.py` - Simple Flask application
- `Dockerfile` - Container definition
- `my-apparmor-profile` - AppArmor security profile
- `apply_apparmor.py` - Python script to apply profile and test restrictions

## Solution Steps

### Task 1: Build the Docker Image
```bash
docker build -t flask-apparmor .
```

### Task 2: Copy and Load AppArmor Profile
```bash
# Copy profile to AppArmor directory
sudo cp my-apparmor-profile /etc/apparmor.d/my-apparmor-profile

# Load the profile
sudo apparmor_parser -r -W /etc/apparmor.d/my-apparmor-profile
```

### Task 3: Run Container with AppArmor Profile
```bash
docker run -d --name secure-flask-app \
  --security-opt apparmor=my-apparmor-profile \
  -p 5000:5000 \
  flask-apparmor
```

### Task 4: Test Restricted Actions
```bash
# Should be DENIED - reading shadow file
docker exec secure-flask-app cat /etc/shadow

# Should be DENIED - executing curl
docker exec secure-flask-app curl http://localhost

# Should be DENIED - writing to /usr
docker exec secure-flask-app touch /usr/testfile

# Should be ALLOWED - accessing Flask app
curl http://localhost:5000/
```

### Task 5: Run Automated Tests
```bash
python3 apply_apparmor.py
```

### Task 6: Clean Up
```bash
docker stop secure-flask-app
docker rm secure-flask-app
sudo apparmor_parser -R /etc/apparmor.d/my-apparmor-profile
```

## Key Learnings
- **AppArmor** provides Mandatory Access Control (MAC) for Linux applications
- **Security profiles** can restrict file access, network access, and binary execution
- **Docker's `--security-opt`** flag applies AppArmor profiles to containers
- Defense-in-depth approach to container security
