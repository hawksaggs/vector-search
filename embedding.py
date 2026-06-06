from sentence_transformers import SentenceTransformer

# model = SentenceTransformer('all-mpnet-base-v2')
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text):
    embedding = model.encode(text, normalize_embeddings=True).tolist()
    return embedding