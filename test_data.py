from db import client
from services import index_document, search_documents
import json

with open("data.json", "r") as f:
    data = json.load(f)

DOCUMENTS = data["DOCUMENTS"]
QUERIES = data["QUERIES"]

# ── Runner ────────────────────────────────────────────────────────────────────

def seed():
    print(f"\n── Seeding {len(DOCUMENTS)} documents ──")
    client.vector_search_db.documents.delete_many({})        # clear existing
    for i, doc in enumerate(DOCUMENTS, 1):
        index_document(doc["title"], doc["content"])
        print(f"  [{i:02d}/50] indexed: {doc['title']}")
    print(f"\n✓ {len(DOCUMENTS)} documents indexed\n")


def run_queries():
    print("── Running semantic search queries ──\n")
    passed = 0

    for i, q in enumerate(QUERIES, 1):
        results = search_documents(q["query"], top_k=3)

        top_title = results[0]["title"] if results else "—"
        top_score = results[0]["score"] if results else 0
        hit = top_title == q["expect"]
        passed += hit

        status = "✓" if hit else "✗"
        print(f"[{i:02d}] {status}  Query : {q['query']}")
        print(f"       Expect: {q['expect']}")
        print(f"       Got   : {top_title}  (score: {top_score:.4f})")
        if not hit and len(results) > 1:
            others = [r["title"] for r in results[1:]]
            print(f"       Also  : {', '.join(others)}")
        print()

    print(f"── Results: {passed}/{len(QUERIES)} passed ──\n")


if __name__ == "__main__":
    client.admin.command("ping")
    print("✓ Connected to MongoDB Atlas")

    seed()
    run_queries()

    client.close()