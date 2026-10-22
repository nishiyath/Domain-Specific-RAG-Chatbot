import streamlit as st

from document_loader import extract_pdf_text
from text_chunker import create_chunks
from embedding_model import load_embedding_model, create_embeddings
from vector_store import create_vector_store
from rag_pipeline import generate_answer


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="📚",
    layout="wide"
)

st.title("📚 RAG Chatbot")

st.write(
    "Upload your PDF notes, process them, "
    "and ask questions based on their content."
)


# --------------------------------------------------
# SIDEBAR: PDF UPLOAD
# --------------------------------------------------

st.sidebar.header("Upload Your Notes")

uploaded_files = st.sidebar.file_uploader(
    "Choose PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    st.sidebar.write("Selected documents:")

    for uploaded_file in uploaded_files:
        st.sidebar.write(f"- {uploaded_file.name}")


# --------------------------------------------------
# PROCESS DOCUMENTS
# --------------------------------------------------

if st.sidebar.button("Process Documents"):

    if not uploaded_files:
        st.sidebar.warning("Please upload at least one PDF.")

    else:
        try:
            with st.spinner(
                "Reading documents and building the search index..."
            ):

                all_chunks = []

                # Extract text and create chunks from each PDF
                for uploaded_file in uploaded_files:

                    pages = extract_pdf_text(uploaded_file)

                    chunks = create_chunks(
                        pages,
                        uploaded_file.name
                    )

                    all_chunks.extend(chunks)

                if not all_chunks:
                    st.error(
                        "No extractable text was found. "
                        "Please try a text-based PDF."
                    )

                else:
                    # Load the embedding model
                    model = load_embedding_model()

                    # Create embeddings for all chunks
                    embeddings = create_embeddings(
                        all_chunks,
                        model
                    )

                    # Create the FAISS index
                    index = create_vector_store(embeddings)

                    # Store the processed data in Streamlit session state
                    st.session_state["chunks"] = all_chunks
                    st.session_state["model"] = model
                    st.session_state["index"] = index

                    # Start a fresh chat for the new documents
                    st.session_state["messages"] = []

                    st.sidebar.success(
                        f"Processed {len(uploaded_files)} PDF(s)."
                    )

                    st.success(
                        f"Processing complete! "
                        f"{len(all_chunks)} text chunks are ready."
                    )

        except Exception as error:
            st.error(
                "Document processing failed. "
                "Please check your PDF files and try again."
            )

            st.exception(error)


# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Display sources for assistant answers
        if message["role"] == "assistant" and message.get("sources"):

            with st.expander("View source documents"):
                for source in message["sources"]:
                    st.write(
                        f"- {source['source']}, "
                        f"page {source['page']}"
                    )


# --------------------------------------------------
# QUESTION INPUT
# --------------------------------------------------

if (
    "chunks" in st.session_state
    and "model" in st.session_state
    and "index" in st.session_state
):

    question = st.chat_input(
        "Ask a question about your notes..."
    )

    if question:

        # Display the user's question
        st.session_state["messages"].append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        # Generate an answer using the RAG pipeline
        with st.chat_message("assistant"):

            with st.spinner("Searching your notes..."):

                try:
                    result = generate_answer(
                        question,
                        st.session_state["model"],
                        st.session_state["index"],
                        st.session_state["chunks"]
                    )

                    answer = result["answer"]
                    sources = result["sources"]

                    st.markdown(answer)

                    # Display source document and page numbers
                    if sources:
                        with st.expander("View source documents"):
                            for source in sources:
                                st.write(
                                    f"- {source['source']}, "
                                    f"page {source['page']}"
                                )

                    # Save the answer and sources in chat history
                    st.session_state["messages"].append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })

                except Exception as error:
                    st.error(
                        "I could not generate an answer. "
                        "Please check the API configuration and try again."
                    )

                    st.exception(error)

else:
    st.info(
        "Upload your PDF notes in the sidebar and click "
        "'Process Documents' to start chatting."
    )


# --------------------------------------------------
# CLEAR CHAT
# --------------------------------------------------

if st.sidebar.button("Clear Chat"):
    st.session_state["messages"] = []
    st.rerun()
