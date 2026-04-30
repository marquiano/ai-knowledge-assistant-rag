from pathlib import Path
from typing import Dict, Any
from app.loader import load_documents
from app.embeddings import get_embedding_model
from app.llm import get_llm
from app.retriever import build_vector_store, load_vector_store
from app.utils import estimate_openai_cost

class RAGPipeline:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.persist_dir = Path("vector_store")
        self.embedding_model = get_embedding_model()
        self.llm = get_llm()

    def index_documents(self) -> Dict[str, Any]:
        docs = load_documents(self.data_dir)
        if not docs:
            return {"indexed_documents": 0, "message": "No documents found."}

        vector_store = build_vector_store(
            documents=docs,
            embedding_model=self.embedding_model,
            persist_dir=self.persist_dir
        )

        return {
            "indexed_documents": len(docs),
            "vector_store": str(self.persist_dir),
            "status": "success"
        }

    def answer(self, question: str) -> Dict[str, Any]:
        vector_store = load_vector_store(
            embedding_model=self.embedding_model,
            persist_dir=self.persist_dir
        )

        retriever = vector_store.as_retriever(search_kwargs={"k": 4})
        retrieved_docs = retriever.invoke(question)

        if not retrieved_docs:
            return {
                "answer": "I could not find enough context in the indexed documents.",
                "sources": [],
                "estimated_cost_usd": 0
            }

        context = "\n\n".join([doc.page_content for doc in retrieved_docs])

        prompt = f"""
You are an AI knowledge assistant.

Answer the user's question using only the context below.
If the answer is not present in the context, say that the information was not found.

Context:
{context}

Question:
{question}
"""

        response = self.llm.invoke(prompt)
        answer_text = response.content if hasattr(response, "content") else str(response)

        sources = list({
            doc.metadata.get("source", "unknown")
            for doc in retrieved_docs
        })

        return {
            "answer": answer_text,
            "sources": sources,
            "estimated_cost_usd": estimate_openai_cost(prompt, answer_text)
        }
