# Vector Search RAG (Retrieval-Augmented Generation)

A powerful Retrieval-Augmented Generation (RAG) system that combines vector search with Google's Gemini AI to answer questions based on your document collection. This project uses MongoDB for document storage, sentence transformers for embeddings, and implements semantic search capabilities.

## Features

- **Vector Search**: Semantic search using MongoDB's vector search capabilities
- **Text Embeddings**: Convert text to embeddings using Sentence Transformers
- **PDF Processing**: Extract and chunk PDF documents for indexing
- **RAG Pipeline**: Retrieve relevant documents and generate answers using Google Gemini
- **MongoDB Integration**: Persistent storage of documents and embeddings
- **Configurable Search**: Adjustable number of results and chunk sizes
- **Test Infrastructure**: Built-in test data and test cases

## Project Structure

```
.
├── main.py              # Entry point for running searches
├── db.py               # MongoDB client initialization
├── embedding.py        # Text embedding using Sentence Transformers
├── services.py         # Document indexing and search functionality
├── rag.py              # RAG pipeline with Gemini integration
├── pdf_loader.py       # PDF extraction and text chunking
├── test_data.py        # Test data utilities
├── test_rag.py         # RAG testing suite
├── requirements.txt    # Python dependencies
├── env.example         # Environment variables template
└── .gitignore          # Git ignore rules
```

## Technology Stack

- **Database**: MongoDB (with vector search capability)
- **Embeddings**: Sentence Transformers (`all-MiniLM-L6-v2`)
- **LLM**: Google Gemini 2.5 Flash
- **PDF Processing**: PyPDF
- **Backend**: Python with Typer CLI framework

## Prerequisites

- Python 3.8+
- MongoDB instance with vector search enabled
- Google Gemini API key
- pip package manager

## Installation

1. **Clone the repository** (or navigate to the project directory)
   ```bash
   cd vector-search
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Copy the environment template**
   ```bash
   cp env.example .env
   ```

2. **Set up environment variables in `.env`**
   ```
   MONGO_URL=mongodb://localhost:27017/
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

   - **MONGO_URL**: Connection string to your MongoDB instance
   - **GEMINI_API_KEY**: Your Google Gemini API key (get it from [Google AI Studio](https://aistudio.google.com/))

3. **Ensure MongoDB Vector Search is enabled**
   - Your MongoDB instance must have vector search capability enabled
   - Create a vector search index on the `documents` collection with the `embedding` field

## Running the Project

### Basic Usage

Run the main script to test document indexing and searching:

```bash
python main.py
```

This will:
1. Connect to MongoDB
2. Load test data from `data.json`
3. Perform vector search on queries
4. Display results

### Using the RAG Pipeline

To use the full RAG functionality with Gemini:

```python
from rag import rag

result = rag("Your question here", top_k=3)
print(result)
```

This returns a structured response with:
- The original question
- Generated answer from Gemini
- Retrieved sources with similarity scores
- Token usage information

### Indexing PDF Documents

To index PDF documents:

```python
from services import index_pdf

# Index a PDF file
index_pdf("your_document.pdf", chunk_size=500, overlap=50)
```

### Searching Documents

```python
from services import search_documents

# Search for relevant documents
results = search_documents("Your search query", top_k=5)
for doc in results:
    print(f"Title: {doc['title']}")
    print(f"Score: {doc['score']}")
    print(f"Content: {doc['content'][:200]}...")
```

## API Reference

### `embedding.py`

- **`embed_text(text)`**: Converts text to a vector embedding
  - Returns: List of floats (embedding vector)

### `services.py`

- **`index_document(title, content)`**: Index a document with its embedding
  - Returns: MongoDB document ID

- **`search_documents(query, top_k=5)`**: Search for similar documents
  - Returns: List of documents with scores

- **`index_pdf(file_path, chunk_size=500, overlap=50)`**: Index a PDF file
  - Automatically extracts and chunks text

### `rag.py`

- **`rag(question, top_k=3)`**: Full RAG pipeline
  - Returns: Dictionary with question, answer, sources, and token usage

- **`build_context(docs)`**: Format documents for LLM

- **`build_prompt(question, context)`**: Build the LLM prompt

## Testing

Run the test suite:

```bash
python test_rag.py
```

Test data is provided in `test_data.py` with sample documents and queries.

## Configuration Options

### Embedding Model

In `embedding.py`, you can switch embedding models:

```python
# Current (lightweight)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Larger, more accurate model (requires more memory)
# model = SentenceTransformer('all-mpnet-base-v2')
```

### Search Parameters

- `top_k`: Number of documents to retrieve (default: 5)
- `chunk_size`: Size of text chunks in PDF processing (default: 500)
- `overlap`: Overlap between chunks (default: 50)

### Gemini Configuration

In `rag.py`, adjust these parameters:
- `temperature`: Controls randomness (0.0-1.0, default: 0.2)
- `max_output_tokens`: Maximum response length (default: 1024)
- `model`: Gemini model version (default: gemini-2.5-flash)

## Troubleshooting

### MongoDB Connection Error
- Verify `MONGO_URL` is correct
- Ensure MongoDB service is running
- Check network connectivity

### API Key Issues
- Verify `GEMINI_API_KEY` is valid
- Check you haven't exceeded API rate limits
- Ensure API key has necessary permissions

### Vector Search Not Working
- Confirm MongoDB vector search is enabled on your instance
- Verify the vector index is created on the `documents` collection
- Check that embeddings are properly stored

### Out of Memory
- Use a smaller embedding model (all-MiniLM-L6-v2 is lightweight)
- Reduce `chunk_size` for PDF processing
- Process PDFs in batches instead of all at once

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this project for your needs.

## Support

For questions or issues, please open an issue on the repository.
