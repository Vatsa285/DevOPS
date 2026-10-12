"""
Assignment 1: Fine-tuning and Deploying an LLM in Docker
Fine-tuned for Course Name Extraction
"""

import pandas as pd
from transformers import AutoModelForTokenClassification, AutoTokenizer, Trainer, TrainingArguments
from datasets import Dataset

# ============================================================
# Step 1: Prepare the Dataset
# ============================================================

data = {
    "text": [
        "Introduction to Computer Science",
        "Advanced Mathematics",
        "Data Structures and Algorithms",
        "Operating Systems",
        "Machine Learning",
        "Database Management Systems",
        "Computer Networks",
        "Software Engineering",
        "Artificial Intelligence",
        "Web Development",
        "Cloud Computing",
        "Cyber Security",
        "DevOps Engineering",
        "Mobile Application Development",
        "Natural Language Processing"
    ],
    "labels": [
        ["Introduction to Computer Science"],
        ["Advanced Mathematics"],
        ["Data Structures and Algorithms"],
        ["Operating Systems"],
        ["Machine Learning"],
        ["Database Management Systems"],
        ["Computer Networks"],
        ["Software Engineering"],
        ["Artificial Intelligence"],
        ["Web Development"],
        ["Cloud Computing"],
        ["Cyber Security"],
        ["DevOps Engineering"],
        ["Mobile Application Development"],
        ["Natural Language Processing"]
    ]
}

df = pd.DataFrame(data)

# Convert to Hugging Face Dataset
dataset = Dataset.from_pandas(df)

# ============================================================
# Step 2: Load Pre-trained Model and Tokenizer
# ============================================================

model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

# ============================================================
# Step 3: Tokenize the Dataset
# ============================================================

def tokenize_function(examples):
    encoded = tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        return_offsets_mapping=True,
    )
    encoded["labels"] = []

    for offsets in encoded["offset_mapping"]:
        labels = []
        entity_started = False
        for start, end in offsets:
            if start == end:
                labels.append(-100)
            elif not entity_started:
                labels.append(1)
                entity_started = True
            else:
                labels.append(2)
        encoded["labels"].append(labels)

    encoded.pop("offset_mapping")
    return encoded

tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=dataset.column_names,
)

# ============================================================
# Step 4: Fine-tune the Model
# ============================================================

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    save_steps=10,
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=5,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

trainer.train()

# Save the fine-tuned model
model.save_pretrained("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")

print("Model saved to ./fine_tuned_model")
print("Fine-tuning complete!")
