from pathlib import Path
from langchain_chroma import Chroma

def build_vector_store(documents, embedding_model, persist_dir: Path):
    persist_dir.mkdir(parents=True, exist_ok=True)

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=str(persist_dir)
    )

    return vector_store

def load_vector_store(embedding_model, persist_dir: Path):
    return Chroma(
        persist_directory=str(persist_dir),
        embedding_function=embedding_model
    )
