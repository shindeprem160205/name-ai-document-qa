import faiss
import numpy as np
import pickle


def create_vector_store(embeddings):
    vectors = np.array(embeddings).astype("float32")

    dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(vectors)

    return index


def save_vector_store(index, path):
    faiss.write_index(index, path)


def load_vector_store(path):
    return faiss.read_index(path)


def save_chunks(chunks, path):
    with open(path, "wb") as file:
        pickle.dump(chunks, file)


def load_chunks(path):
    with open(path, "rb") as file:
        return pickle.load(file)


def search_vector_store(index, query, model, chunks, k=3):
    query_vector = model.encode([query])
    query_vector = np.array(query_vector).astype("float32")

    distances, indices = index.search(query_vector, k)

    results = [chunks[i] for i in indices[0]]

    return results