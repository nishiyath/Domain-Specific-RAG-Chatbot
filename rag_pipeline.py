import os

from groq import Groq
from dotenv import load_dotenv

from prompt import SYSTEM_PROMPT
from vector_store import search_similar_chunks


# Load the API key from the .env file
load_dotenv()


def generate_answer(question, model, index, chunks, top_k=3):

    # Find the most relevant document chunks
    results = search_similar_chunks(
        question,
        model,
        index,
        chunks,
        top_k=top_k
    )

    # Return the fallback if there are no results
    if not results:
        return {
            "answer": (
                "I could not find this information "
                "in the uploaded documents."
            ),
            "sources": []
        }

    # Prepare the retrieved text as context
    context_parts = []

    for result in results:
        context_parts.append(
            f"Source: {result['source']}\n"
            f"Page: {result['page']}\n"
            f"Text: {result['text']}"
        )

    context = "\n\n".join(context_parts)

    # Read the Groq API key
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Check your .env file."
        )

    # Connect to Groq
    client = Groq(api_key=api_key)

    # Generate an answer using the retrieved context
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": (
                    f"Document context:\n{context}\n\n"
                    f"Question: {question}"
                )
            }
        ],
        temperature=0.1
    )

    # Extract the answer
    answer = response.choices[0].message.content

    # Check whether the fallback message was returned
    fallback = (
        "I could not find this information "
        "in the uploaded documents."
    )

    # Do not display sources for unavailable answers
    if fallback.lower() in answer.lower():
        sources = []

    else:
        sources = [
            {
                "source": result["source"],
                "page": result["page"],
                "score": result["score"]
            }
            for result in results
        ]

    # Return the answer and source information
    return {
        "answer": answer,
        "sources": sources
    }