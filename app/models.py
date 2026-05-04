from sqlalchemy import Column, Integer, Text, DateTime, Float
from datetime import datetime
from app.database import Base

class QueryHistory(Base):
    __tablename__ = "query_history"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    sources = Column(Text)
    estimated_cost_usd = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)