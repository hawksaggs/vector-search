from db import client
from embedding import embed_text
from pdf_loader import chunk_text, extract_text_from_pdf

def index_document(title, content):
    embedding = embed_text(content)
    document = {
        "title": title,
        "content": content,
        "embedding": embedding
    }
    result = client.vector_search_db.documents.insert_one(document)
    return result.inserted_id

def search_documents(query, top_k=5):
    query_embed = embed_text(query)
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embed,
                "limit": top_k,
                "numCandidates": top_k * 10
            }
        },
        {
            "$project": {
                "_id": 1,
                "title": 1,
                "content": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]

    results = []
    for doc in client.vector_search_db.documents.aggregate(pipeline):
        doc["id"] = str(doc.pop("_id"))
        results.append(doc)

    return results

def index_pdf(file_path: str, chunk_size: int = 500, overlap: int = 50):
    
    extracted_text = extract_text_from_pdf(file_path)
    chunks = chunk_text(extracted_text, chunk_size, overlap)
    
    for i, chunk in enumerate(chunks, 1):
        title = f"{file_path} - Chunk {i}"
        index_document(title, chunk)