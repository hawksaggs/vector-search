from google import genai
from google.genai import types
from dotenv import load_dotenv
from services import search_documents  # This should be your implementation of the retrieval function
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain Quantum Computing in one simple sentence."
)

print(response)

def build_context(docs):
    """
    Formats retrieved documents into a numbered context block
    for the LLM prompt. Each entry includes the title and content
    """
    contexts = []
    for i, doc in enumerate(docs, 1):
        contexts.append(f"[{i}] {doc['title']}\n{doc['content']}")
    return "\n\n".join(contexts)

def build_prompt(question, context):
    """
    Constructs the final prompt for the LLM, combining the question
    with the retrieved context. The prompt instructs the model to use
    the provided information to answer the question.
    """
    
    return f"""You are a helpful assistant. Answer the question using ONLY
            the context documents provided below. If the context does not contain
            enough information to answer, say so clearly.

            Context:
            {context}

            Question: {question}

            Answer:"""
            
def rag(question: str, top_k: int = 3) -> str:
    """
    Main function to perform Retrieval-Augmented Generation (RAG).
    It retrieves relevant documents based on the question, builds the
    context and prompt, and then generates an answer using the LLM.
    """
    # Step 1: Retrieve relevant documents
    docs = search_documents(question, top_k)  # This function should implement your retrieval logic
    
    if not docs:
        return {
            "question": question,
            "answer": "No relevant documents found in the knowledge base.",
            "sources": [],
        }
    

    # Step 2: Build context from retrieved documents
    context = build_context(docs)

    # Step 3: Build the prompt for the LLM
    prompt = build_prompt(question, context)

    # Step 4: Generate answer using the LLM
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config = types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=1024
        )
    )
    
    answer = response.text.strip()
    
    # Step 5 — Build structured response
    sources = [
        {
            "title": doc["title"],
            "score": round(doc["score"], 4),
            "content": doc["content"],
        }
        for doc in docs
    ]

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
         "usage": {
            "input_tokens": response.usage_metadata.prompt_token_count,
            "output_tokens": response.usage_metadata.candidates_token_count,
            "total_tokens": response.usage_metadata.total_token_count,
        }
    }