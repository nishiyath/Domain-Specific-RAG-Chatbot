from document_loader import extract_pdf_text
from text_chunker import create_chunks
from embedding_model import load_embedding_model, create_embeddings
from vector_store import create_vector_store
from rag_pipeline import generate_answer


# Step 1: Load the CNN notes
pages = extract_pdf_text("documents/cnn.pdf")

# Step 2: Divide the text into chunks
chunks = create_chunks(pages, "cnn.pdf")

print("Document loaded.")
print("Total chunks:", len(chunks))


# Step 3: Load the embedding model
model = load_embedding_model()

# Step 4: Convert chunks into embeddings
embeddings = create_embeddings(chunks, model)

# Step 5: Store embeddings in FAISS
index = create_vector_store(embeddings)

print("FAISS index ready.")


# Step 6: Ask a question
question = "Who invented the telephone?"

print("\nQuestion:", question)

# Step 7: Retrieve information and generate an answer
result = generate_answer(
    question,
    model,
    index,
    chunks
)

# Step 8: Display the answer
print("\nANSWER:")
print(result["answer"])

# Step 9: Display the sources
print("\nSOURCES:")

for source in result["sources"]:
    print(
        f"- {source['source']}, "
        f"page {source['page']}"
    )
