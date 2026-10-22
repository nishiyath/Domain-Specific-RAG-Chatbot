import faiss
import numpy as np


def create_vector_store(embeddings):

    # Convert embeddings into a NumPy array
    vectors = np.array(embeddings, dtype="float32")

    # Normalize vectors for cosine similarity
    faiss.normalize_L2(vectors)

    # Get the number of values in each embedding
    embedding_size = vectors.shape[1]

    # Create a FAISS index using inner product
    index = faiss.IndexFlatIP(embedding_size)

    # Store the embeddings in the index
    index.add(vectors)

    return index


def search_similar_chunks(question, model, index, chunks, top_k=3):

    # Convert the question into an embedding
    question_embedding = model.encode(
        [question],
        convert_to_numpy=True
    )

    # Convert the question embedding to float32
    question_embedding = np.array(
        question_embedding,
        dtype="float32"
    )

    # Normalize the question embedding
    faiss.normalize_L2(question_embedding)

    # Search for the most similar chunks
    scores, positions = index.search(question_embedding, top_k)

    # Collect the matching chunks and their scores
    results = []

    for score, position in zip(scores[0], positions[0]):

        # Ignore invalid search positions
        if position == -1:
            continue

        results.append({
            "text": chunks[position]["text"],
            "source": chunks[position]["source"],
            "page": chunks[position]["page"],
            "score": float(score)
        })

    return results
