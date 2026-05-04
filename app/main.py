from dotenv import load_dotenv
load_dotenv()

from app.memory import get_memory
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel

from app.auth import verify_api_key
from app.database import Base, engine
from app.history_repository import get_history
from app.rag_pipeline import RAGPipeline


DATA_DIR = Path("data/sample_docs")
DATA_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="AI Knowledge Assistant - RAG System")

Base.metadata.create_all(bind=engine)

rag = RAGPipeline(data_dir=DATA_DIR)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def health_check():
    return {"status": "ok", "project": "AI Knowledge Assistant (RAG System)"}


@app.get("/history")
def history(_: bool = Depends(verify_api_key)):
    records = get_history()

    return [
        {
            "id": r.id,
            "question": r.question,
            "answer": r.answer,
            "sources": r.sources,
            "estimated_cost_usd": r.estimated_cost_usd,
            "created_at": r.created_at.isoformat() if r.created_at else None
        }
        for r in records
    ]

@app.get("/memory")
def memory(_: bool = Depends(verify_api_key)):
    return {
        "user_id": "default_user",
        "memory": get_memory("default_user")
    }

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    _: bool = Depends(verify_api_key)
):
    if not file.filename.lower().endswith((".txt", ".pdf")):
        raise HTTPException(
            status_code=400,
            detail="Only .txt and .pdf files are supported."
        )

    file_path = DATA_DIR / file.filename
    content = await file.read()
    file_path.write_bytes(content)

    result = rag.index_documents()

    return {
        "message": "Document uploaded and indexed.",
        "file": file.filename,
        "result": result
    }


@app.post("/ask")
def ask_question(
    request: QuestionRequest,
    _: bool = Depends(verify_api_key)
):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    return rag.answer(request.question)