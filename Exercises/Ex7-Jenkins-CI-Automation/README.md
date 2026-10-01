# Exercise 7: Introduction to Continuous Integration (CI) and Jenkins

## Objective
Understand CI concepts and set up Jenkins for automated builds and testing.

## What is Continuous Integration (CI)?
Continuous Integration is a development practice where developers frequently integrate code changes into a shared repository. Each integration triggers automated builds and tests.

## Key Features of CI
1. **Frequent Code Integration** - Developers commit multiple times a day
2. **Automated Builds** - Every commit triggers a build
3. **Automated Testing** - Tests run as part of CI
4. **Immediate Feedback** - Quick feedback on changes

## Benefits of CI
- Early bug detection
- Improved collaboration
- Faster development cycles
- High-quality code

## CI Tools Comparison

| Tool | Key Features | Ideal For |
|------|-------------|-----------|
| **Jenkins** | Open-source, plugin ecosystem, Pipeline-as-Code | Enterprise teams |
| **GitLab CI/CD** | Built-in with GitLab, YAML pipelines | GitLab users |
| **CircleCI** | Cloud-based, Docker support | Container workflows |
| **Travis CI** | Easy GitHub integration | Open-source projects |
| **Bamboo** | Atlassian integration | Atlassian ecosystem |
| **TeamCity** | JetBrains, intelligent features | JetBrains users |
| **GitHub Actions** | Native GitHub, YAML workflows | GitHub users |

## Jenkins Installation

### On Ubuntu/Debian:
```bash
# Install Java (prerequisite)
sudo apt update
sudo apt install openjdk-17-jdk -y

# Add Jenkins repository
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install Jenkins
sudo apt update
sudo apt install jenkins -y

# Start Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

### On Windows:
```powershell
# Using Chocolatey
choco install jenkins -y
```

### Using Docker:
```bash
docker run -d --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

### Access Jenkins:
1. Open http://localhost:8080
2. Get initial admin password:
   ```bash
   sudo cat /var/lib/jenkins/secrets/initialAdminPassword
   # OR for Docker:
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```
3. Install suggested plugins
4. Create admin user

## How CI Works (Workflow)
```
Developer → Git Push → CI Server (Jenkins) → Build → Test → Feedback
```

1. Developer writes code and pushes to Git
2. Jenkins detects changes and triggers build
3. Code is compiled and dependencies resolved
4. Automated tests run
5. Results (pass/fail) reported back to developer

## Key Learnings
- CI catches integration issues early
- Jenkins is the most widely used open-source CI server
- Plugins extend Jenkins capabilities
- Pipeline-as-Code (Jenkinsfile) is the modern approach
