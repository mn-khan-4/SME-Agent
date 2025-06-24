# rag/retriever.py

import os
import sys
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Ensure correct path resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import INDEX_PATH


# Load FAISS index and metadata
def load_index_and_metadata():
    if not os.path.exists(INDEX_PATH):
        raise FileNotFoundError(f"FAISS index not found at {INDEX_PATH}")
    
    print("Loading FAISS index and metadata...")
    index = faiss.read_index(INDEX_PATH)
    with open(INDEX_PATH + ".meta.pkl", "rb") as f:
        metadata = pickle.load(f)
    
    return index, metadata


# Perform a semantic search
def retrieve_relevant_docs(query, top_k=3):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    index, metadata = load_index_and_metadata()

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    D, I = index.search(query_embedding, top_k)
    results = []

    for i in I[0]:
        if i < len(metadata):
            results.append(metadata[i])
    
    return results


# Example run (test)
if __name__ == "__main__":
    query = input("Enter your query: ")
    results = retrieve_relevant_docs(query)
    print("\nTop matching documents/templates:")
    for r in results:
        print(r)