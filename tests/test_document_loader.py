
from io import BytesIO
from document_loader import extract_documents


class UploadedTextFile:
    """Simulate a file uploaded through Streamlit."""

    def __init__(self, name, content):
        self.name = name
        self.content = content

    def getvalue(self):
        return self.content


# Create a sample TXT file in memory
sample_file = UploadedTextFile(
    "ai_notes.txt",
    b"Artificial Intelligence is a field of computer science."
)

# Extract the uploaded file
documents = extract_documents([sample_file])

# Display the results
print("Documents extracted:", len(documents))

for document in documents:
    print("Source:", document.metadata["source"])
    print("Page:", document.metadata["page"])
    print("Text:", document.page_content)
