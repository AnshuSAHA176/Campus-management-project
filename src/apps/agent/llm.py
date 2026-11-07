
import os
import logging
from itertools import cycle
from threading import Lock

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

logger = logging.getLogger(__name__)

API_KEYS = [
   
    os.getenv("GROQ_API_KEY_2"),
    os.getenv("GROQ_API_KEY_3"),
]

API_KEYS = [key for key in API_KEYS if key]

if not API_KEYS:
    raise ValueError("No Groq API keys configured")

key_cycle = cycle(API_KEYS)
key_lock = Lock()


def get_next_key():
    with key_lock:
        return next(key_cycle)


def get_model(model="openai/gpt-oss-120b"):
    return ChatGroq(
        model=model,
        temperature=0,
        max_retries=2,
        reasoning_effort="low",
        max_tokens=512,
    )
