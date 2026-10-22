
from document_loader import extract_pdf_text
from text_chunker import create_chunks
from embedding_model import load_embedding_model, create_embeddings
from vector_store import create_vector_store, search_similar_chunks


# Step 1: Extract and split the CNN notes
pages = extract_pdf_text("documents/cnn.pdf")
chunks = create_chunks(pages, "cnn.pdf")

# Step 2: Load the embedding model
model = load_embedding_model()

# Step 3: Convert the chunks into embeddings
embeddings = create_embeddings(chunks, model)

# Step 4: Store the embeddings in FAISS
index = create_vector_store(embeddings)

print("FAISS index created successfully!")
print("Number of vectors stored:", index.ntotal)


# Step 5: Ask a question
question = "What is a CNN and what is it used for?"

results = search_similar_chunks(
    question,
    model,
    index,
    chunks,
    top_k=3
)

# Step 6: Display the retrieved information
print("\nQuestion:", question)

for number, result in enumerate(results, start=1):

    print(f"\nResult {number}")
    print("Source:", result["source"])
    print("Page:", result["page"])
    print("Similarity score:", round(result["score"], 3))
    print("Text:", result["text"][:300])
