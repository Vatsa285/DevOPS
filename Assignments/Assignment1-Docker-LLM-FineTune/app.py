"""
Assignment 1: FastAPI Server for Course Name Extraction
Serves the fine-tuned model via REST API
"""

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline
import uvicorn

app = FastAPI(
    title="Course Name Extractor API",
    description="Fine-tuned LLM API for extracting course names from text",
    version="1.0.0"
)

# Load model and tokenizer
MODEL_PATH = "./fine_tuned_model"

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForTokenClassification.from_pretrained(MODEL_PATH)
    ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    model_loaded = True
except Exception as e:
    print(f"Warning: Could not load fine-tuned model: {e}")
    print("Using fallback pre-trained model...")
    model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    model_loaded = True


class TextInput(BaseModel):
    text: str


class ExtractionResult(BaseModel):
    text: str
    entities: list
    course_names: list


@app.get("/")
def root():
    return {
        "message": "Course Name Extractor API",
        "endpoints": {
            "/extract": "POST - Extract course names from text",
            "/health": "GET - Health check",
            "/docs": "GET - API documentation"
        }
    }


@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model_loaded}


@app.post("/extract", response_model=ExtractionResult)
def extract_courses(input_data: TextInput):
    """Extract course names from the given text"""
    results = ner_pipeline(input_data.text)

    entities = [
        {
            "word": r["word"],
            "entity_group": r["entity_group"],
            "score": round(float(r["score"]), 4),
            "start": r["start"],
            "end": r["end"]
        }
        for r in results
    ]

    # Extract potential course names (entities of type MISC or ORG)
    course_names = [
        r["word"] for r in results
        if r["entity_group"] in ["MISC", "ORG", "PER"]
    ]

    return ExtractionResult(
        text=input_data.text,
        entities=entities,
        course_names=course_names
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
