from google import genai
import pandas as pd
import faiss
import numpy as np
import pickle
import os
import json

client = genai.Client(api_key="AIzaSyC6_BxvOzwB24K2tj7c70CHr220kpnswjY")
data_path = "data/vehicle_inventory.json"
EMBED_PATH = "data/faiss_index.index"
META_PATH = "data/faiss_metadata.pkl"
# with open(data_path) as f:
#     data = json.load(f)

def row_to_text(row):
    return f"{row['title']} {row['year']} {row['brand']} {row['model']}, {row['comndition']}, {row['price']}. Features: {row['description']}"


def get_embedding(text: str):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text)
    # print(result.embeddings[0].values)
    return result.embeddings[0].values


def populate_faiss_from_json(json_path=data_path):
    with open(json_path, "r") as f:
        json_data = json.load(f)
    df = pd.DataFrame(json_data)

    docs = [row_to_text(row) for _, row in df.iterrows()]
    print("ss")
    embeddings = np.array([get_embedding(doc) for doc in docs]).astype('float32')
    print(embeddings)
    # Create FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    print("index")
    index.add(embeddings)
    faiss.write_index(index, EMBED_PATH)
    with open(META_PATH, 'wb') as f:
        pickle.dump(list(zip(docs, df.to_dict(orient='records'))), f)

    print("✅ FAISS index built from JSON data.")


def search_cars(query, top_k=3):
    if not os.path.exists(EMBED_PATH) or not os.path.exists(META_PATH):
        raise RuntimeError("FAISS index or metadata not found. Run populate_faiss() first.")

    # Load FAISS and metadata
    index = faiss.read_index(EMBED_PATH)
    with open(META_PATH, 'rb') as f:
        metadata = pickle.load(f)

    query_embedding = np.array([get_embedding(query)]).astype('float32')
    D, I = index.search(query_embedding, top_k)

    results = []
    for idx in I[0]:
        doc, meta = metadata[idx]
        results.append((doc, meta))
    return results


# --- Test Flow ---
if __name__ == "__main__":
    if not os.path.exists(EMBED_PATH) or not os.path.exists(META_PATH):
        populate_faiss()

    query = input("What kind of car are you looking for? ")
    results = search_cars(query)

    print("\n🔍 Top Matches:")
    for doc, meta in results:
        print(f"✅ {doc}")
        print(f"ℹ  Metadata: {meta}")
        print("---")
