# Domain-Specific RAG Chatbot 

## 1. Project Overview

This project is a chatbot. Users can upload PDF documents and ask questions about their contents.

The chatbot retrieves relevant text from the uploaded documents and uses a language model to generate answers. It also displays source document names and page numbers.

## 2. Project Objectives

- Extract text from PDF documents.
- Clean and split text into smaller chunks.
- Convert chunks into numerical embeddings.
- Store and search embeddings using FAISS.
- Retrieve relevant information for user questions.
- Generate answers using Groq.
- Display answers and source information in Streamlit.
- Return a fallback response when information is unavailable.

## 3. Technologies Used

- Python
- pypdf
- LangChain text splitters
- Sentence Transformers
- all-MiniLM-L6-v2
- FAISS
- Groq API
- Streamlit
- python-dotenv

## 4. Project Workflow

1. Upload PDF documents.
2. Extract text and preserve page numbers.
3. Clean the extracted text.
4. Split text into smaller chunks.
5. Generate embeddings using Sentence Transformers.
6. Store embeddings in FAISS.
7. Retrieve relevant chunks for a question.
8. Send the retrieved context and question to Groq.
9. Display the generated answer and source information.

See 'workflow_diagram.png' for the workflow diagram.

## 5. Main Features

- Upload multiple PDF documents.
- Extract text from PDF pages.
- Preserve source document names and page numbers.
- Split text into chunks with overlap.
- Generate embeddings using a pretrained model.
- Retrieve relevant chunks using FAISS.
- Generate answers using Groq.
- Display source document information.
- Provide a fallback response for unavailable information.
- Maintain chat history during the session.
- Clear the conversation.



## 6. Installation

### Create a virtual environment


python -m venv rag_env


### Activate the environment on Windows PowerShell


.\rag_env\Scripts\Activate.ps1


### Install dependencies

pip install -r requirements.txt


## 7. API Configuration

Create a `.env` file in the project folder and add your Groq API key:


GROQ_API_KEY=your_groq_api_key



## 8. Run the Application

Start the Streamlit application:


streamlit run app.py


Then open the local URL displayed in the terminal.

Upload  PDF notes, click **Process Documents**, and enter a question in the chat box.

## 9. Testing

The testing sheet is available at:

`tests/test_questions.csv`

It contains 15 test questions covering document-based answers, summaries, and questions whose answers may be unavailable in the uploaded documents.

## 10. Limitations

- The system currently processes text-based PDFs, scanned PDFs may require OCR.
- Answer quality depends on the extracted text and retrieved chunks.

## 11. Conclusion

This project shows a Retrieval-Augmented Generation (RAG) workflow for question answering over some notes. It combines PDF text extraction, chunking, embeddings, FAISS retrieval, Groq-based answer generation, and a Streamlit interface.