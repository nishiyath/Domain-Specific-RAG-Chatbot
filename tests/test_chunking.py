
from document_loader import extract_pdf_text
from text_chunker import create_chunks

# Test using the CNN notes
file_path = "documents/cnn.pdf"

# Step 1: Extract text from the PDF
pages = extract_pdf_text(file_path)

# Step 2: Split the text into chunks
chunks = create_chunks(pages, "cnn.pdf")

# Step 3: Display the results
print("Total chunks created:", len(chunks))

print("\nFirst chunk:")
print(chunks[0]["text"])

print("\nSource:", chunks[0]["source"])
print("Page:", chunks[0]["page"])
