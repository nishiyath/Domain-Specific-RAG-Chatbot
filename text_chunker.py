
from langchain_text_splitters import RecursiveCharacterTextSplitter
from text_cleaner import clean_text


def create_chunks(pages, file_name):

    # Divide text into chunks of 800 characters
    # Keep 120 characters from the previous chunk
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120
    )

    all_chunks = []

    # Process each page separately to preserve its page number
    for page in pages:

        # Clean the extracted page text
        cleaned_text = clean_text(page["text"])

        # Split the cleaned text into smaller pieces
        text_chunks = splitter.split_text(cleaned_text)

        # Store each chunk with its source information
        for chunk in text_chunks:
            all_chunks.append({
                "text": chunk,
                "source": file_name,
                "page": page["page"]
            })

    return all_chunks
