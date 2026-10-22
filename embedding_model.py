from sentence_transformers import SentenceTransformer


# Load the pretrained embedding model
def load_embedding_model():

    model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


# Convert text chunks into numerical embeddings
def create_embeddings(chunks, model):

    # Extract the text from each chunk
    texts = [chunk["text"] for chunk in chunks]

    # Convert the text into numerical vectors
    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    return embeddings
