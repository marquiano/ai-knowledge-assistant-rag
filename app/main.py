from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from pathlib import Path
from app.rag_pipeline import RAGPipeline

DATA_DIR = Path("data/sample_docs")
DATA_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="AI Knowledge Assistant - RAG System")
rag = RAGPipeline(data_dir=DATA_DIR)

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def health_check():
    return {"status": "ok", "project": "AI Knowledge Assistant (RAG System)"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".txt", ".pdf")):
        raise HTTPException(status_code=400, detail="Only .txt and .pdf files are supported.")

    file_path = DATA_DIR / file.filename
    content = await file.read()
    file_path.write_bytes(content)

    result = rag.index_documents()
    return {"message": "Document uploaded and indexed.", "file": file.filename, "result": result}

@app.post("/ask")
def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    answer = rag.answer(request.question)
    return answer
