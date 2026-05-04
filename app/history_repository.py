from app.database import SessionLocal
from app.models import QueryHistory

def save_query(question, answer, sources, cost):
    db = SessionLocal()
    try:
        record = QueryHistory(
            question=question,
            answer=answer,
            sources=", ".join(sources) if sources else "",
            estimated_cost_usd=cost
        )
        db.add(record)
        db.commit()
    finally:
        db.close()


def get_history():
    db = SessionLocal()
    try:
        return db.query(QueryHistory).order_by(QueryHistory.created_at.desc()).all()
    finally:
        db.close()