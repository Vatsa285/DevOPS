FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY fine_tune.py .

# Download and cache the pre-trained model at build time
RUN python -c "from transformers import AutoModelForTokenClassification, AutoTokenizer; \
    m='dbmdz/bert-large-cased-finetuned-conll03-english'; \
    AutoTokenizer.from_pretrained(m); \
    AutoModelForTokenClassification.from_pretrained(m)"

# Expose port
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
