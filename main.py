from db import client
from embedding import embed_text
from services import index_document, search_documents
import json

def load_json():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data

def load_data(data):
    for doc in data["DOCUMENTS"]:
        doc_id = index_document(doc["title"], doc["content"])
        print("Document indexed with ID:", doc_id)

def main():
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
    # embedding = embed_text("Hello, my dog is cute")
    # print("Embedding:", embedding)
    data = load_json()
    # load_data(data)
    for query in data["QUERIES"]:
        print("Query:", query["query"])
        results = search_documents(query["query"])
        print("Search Results:", results)
        print("Expected Result:", query["expect"])

if __name__ == "__main__":
    main()