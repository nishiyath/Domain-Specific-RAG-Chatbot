from document_loader import extract_pdf_text

# List the PDF files we want to test
pdf_files = [
    "documents/cnn.pdf",
    "documents/LLM_notes.pdf",
    "documents/prompt_engineering.pdf"
]

# Test each PDF separately
for pdf_file in pdf_files:

    print("\n" + "=" * 60)
    print("FILE:", pdf_file)
    print("=" * 60)

    # Extract text while preserving page numbers
    pages = extract_pdf_text(pdf_file)

    print("Pages containing extractable text:", len(pages))

    # Display the first page containing text
    if pages:
        print("\nFirst extracted page number:", pages[0]["page"])
        print("\nExtracted text preview:")
        print(pages[0]["text"][:500])

    else:
        print("No extractable text found in this PDF.")