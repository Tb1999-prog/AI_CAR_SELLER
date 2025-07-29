import pandas as pd
import faiss
import numpy as np
import pickle
import os
import json
import config
import time


def row_to_text(row):
    return f"{row['title']} {row['year']} {row['brand']} {row['model']}, {row['comndition']}, {row['price']}. Features: {row['description']}"


def get_embedding(text: str):
    result = config.client.models.embed_content(
        model="models/embedding-001",
        contents=text)
 
    return result.embeddings[0].values


def populate_faiss_from_json(json_path=config.data_path):
    with open(json_path, "r") as f:
        json_data = json.load(f)
    df = pd.DataFrame(json_data)

    docs = [row_to_text(row) for _, row in df.iterrows()]
    embeddings = np.array([get_embedding(doc) for doc in docs]).astype('float32')
    print(embeddings)
    # Create FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, config.EMBED_PATH)
    with open(config.META_PATH, 'wb') as f:
        pickle.dump(list(zip(docs, df.to_dict(orient='records'))), f)

    print("✅ FAISS index built from JSON data.")


def search_cars(query, top_k=3):
    if not os.path.exists(config.EMBED_PATH) or not os.path.exists(config.META_PATH):
        raise RuntimeError("FAISS index or metadata not found. Run populate_faiss() first.")

    # Load FAISS and metadata
    index = faiss.read_index(config.EMBED_PATH)
    with open(config.META_PATH, 'rb') as f:
        metadata = pickle.load(f)

    query_embedding = np.array([get_embedding(query)]).astype('float32')
    _, I = index.search(query_embedding, top_k)

    results = []
    for idx in I[0]:
        doc, meta = metadata[idx]
        results.append((doc, meta))
    return results
