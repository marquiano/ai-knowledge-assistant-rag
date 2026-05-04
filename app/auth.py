import os
from fastapi import Header, HTTPException
from dotenv import load_dotenv

load_dotenv()

RAG_API_KEY = os.getenv("RAG_API_KEY")


def verify_api_key(x_api_key: str = Header(None)):
    if not RAG_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="RAG_API_KEY is not configured."
        )

    if x_api_key != RAG_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key."
        )

    return True