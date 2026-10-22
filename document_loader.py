from pypdf import PdfReader


def extract_pdf_text(file_path):
    # Open the PDF document
    reader = PdfReader(file_path)

    # Store the extracted text and page numbers
    pages = []

    # Read each page separately
    for page_number, page in enumerate(reader.pages, start=1):

        # Extract text from the current page
        page_text = page.extract_text()

        # Skip pages without extractable text
        if page_text and page_text.strip():

            pages.append({
                "page": page_number,
                "text": page_text
            })

    return pages
