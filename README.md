# AI Knowledge Assistant (RAG System)

## Overview

AI Knowledge Assistant is a Retrieval-Augmented Generation (RAG) system that allows users to upload documents and ask questions using natural language.

The system retrieves relevant context from indexed documents and generates accurate, context-aware answers using LLMs.

## Problem

Organizations often store knowledge across fragmented documents, PDFs, and internal files. Searching manually is slow, repetitive, and inefficient.

## Solution

This project implements a RAG pipeline that:

1. Ingests documents
2. Splits content into semantic chunks
3. Creates embeddings
4. Stores vectors in ChromaDB
5. Retrieves relevant context
6. Generates an answer using an LLM

## Architecture

```text
User Uploads Document
        ↓
Document Loader
        ↓
Text Chunking
        ↓
Embeddings
        ↓
Vector Database
        ↓
Retriever
        ↓
LLM Response
        ↓
Answer + Sources + Cost Estimate
```

## Tech Stack

- Python
- FastAPI
- LangChain
- OpenAI API
- ChromaDB
- PyPDF
- REST API

## Features

- Upload `.txt` and `.pdf` documents
- Index documents into a vector database
- Ask natural-language questions
- Retrieve source documents
- Basic cost estimation per query
- Fallback response when context is insufficient

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/ai-knowledge-assistant-rag.git
cd ai-knowledge-assistant-rag
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env`

Copy `.env.example` to `.env` and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run the API

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Health Check

```http
GET /
```

### Upload Document

```http
POST /upload
```

Supported formats:

- `.txt`
- `.pdf`

### Ask Question

```http
POST /ask
```

Example request:

```json
{
  "question": "What does this project demonstrate?"
}
```

Example response:

```json
{
  "answer": "This project demonstrates Retrieval-Augmented Generation, also known as RAG.",
  "sources": ["data/sample_docs/sample.txt"],
  "estimated_cost_usd": 0.000018
}
```

## Business Impact

- Reduces manual information retrieval time
- Improves access to institutional knowledge
- Enables scalable document-based AI workflows
- Demonstrates practical LLM system architecture

## Future Improvements

- Add authentication
- Add multi-user document isolation
- Add frontend interface
- Add evaluation metrics for retrieval quality
- Add Docker support
- Add cloud deployment
