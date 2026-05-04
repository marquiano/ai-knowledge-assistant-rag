import os
import redis
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)


def save_context(user_id: str, question: str, answer: str):
    key = f"context:{user_id}"

    redis_client.lpush(
        key,
        f"Q: {question}\nA: {answer}"
    )

    redis_client.ltrim(key, 0, 4)


def get_context(user_id: str = "default_user"):
    key = f"context:{user_id}"
    return redis_client.lrange(key, 0, 4)


def get_memory(user_id: str = "default_user"):
    return get_context(user_id)