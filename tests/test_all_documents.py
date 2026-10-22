from document_loader import extract_pdf_text
from text_chunker import create_chunks
from embedding_model import load_embedding_model, create_embeddings
from vector_store import create_vector_store
from rag_pipeline import generate_answer


# List all the PDF documents
pdf_files = [
    "cnn.pdf",
    "LLM_notes.pdf",
    "prompt_engineering.pdf"
]

all_chunks = []

# Extract and split every PDF
for file_name in pdf_files:

    file_path = f"documents/{file_name}"

    pages = extract_pdf_text(file_path)

    chunks = create_chunks(pages, file_name)

    all_chunks.extend(chunks)

    print(
        f"{file_name}: "
        f"{len(pages)} pages, "
        f"{len(chunks)} chunks"
    )


# Load the embedding model
model = load_embedding_model()

# Convert all chunks into embeddings
embeddings = create_embeddings(
    all_chunks,
    model
)

# Store all embeddings in one FAISS index
index = create_vector_store(embeddings)

print("\nAll documents processed.")
print("Total chunks:", len(all_chunks))
print("Vectors stored:", index.ntotal)


# Ask a question about the uploaded notes
question = "What is prompt engineering?"

result = generate_answer(
    question,
    model,
    index,
    all_chunks
)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(result["answer"])

print("\nSOURCES:")

for source in result["sources"]:
    print(
        f"- {source['source']}, "
        f"page {source['page']}"
    )