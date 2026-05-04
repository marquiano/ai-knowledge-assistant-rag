from pathlib import Path
from typing import Dict, Any

from app.tools.n8n_webhook import send_n8n_alert
from app.tools.classifier import classify_intent
from app.memory import get_context, save_context
from app.history_repository import save_query
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
            return {
                "indexed_documents": 0,
                "message": "No documents found."
            }

        build_vector_store(
            documents=docs,
            embedding_model=self.embedding_model,
            persist_dir=self.persist_dir
        )

        return {
            "indexed_documents": len(docs),
            "vector_store": str(self.persist_dir),
            "status": "success"
        }

    def _send_alert_if_needed(
        self,
        user_id: str,
        question: str,
        answer_text: str,
        sources: list,
        estimated_cost: float,
        intent_data: dict
    ) -> dict | None:
        if intent_data.get("priority") != "high":
            return None

        return send_n8n_alert({
            "user_id": user_id,
            "question": question,
            "answer": answer_text,
            "sources": sources,
            "estimated_cost_usd": estimated_cost,
            "intent": intent_data
        })

    def answer(self, question: str, user_id: str = "default_user") -> Dict[str, Any]:
        memory_context = "\n".join(get_context(user_id))
        intent_data = classify_intent(question)

        vector_store = load_vector_store(
            embedding_model=self.embedding_model,
            persist_dir=self.persist_dir
        )

        retriever = vector_store.as_retriever(search_kwargs={"k": 4})
        retrieved_docs = retriever.invoke(question)

        if not retrieved_docs:
            answer_text = "I could not find enough context in the indexed documents."
            sources = []
            estimated_cost = 0

            save_query(
                question=question,
                answer=answer_text,
                sources=sources,
                cost=estimated_cost
            )

            save_context(user_id, question, answer_text)

            n8n_alert = self._send_alert_if_needed(
                user_id=user_id,
                question=question,
                answer_text=answer_text,
                sources=sources,
                estimated_cost=estimated_cost,
                intent_data=intent_data
            )

            return {
                "answer": answer_text,
                "sources": sources,
                "estimated_cost_usd": estimated_cost,
                "intent": intent_data,
                "n8n_alert": n8n_alert
            }

        context = "\n\n".join([doc.page_content for doc in retrieved_docs])

        prompt = f"""
You are an AI assistant.

Use the conversation history only when it helps clarify references such as "it", "that", "the previous answer", or follow-up questions.

Intent classification:
{intent_data}

Conversation history:
{memory_context}

Document context:
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

        estimated_cost = estimate_openai_cost(prompt, answer_text)

        save_query(
            question=question,
            answer=answer_text,
            sources=sources,
            cost=estimated_cost
        )

        save_context(user_id, question, answer_text)

        n8n_alert = self._send_alert_if_needed(
            user_id=user_id,
            question=question,
            answer_text=answer_text,
            sources=sources,
            estimated_cost=estimated_cost,
            intent_data=intent_data
        )

        return {
            "answer": answer_text,
            "sources": sources,
            "estimated_cost_usd": estimated_cost,
            "intent": intent_data,
            "n8n_alert": n8n_alert
        }