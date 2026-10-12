# Assignment 1: Fine-tuning and Deploying an LLM in Docker

## Objective
Fine-tune a pre-trained language model (BERT) to extract course names from text, and deploy it as a Docker container using FastAPI.

## Architecture
```
Fine-tune BERT Model → Save Model → Dockerize FastAPI Server → Deploy Container
```

## Files
- `fine_tune.py` - Script to fine-tune the BERT model on course name data
- `app.py` - FastAPI server for serving predictions via REST API
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container definition for deployment

## Solution Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Fine-tune the Model
```bash
python fine_tune.py
```
This creates a `fine_tuned_model/` directory with the trained model weights.

### Step 3: Test the API Locally
```bash
python app.py
```
Access the API docs at: http://localhost:8000/docs

### Step 4: Build Docker Image
```bash
docker build -t course-extractor:1.0 .
```

### Step 5: Run Docker Container
```bash
docker run -d --name course-extractor \
  -p 8000:8000 \
  course-extractor:1.0
```

### Step 6: Test the API
```bash
# Health check
curl http://localhost:8000/health

# Extract course names
curl -X POST http://localhost:8000/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "I am enrolled in Introduction to Computer Science and Machine Learning courses"}'
```

**Expected Response:**
```json
{
  "text": "I am enrolled in Introduction to Computer Science and Machine Learning courses",
  "entities": [...],
  "course_names": ["Computer Science", "Machine Learning"]
}
```

### Step 7: Clean Up
```bash
docker stop course-extractor
docker rm course-extractor
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info and available endpoints |
| GET | `/health` | Health check |
| POST | `/extract` | Extract course names from text |
| GET | `/docs` | Swagger UI documentation |

## Key Learnings
- **Hugging Face Transformers** provides pre-trained models for NLP tasks
- **Token Classification** (NER) identifies entities in text
- **FastAPI** provides high-performance REST API with auto-generated docs
- **Docker** packages the model + server for portable deployment
