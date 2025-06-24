import os
import sys
import json
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# ✅ Ensure we can import from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(_file_), '..')))

# ✅ Import all needed paths
from config import (
    TEMPLATE_DIR,
    DOCS_PATH,
    INDEX_PATH,
    HR_TEMPLATES_DIR,
    HR_EMPLOYEE_DATA_PATH
)

def load_templates():
    print("🔄 Loading Admin templates...")
    texts = []
    metadata = []
    for fname in os.listdir(TEMPLATE_DIR):
        if fname.endswith(".txt"):
            with open(os.path.join(TEMPLATE_DIR, fname), "r", encoding="utf-8") as f:
                content = f.read()
                texts.append(content)
                metadata.append({"source": "template", "filename": fname})
    print(f"📄 Loaded {len(texts)} Admin templates")
    return texts, metadata

def load_docs():
    print("🔄 Loading Admin documents from JSON...")
    texts = []
    metadata = []
    if os.path.exists(DOCS_PATH):
        with open(DOCS_PATH, "r", encoding="utf-8") as f:
            docs = json.load(f)
            for doc in docs:
                texts.append(doc["content"])
                metadata.append({
                    "source": "doc",
                    "type": doc.get("type", "unknown"),
                    "client": doc.get("client", ""),
                    "date": doc.get("date", "")
                })
    print(f"📄 Loaded {len(texts)} Admin documents")
    return texts, metadata

# ✅ Load HR templates
def load_hr_templates():
    print("🔄 Loading HR templates...")
    texts = []
    metadata = []
    if os.path.exists(HR_TEMPLATES_DIR):
        for fname in os.listdir(HR_TEMPLATES_DIR):
            if fname.endswith(".txt"):
                with open(os.path.join(HR_TEMPLATES_DIR, fname), "r", encoding="utf-8") as f:
                    content = f.read()
                    texts.append(content)
                    metadata.append({"source": "hr_template", "filename": fname})
    print(f"📄 Loaded {len(texts)} HR templates")
    return texts, metadata

# ✅ Load HR employee records
def load_hr_docs():
    print("🔄 Loading HR employee records...")
    texts = []
    metadata = []
    if os.path.exists(HR_EMPLOYEE_DATA_PATH):
        with open(HR_EMPLOYEE_DATA_PATH, "r", encoding="utf-8") as f:
            employees = json.load(f)
            for emp in employees:
                summary = f"Employee Record: {emp['name']} ({emp['designation']} in {emp['department']})"
                texts.append(summary)
                metadata.append({
                    "source": "hr_data",
                    "type": "employee_record",
                    "employee_id": emp["employee_id"],
                    "department": emp["department"]
                })
    print(f"📄 Loaded {len(texts)} HR records")
    return texts, metadata

def create_embeddings(texts, model):
    print("✨ Generating embeddings...")
    return model.encode(texts, show_progress_bar=True)

def save_faiss_index(embeddings, metadata):
    print("💾 Saving FAISS index and metadata...")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)

    with open(INDEX_PATH + ".meta.pkl", "wb") as f:
        pickle.dump(metadata, f)

    print(f"✅ FAISS index saved at: {INDEX_PATH}")
    print(f"✅ Metadata saved at: {INDEX_PATH}.meta.pkl")

def main():
    print("🚀 Starting embedder...")
    print("🧠 Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Load all data
    texts1, meta1 = load_templates()
    texts2, meta2 = load_docs()
    texts3, meta3 = load_hr_templates()
    texts4, meta4 = load_hr_docs()

    texts = texts1 + texts2 + texts3 + texts4
    metadata = meta1 + meta2 + meta3 + meta4

    print(f"📝 Total texts to embed: {len(texts)}")
    if len(texts) == 0:
        print("❌ No text data found to embed. Exiting.")
        return

    embeddings = create_embeddings(texts, model)
    embeddings = np.array(embeddings).astype("float32")
    save_faiss_index(embeddings, metadata)
    print("🏁 Done with embedding creation.")

if __name__ == "_main_":
    main()