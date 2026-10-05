# Exercise 9: Jenkins Multi-Stage Pipeline

## Objective
Create and execute a Jenkins Pipeline with multiple stages: **Build**, **Test**, and **Deploy** for a Python Flask application.

## Scenario
Automate the CI/CD pipeline for a Python Flask application with:
1. **Build** - Install dependencies
2. **Test** - Run unit tests
3. **Deploy** - Copy application to deployment directory
4. **Run** - Verify application starts

## Files
- `app.py` - Flask application
- `requirements.txt` - Python dependencies
- `test_app.py` - Unit tests
- `Jenkinsfile` - Multi-stage pipeline definition

## Solution Steps

### Step 1: Set Up Jenkins
1. Ensure Jenkins is running
2. Install the **Pipeline Plugin** (if not already installed)

### Step 2: Push Code to GitHub
```bash
git add .
git commit -m "Add multi-stage pipeline exercise"
git push origin main
```

### Step 3: Create Jenkins Pipeline Job
1. Go to Jenkins Dashboard → **New Item**
2. Name: `Python-MultiStage-Pipeline`
3. Select **Pipeline** → Click **OK**
4. Under **Pipeline**:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/Vatsa285/DevOPS.git`
   - Script Path: `Exercises/Ex9-Jenkins-Multi-Stage-Pipeline/Jenkinsfile`
5. Click **Save**

### Step 4: Run the Pipeline
1. Click **Build Now**
2. Watch the **Stage View** to see each stage execute
3. Click on build → **Console Output** for details

### Expected Stage View
```
Build → Test → Deploy → Run Application
  ✓       ✓       ✓          ✓
```

### Expected Console Output
```
[Pipeline] stage (Build)
Creating virtual environment and installing dependencies...
Successfully installed flask-2.1.2

[Pipeline] stage (Test)
Running tests...
Hello, Jenkins Multi-Stage Pipeline!
.
----------------------------------------------------------------------
Ran 1 test in 0.005s
OK

[Pipeline] stage (Deploy)
Deploying application...

[Pipeline] stage (Run Application)
Starting application (test run)...
 * Serving Flask app 'app'
```

## Run Tests Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python -m unittest test_app.py -v

# Run app
python app.py
```

## Key Learnings
- **Multi-stage pipelines** break CI/CD into discrete phases
- **Jenkinsfile** defines the pipeline as code (declarative syntax)
- **Post actions** handle success/failure notifications
- Each stage can have its own configuration and error handling
