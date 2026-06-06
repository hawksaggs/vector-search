from db import client as mongo_client
from rag import rag

RAG_QUERIES = [
    # Python
    {
        "question": "What are two ways Python helps you write less repetitive code?",
        "expect_sources": ["Python Decorators", "Python Dataclasses"],
    },
    {
        "question": "How can I handle large data without running out of memory in Python?",
        "expect_sources": ["Python Generators"],
    },
    {
        "question": "How does Python handle errors without crashing the program?",
        "expect_sources": ["Python Exception Handling"],
    },

    # MongoDB
    {
        "question": "How do I make MongoDB queries faster?",
        "expect_sources": ["MongoDB Indexes"],
    },
    {
        "question": "How does MongoDB support high availability?",
        "expect_sources": ["MongoDB Replica Sets"],
    },
    {
        "question": "How do I automatically clean up old session data in MongoDB?",
        "expect_sources": ["MongoDB TTL Indexes"],
    },

    # Vector DB / RAG
    {
        "question": "How does semantic search differ from regular keyword search?",
        "expect_sources": ["Semantic Search vs Keyword Search"],
    },
    {
        "question": "What is RAG and why is it useful for LLM applications?",
        "expect_sources": ["RAG Architecture"],
    },
    {
        "question": "How do I improve retrieval quality by combining vector and keyword search?",
        "expect_sources": ["Hybrid Search"],
    },

    # System Design
    {
        "question": "How do microservices handle transactions that span multiple services?",
        "expect_sources": ["Saga Pattern"],
    },
    {
        "question": "What pattern helps prevent cascading failures in distributed systems?",
        "expect_sources": ["Circuit Breaker Pattern"],
    },
    {
        "question": "How can I scale reads and writes independently in my system?",
        "expect_sources": ["CQRS Pattern"],
    },

    # ML
    {
        "question": "How do I use a pretrained model without training from scratch?",
        "expect_sources": ["Transfer Learning"],
    },
    {
        "question": "Why does my model perform well on training data but fail on new data?",
        "expect_sources": ["Overfitting and Regularization"],
    },
    {
        "question": "How does a transformer model know which words to focus on?",
        "expect_sources": ["Attention Mechanism"],
    },
]


def run_rag_tests():
    print("── Running RAG test queries (Gemini) ──\n")
    passed    = 0
    total_in  = 0
    total_out = 0

    for i, q in enumerate(RAG_QUERIES, 1):
        result = rag(q["question"], top_k=3)

        source_titles = [s["title"] for s in result["sources"]]
        expected      = q["expect_sources"]
        sources_hit   = all(e in source_titles for e in expected)
        passed       += sources_hit

        total_in  += result["usage"]["input_tokens"]
        total_out += result["usage"]["output_tokens"]

        status = "✓" if sources_hit else "✗"
        print(f"[{i:02d}] {status}  Q: {result['question']}")
        print(f"       A: {result['answer'][:160]}{'...' if len(result['answer']) > 160 else ''}")
        print(f"       Sources retrieved : {source_titles}")
        print(f"       Sources expected  : {expected}")
        print(f"       Tokens — in: {result['usage']['input_tokens']}  out: {result['usage']['output_tokens']}")
        print()

    print(f"── Results      : {passed}/{len(RAG_QUERIES)} passed")
    print(f"── Total tokens — input: {total_in}  output: {total_out}\n")


if __name__ == "__main__":
    mongo_client.admin.command("ping")
    print("✓ Connected to MongoDB Atlas\n")

    run_rag_tests()

    mongo_client.close()