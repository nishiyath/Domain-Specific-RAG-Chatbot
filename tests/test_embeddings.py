from document_loader import extract_pdf_text
from text_chunker import create_chunks
from embedding_model import load_embedding_model, create_embeddings


# Step 1: Extract text from the PDF
pages = extract_pdf_text("documents/cnn.pdf")

# Step 2: Divide the text into chunks
chunks = create_chunks(pages, "cnn.pdf")

print("Total chunks:", len(chunks))


# Step 3: Load the embedding model
print("\nLoading embedding model...")
model = load_embedding_model()


# Step 4: Convert chunks into embeddings
embeddings = create_embeddings(chunks, model)


# Step 5: Display the result
print("\nEmbeddings created successfully!")
print("Number of embeddings:", len(embeddings))
print("Numbers in the first embedding:", len(embeddings[0]))
print("\nFirst few numbers:")
print(embeddings[0][:5])
