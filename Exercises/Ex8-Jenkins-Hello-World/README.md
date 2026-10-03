# Exercise 8: Creating "Hello World" Jenkins Job

## Objective
Create a basic Jenkins job that clones a repository and executes a shell script.

## Files
- `hello-world.sh` - Shell script that prints "Hello, Jenkins!"
- `Jenkinsfile` - Pipeline definition for Jenkins

## Solution Steps

### Step 1: Create hello-world.sh
The script is already created in this directory. It outputs:
- "Hello, Jenkins!"
- Current date and time
- Hostname and username

### Step 2: Push to GitHub Repository
```bash
git add hello-world.sh
git commit -m "Add hello-world.sh"
git push origin main
```

### Step 3: Create Jenkins Job (via Jenkins UI)
1. Go to Jenkins Dashboard → **New Item**
2. Enter name: `HelloWorld-Job`
3. Select **Freestyle project** → Click **OK**
4. Under **Source Code Management**:
   - Select **Git**
   - Repository URL: `https://github.com/Vatsa285/DevOPS.git`
   - Branch: `*/main`
5. Under **Build Steps**:
   - Add **Execute Shell**:
     ```bash
     chmod +x Exercises/Ex8-Jenkins-Hello-World/hello-world.sh
     ./Exercises/Ex8-Jenkins-Hello-World/hello-world.sh
     ```
6. Click **Save**

### Step 4: Run the Job
1. Click **Build Now**
2. Click on the build number → **Console Output**
3. Verify output shows "Hello, Jenkins!"

### Alternative: Using Pipeline Job
1. Go to Jenkins Dashboard → **New Item**
2. Enter name: `HelloWorld-Pipeline`
3. Select **Pipeline** → Click **OK**
4. Under **Pipeline**:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/Vatsa285/DevOPS.git`
   - Script Path: `Exercises/Ex8-Jenkins-Hello-World/Jenkinsfile`
5. Click **Save** → **Build Now**

## Expected Console Output
```
Hello, Jenkins!
Build executed at: Thu Oct 16 15:00:00 IST 2026
Running on: jenkins-server
User: jenkins
```

## Key Learnings
- **Freestyle projects** are simple Jenkins jobs with GUI configuration
- **Pipeline projects** use Jenkinsfile for Pipeline-as-Code
- Jenkins can clone Git repositories and execute shell scripts
- **Personal Access Tokens** are used for Git authentication in Jenkins
